# Oranuss Academy AI Editing: التثبيت بنص واحد (Mac و Windows)

> Developed by Mehdi ORANUSS | Powered by Claude

## للزبون

نسخ **هاد النص كامل** (ماشي غير الرابط)، والصقو فـ **Claude Code**، ومن بعد ورك Enter. Claude كيتكلف بكلشي:
- كيحمّل الملفات ديال Oranuss.
- كيثبت المهارات والأدوات من الروابط الأصلية ديالهم.
- كيوجد ليك الدوسي ديال المونتاج.
- ومن بعد كيسولك واش نبداو فيديو.

**خاصك:**
- **Mac** (Apple Silicon) ولا **Windows 10/11**.
- اشتراك Claude فيه Claude Code (التطبيق ديال Claude، الخانة **Code**).
- تقريبا 5 GB خاويين، والأنترنيت.

**مهم:**
- **ماتعطيش هاد النص لحد.** فيه المفتاح ديال الدخول ديالك.
- وافق على الأوامر اللي كيطلب Claude.
- إلا طلب منك تكتب شي أمر بيدك (كلمة سر ديال الماك، ولا نافذة ديال Windows كتطلب الإذن)، ديرها نتا.

---

You are installing **Oranuss Academy AI Editing** (Claude Code video editing for Moroccan Darija content) on this computer.
Talk to the user in **Moroccan Darija written in Arabic letters**: short and simple. Say what you do before each step. Never skip a check. If something fails, stop, explain, and fix it with the user.
The files are in a **private** GitHub repo. Download them only through the GitHub API with the key below. Do not use `git clone`, do not open the repo page, and do not ask the user to sign in to GitHub. **Never print, log or repeat the key.** Pass it only through the `KIT_TOKEN` environment variable.

- `REPO` = `meeehdy832/oranuss-academy-ai-editing`
- `KIT_TOKEN` = `PASTE_READ_ONLY_KEY_HERE`
- Folder: `oranuss-academy-ai-editing` in the user's Documents.

### 1. Detect the system
- **Mac:** `uname -sm` must be `Darwin arm64`. On an Intel Mac, stop and say the kit needs Apple Silicon.
- **Windows:** use PowerShell. Check the version with `[Environment]::OSVersion.Version` (10.0 or more) and check that `winget --version` works. If winget is missing, ask the user to install **App Installer** from the Microsoft Store.
- Check there are 5 GB free (Mac: `df -h ~`; Windows: `Get-PSDrive C`).

### 2. Ask before the big downloads (Darija, yes or no each)
- the tools: about 1 GB;
- the transcription model: 2.9 GB, needed to turn Darija speech into captions;
- earshot: optional, about 100 MB.

Recommend yes to the first two.

### 3. Prerequisites
- **Mac:**
  - If `brew` is missing, the user installs it (it needs their Mac password). Give them this command in a `bash` block for the Terminal app, then wait:
    `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
    Then: `echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile && eval "$(/opt/homebrew/bin/brew shellenv)"`
  - If `xcode-select -p` fails, the user runs `xcode-select --install`.
- **Windows:** nothing to do before. winget installs Git, FFmpeg, Node.js and Python. Windows may show permission windows: tell the user to click **Yes**.

### 4. Download the installer with the key, then read it
- **Mac:**
  `curl -fsSL -H "Authorization: Bearer $KIT_TOKEN" -H "Accept: application/vnd.github.raw" "https://api.github.com/repos/meeehdy832/oranuss-academy-ai-editing/contents/install.sh" -o /tmp/oranuss-install.sh`
- **Windows** (PowerShell):
  `Invoke-WebRequest -UseBasicParsing -Headers @{Authorization="Bearer $env:KIT_TOKEN"; Accept="application/vnd.github.raw"; "User-Agent"="oranuss"} -Uri "https://api.github.com/repos/meeehdy832/oranuss-academy-ai-editing/contents/install.ps1" -OutFile "$env:TEMP\oranuss-install.ps1"`
- Set the variable first, in the same command: `KIT_TOKEN='…' curl …` on Mac, `$env:KIT_TOKEN='…'; Invoke-WebRequest …` on Windows.
- An HTTP 401 or 404 means the key is wrong or expired. Then stop and tell the user (in Darija) to ask Oranuss Academy for a new install text.
- Read the whole installer before running it. It must only:
  - copy files;
  - download the repo through api.github.com with the key;
  - run `npx skills add` from GitHub;
  - install tools (brew on Mac, winget on Windows);
  - download files from huggingface.co and github.com.

### 5. Install (in the background, once; never two runs at once)
- **Mac:** `KIT_TOKEN='…' bash /tmp/oranuss-install.sh ~/Documents/oranuss-academy-ai-editing --tools --model` (add `--earshot` if accepted).
- **Windows:** `$env:KIT_TOKEN='…'; powershell -ExecutionPolicy Bypass -File "$env:TEMP\oranuss-install.ps1" -Tools -Model` (add `-Earshot` if accepted).
  After it finishes, open a new PowerShell so the new PATH is used.
- Drop any flag the user refused. The installer never overwrites existing files, so running it again is safe.

### 6. Verify
- Every installer line must be ✅ / [OK]. Fix each ❌ / [X] (usually: run the tool command it names, then run the installer again).
- Then check yourself:
  - the global skills folder (`~/.claude/skills`, on Windows `%USERPROFILE%\.claude\skills`) has 30 or more folders;
  - the project skills folder (`oranuss-academy-ai-editing/.claude/skills`) has 15 or more;
  - `ffmpeg -version` works;
  - `whisper-cli --help` works;
  - `node -v` works.
- Delete the downloaded installer (`/tmp/oranuss-install.sh` or `%TEMP%\oranuss-install.ps1`).
- Show the user one short table in Darija with ✅ or ❌ per item.

### 7. Explain (Darija, short)
- The editing folder is `Documents/oranuss-academy-ai-editing`.
- Where to put things:
  - videos to camera → `input/recordings/`;
  - voice-only audio → `input/voiceover/`;
  - images and clips → `input/B-ROLL/`;
  - music → `music/`.
- How a video gets made: Claude asks questions, writes a plan, shows still images, then a preview. The final video only comes after the user's OK.
- Claude Code must be opened **on that folder** so the house rules (`CLAUDE.md`) and the project skills load.
- **Windows only:** face tracking uses `project/.venv` + `project/tools/face_track.py` (instead of the Mac helper), and `ffmpeg` and `whisper-cli` come from PATH.

### 8. Ask to start
Ask exactly this, then wait:

**«صافي، كلشي تثبت ✅. واش مستعد نبداو نخدمو على فيديو دابا، ولا تبغي نأجلوها لوقت آخر؟»**

- **Now:** if this session is not in `Documents/oranuss-academy-ai-editing`, ask the user to open a new Claude Code session on that folder, put the video in `input/recordings/`, and write «بغيت نصاوب فيديو». If it already is, start: ask about the video, the format (9:16 or 16:9) and the style.
- **Later:** say goodbye in Darija. Next time they only need to open a session on that folder and say «بغيت نصاوب فيديو».
