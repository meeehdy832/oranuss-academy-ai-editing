#!/usr/bin/env python3
"""Find and safely remove junk files and duplicate files in a folder.

Safe by design:
  * Default is a dry run: nothing is touched, a report is printed/written.
  * --apply MOVES files into a quarantine folder (never deletes) and writes
    an undo manifest. --restore puts everything back.
  * .git, the quarantine folder itself and symlinks are never touched.

Usage:
  python clean_folder.py PATH                      # dry run, report only
  python clean_folder.py PATH --report report.md   # also save the report
  python clean_folder.py PATH --apply              # quarantine junk + duplicates
  python clean_folder.py PATH --apply --only dupes # only duplicates (or: junk, empty)
  python clean_folder.py PATH --restore            # undo the last --apply
  python clean_folder.py PATH --empty-trash        # permanently delete quarantine
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shutil
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

TRASH_DIR = "_cleanup_trash"
NEVER_ENTER = {".git", ".hg", ".svn", TRASH_DIR}

# System / temporary junk that is always safe to remove.
JUNK_FILE_PATTERNS = [
    ".DS_Store", "._*", "Thumbs.db", "ehthumbs.db", "desktop.ini", "Icon\r",
    "*.tmp", "*.temp", "~$*", "*.swp", "*.swo", "*~", ".~lock.*#",
    "*.crdownload", "*.part", "*.partial", "*.download",
    "*.pyc", "*.pyo", "npm-debug.log*", "yarn-error.log*",
]
JUNK_DIR_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".ipynb_checkpoints"}

# Big folders that can be regenerated. Reported only; removed only with --include-regenerable.
REGENERABLE_DIRS = {"node_modules", ".venv", "venv", "dist", "build", ".next", ".parcel-cache", ".cache", "target"}

# Name markers of copies, used to decide which duplicate to KEEP (the one without them).
COPY_MARKERS = re.compile(
    r"(\s*\(\d+\)$)|(\s*-\s*copy(\s*\(\d+\))?$)|(\s+copy(\s+\d+)?$)|(_copy\d*$)|(\s*-\s*نسخة$)|(\s*\(copie\)$)",
    re.IGNORECASE,
)


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n} B"


def sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def quick_hash(path: Path) -> str:
    """Hash of the first and last 64 KB: a cheap pre-filter before the full hash."""
    size = path.stat().st_size
    h = hashlib.sha256()
    with path.open("rb") as f:
        h.update(f.read(65536))
        if size > 131072:
            f.seek(-65536, os.SEEK_END)
            h.update(f.read(65536))
    return h.hexdigest()


def is_junk_file(name: str) -> bool:
    return any(fnmatch.fnmatchcase(name, p) for p in JUNK_FILE_PATTERNS)


def scan(root: Path, include_regenerable: bool, extra_ignore: list[str]):
    files, junk, regenerable, empty_dirs = [], [], [], []
    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        d = Path(dirpath)
        keep = []
        for name in dirnames:
            p = d / name
            if name in NEVER_ENTER or p.is_symlink() or any(fnmatch.fnmatch(name, g) for g in extra_ignore):
                continue
            if name in JUNK_DIR_NAMES:
                junk.append(p)
                continue
            if name in REGENERABLE_DIRS:
                regenerable.append(p)
                if not include_regenerable:
                    continue
                continue  # whole folder is handled as one item; don't descend
            keep.append(name)
        dirnames[:] = keep
        for name in filenames:
            p = d / name
            if p.is_symlink() or any(fnmatch.fnmatch(name, g) for g in extra_ignore):
                continue
            if is_junk_file(name):
                junk.append(p)
            else:
                files.append(p)
    # Empty folders (bottom-up), ignoring ones that only contain junk we will move.
    junk_set = {str(j) for j in junk}
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        d = Path(dirpath)
        if d == root or any(part in NEVER_ENTER | REGENERABLE_DIRS | JUNK_DIR_NAMES for part in d.relative_to(root).parts):
            continue
        children = [c for c in d.iterdir() if str(c) not in junk_set and c not in empty_dirs]
        if not children:
            empty_dirs.append(d)
    return files, junk, regenerable, empty_dirs


def find_duplicates(files: list[Path]):
    by_size = defaultdict(list)
    for f in files:
        try:
            s = f.stat().st_size
        except OSError:
            continue
        if s > 0:
            by_size[s].append(f)
    groups = []
    for size, same in by_size.items():
        if len(same) < 2:
            continue
        by_quick = defaultdict(list)
        for f in same:
            by_quick[quick_hash(f)].append(f)
        for cands in by_quick.values():
            if len(cands) < 2:
                continue
            by_full = defaultdict(list)
            for f in cands:
                by_full[sha256(f)].append(f)
            for digest, dupes in by_full.items():
                if len(dupes) > 1:
                    groups.append((size, digest, dupes))
    return groups


def choose_keeper(paths: list[Path]) -> Path:
    """Keep the 'original': no copy marker in the name, then shallowest path, then oldest."""
    def key(p: Path):
        return (
            bool(COPY_MARKERS.search(p.stem)),
            len(p.parts),
            p.stat().st_mtime,
            len(p.name),
            str(p),
        )
    return sorted(paths, key=key)[0]


def size_of(p: Path) -> int:
    if p.is_file():
        return p.stat().st_size
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file() and not f.is_symlink())


def build_plan(root: Path, args):
    files, junk, regenerable, empty_dirs = scan(root, args.include_regenerable, args.ignore or [])
    only = set(args.only or ["junk", "dupes", "empty"])
    plan = []  # (category, path, reason)
    if "junk" in only:
        for p in junk:
            plan.append(("junk", p, "system/temporary file"))
        if args.include_regenerable:
            for p in regenerable:
                plan.append(("regenerable", p, "can be rebuilt (dependencies/build output)"))
    dup_groups = find_duplicates(files) if "dupes" in only else []
    for size, digest, dupes in dup_groups:
        keeper = choose_keeper(dupes)
        for p in dupes:
            if p != keeper:
                plan.append(("duplicate", p, f"same content as {keeper.relative_to(root)}"))
    if "empty" in only:
        planned = {str(p) for _, p, _ in plan}
        for d in empty_dirs:
            if str(d) not in planned:
                plan.append(("empty_folder", d, "empty folder"))
    for p in files:
        if "empty" in only and p.stat().st_size == 0 and not p.name.startswith(".") and p.name not in {"__init__.py", ".gitkeep", ".keep"}:
            plan.append(("empty_file", p, "0-byte file"))
    return plan, dup_groups, regenerable, files


def write_report(root: Path, plan, dup_groups, regenerable, files, top_n: int) -> str:
    lines = [f"# Folder cleanup report: {root}", "", f"_Generated {datetime.now():%Y-%m-%d %H:%M}_", ""]
    total = sum(size_of(p) for _, p, _ in plan)
    by_cat = defaultdict(list)
    for cat, p, why in plan:
        by_cat[cat].append((p, why))
    lines += ["## Summary", "", "| Category | Items | Space |", "|---|---|---|"]
    for cat, items in by_cat.items():
        lines.append(f"| {cat} | {len(items)} | {human(sum(size_of(p) for p, _ in items))} |")
    lines += [f"| **Total to clean** | **{len(plan)}** | **{human(total)}** |", ""]

    if dup_groups:
        lines += ["## Duplicate groups (kept file first)", ""]
        for size, digest, dupes in sorted(dup_groups, key=lambda g: -g[0] * (len(g[2]) - 1)):
            keeper = choose_keeper(dupes)
            lines.append(f"- **{human(size)}** × {len(dupes)} · keep `{keeper.relative_to(root)}`")
            for p in dupes:
                if p != keeper:
                    lines.append(f"  - remove `{p.relative_to(root)}`")
        lines.append("")
    for cat in ("junk", "empty_file", "empty_folder", "regenerable"):
        if by_cat.get(cat):
            lines += [f"## {cat.replace('_', ' ').title()}", ""]
            lines += [f"- `{p.relative_to(root)}` ({human(size_of(p))})" for p, _ in by_cat[cat][:200]]
            if len(by_cat[cat]) > 200:
                lines.append(f"- … and {len(by_cat[cat]) - 200} more")
            lines.append("")
    if regenerable and not by_cat.get("regenerable"):
        lines += ["## Regenerable folders (not touched; use --include-regenerable)", ""]
        lines += [f"- `{p.relative_to(root)}` ({human(size_of(p))})" for p in regenerable]
        lines.append("")
    big = sorted(files, key=lambda f: f.stat().st_size, reverse=True)[:top_n]
    if big:
        lines += [f"## Largest {len(big)} files (for your review, not removed)", ""]
        lines += [f"- `{f.relative_to(root)}` ({human(f.stat().st_size)})" for f in big]
        lines.append("")
    return "\n".join(lines)


def apply_plan(root: Path, plan) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    trash = root / TRASH_DIR / stamp
    moved = []
    # Move deepest paths first so folders don't vanish under their children.
    for cat, p, why in sorted(plan, key=lambda x: -len(x[1].parts)):
        if not p.exists():
            continue
        rel = p.relative_to(root)
        dest = trash / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p), str(dest))
        moved.append({"category": cat, "from": str(rel), "reason": why})
    (trash / "_manifest.json").write_text(json.dumps(moved, indent=2, ensure_ascii=False), encoding="utf-8")
    return trash


def restore(root: Path) -> int:
    base = root / TRASH_DIR
    runs = sorted(d for d in base.glob("*") if (d / "_manifest.json").exists()) if base.exists() else []
    if not runs:
        print("Nothing to restore.")
        return 1
    run = runs[-1]
    items = json.loads((run / "_manifest.json").read_text(encoding="utf-8"))
    restored = 0
    for item in sorted(items, key=lambda i: len(Path(i["from"]).parts)):
        src, dest = run / item["from"], root / item["from"]
        if not src.exists():
            continue
        if dest.exists() and dest.is_file():
            print(f"skip (already exists): {item['from']}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir() and dest.is_dir():
            for child in src.iterdir():
                shutil.move(str(child), str(dest / child.name))
        else:
            shutil.move(str(src), str(dest))
        restored += 1
    shutil.rmtree(run)
    if not any(base.iterdir()):
        base.rmdir()
    print(f"Restored {restored} item(s) from {run.name}.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Find and safely clean junk and duplicate files.")
    ap.add_argument("path", help="folder to clean")
    ap.add_argument("--apply", action="store_true", help="move items to the quarantine folder (default: dry run)")
    ap.add_argument("--only", nargs="+", choices=["junk", "dupes", "empty"], help="limit to these categories")
    ap.add_argument("--include-regenerable", action="store_true", help="also clean node_modules, venv, build output…")
    ap.add_argument("--ignore", nargs="+", metavar="GLOB", help="names to skip, e.g. '*.psd' 'Archive'")
    ap.add_argument("--report", metavar="FILE", help="save the report as Markdown")
    ap.add_argument("--top", type=int, default=10, help="list the N largest files (default 10)")
    ap.add_argument("--restore", action="store_true", help="undo the last --apply")
    ap.add_argument("--empty-trash", action="store_true", help="permanently delete the quarantine folder")
    ap.add_argument("--yes", action="store_true", help="don't ask for confirmation")
    args = ap.parse_args()

    root = Path(args.path).expanduser().resolve()
    if not root.is_dir():
        print(f"Not a folder: {root}", file=sys.stderr)
        return 2
    if root == Path(root.anchor) or root == Path.home():
        print("Refusing to clean a drive root or the whole home folder. Pick a specific folder.", file=sys.stderr)
        return 2

    if args.restore:
        return restore(root)
    if args.empty_trash:
        t = root / TRASH_DIR
        if not t.exists():
            print("Quarantine is already empty.")
            return 0
        if not args.yes and input(f"Permanently delete {t} ({human(size_of(t))})? [y/N] ").lower() != "y":
            print("Cancelled.")
            return 1
        shutil.rmtree(t)
        print("Quarantine deleted permanently.")
        return 0

    plan, dup_groups, regenerable, files = build_plan(root, args)
    report = write_report(root, plan, dup_groups, regenerable, files, args.top)
    print(report)
    if args.report:
        Path(args.report).write_text(report, encoding="utf-8")
        print(f"\nReport saved to {args.report}")

    if not plan:
        print("\nNothing to clean.")
        return 0
    if not args.apply:
        print(f"\nDRY RUN: nothing was changed. Re-run with --apply to move {len(plan)} item(s) to {TRASH_DIR}/.")
        return 0
    if not args.yes and input(f"\nMove {len(plan)} item(s) to {TRASH_DIR}/? [y/N] ").lower() != "y":
        print("Cancelled.")
        return 1
    trash = apply_plan(root, plan)
    print(f"\nMoved {len(plan)} item(s) to {trash.relative_to(root)}. Undo with --restore; delete for good with --empty-trash.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
