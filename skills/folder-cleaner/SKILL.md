---
name: folder-cleaner
description: Clean up a folder by finding duplicate files (same content, any name), system/temporary junk (.DS_Store, Thumbs.db, ~$ lock files, *.tmp, partial downloads, __pycache__), empty files and empty folders, and optionally rebuildable folders (node_modules, venv, build output). Use when the user asks to clean, tidy, declutter or free space in a folder, remove duplicated/duplicate files, find copies like "file (1).jpg" or "file - Copy", or delete things they don't need. Always safe: dry-run first, then items are moved to a quarantine folder that can be restored.
---

# Folder Cleaner

Use `scripts/clean_folder.py` (Python 3.8+, no extra packages). It works on Windows, macOS and Linux.

## Workflow (always in this order)

1. **Confirm the folder.** Use the exact path the user gives. Never run it on a drive root or the whole home folder; the script refuses those too.
2. **Dry run first** and save the report:
   ```bash
   python scripts/clean_folder.py "<FOLDER>" --report cleanup-report.md
   ```
3. **Show the user the summary**: the count and space per category, the duplicate groups (which copy is kept and which are removed), and the largest files. Point out anything that looks important, like documents, photos or project files in the duplicate list.
4. **Ask for the go-ahead.** Apply only after the user agrees. Respect any limits they set:
   ```bash
   python scripts/clean_folder.py "<FOLDER>" --apply --yes                 # everything found
   python scripts/clean_folder.py "<FOLDER>" --apply --yes --only dupes    # only duplicates
   python scripts/clean_folder.py "<FOLDER>" --apply --yes --only junk empty
   python scripts/clean_folder.py "<FOLDER>" --apply --yes --ignore "*.psd" "Archive"
   ```
5. **Tell the user** where the items went (`_cleanup_trash/<date-time>/` inside the folder) and how to undo it.
6. Only if the user explicitly asks to delete permanently:
   ```bash
   python scripts/clean_folder.py "<FOLDER>" --empty-trash --yes
   ```

**Undo:** `python scripts/clean_folder.py "<FOLDER>" --restore` puts the last cleanup back.

## What it detects

| Category | Rule |
|---|---|
| duplicate | Byte-identical content (size → quick hash → full SHA-256), whatever the file name. One file per group is kept. |
| junk | OS and app leftovers: `.DS_Store`, `._*`, `Thumbs.db`, `desktop.ini`, `~$*`, `*.tmp`, `*.swp`, `*.crdownload`, `*.part`, `*.pyc`, `__pycache__`, caches |
| empty_file | 0-byte files (except `__init__.py`, `.gitkeep`) |
| empty_folder | Folders with nothing left in them |
| regenerable | `node_modules`, `venv`, `.venv`, `dist`, `build`, `.next`, `target`, `.cache`. **Only** reported, unless `--include-regenerable` is passed. |

**Which duplicate is kept:** the one without a copy marker in its name (`(1)`, `- Copy`, `copy 2`, `_copy`, `- نسخة`), then the shallowest path, then the oldest file.

**Never touched:** `.git`/`.svn`/`.hg`, symlinks, the quarantine folder, and anything matched by `--ignore`.

## Rules for you

- Never apply without showing the dry-run results and getting a yes.
- Never use `--include-regenerable` or `--empty-trash` unless the user asks for it.
- If the duplicate list contains files the user may want in both places (for example, the same photo in two albums on purpose), ask before applying, or exclude them with `--ignore` or `--only`.
- Report outcomes plainly: how many items were moved, how much space was freed, and where they are.
