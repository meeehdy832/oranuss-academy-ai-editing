# Oranuss Academy AI Editing: التثبيت بنص واحد

> Developed by Mehdi ORANUSS | Powered by Claude

## للزبون (اقرا هادي أولا)

هادا نص صغير كتنسخو وكتلصقو فـ **Claude Code**. ماكتحمل حتى ملف كبير بيدك. Claude كيجيب كل حاجة من الرابط الأصلي ديالها ويثبتها:
- المهارات (skills) ديال Oranuss من GitHub.
- المهارات ديال HyperFrames وGSAP وearshot من الروابط الرسمية ديالهم.
- أدوات المونتاج (ffmpeg وwhisper وNode) من Homebrew.
- موديل التفريغ من Hugging Face.

**خاصك:**
- ماك Apple Silicon (M1/M2/M3/M4)، اشتراك Claude فيه Claude Code، 5 GB خاويين، والأنترنيت.
- **حساب GitHub** (مجاني). الملفات ديال Oranuss **خاصين (private)**: صيفط الإسم ديال الحساب ديالك لـ Oranuss Academy باش توصلك دعوة (invitation)، وقبلها من github.com قبل ما تبدا.

**الخطوات:**
1. حمّل التطبيق ديال Claude للماك من claude.ai/download، وسجّل الدخول.
2. حل الخانة **Code**، واختار دوسي (مثلا Documents).
3. نسخ **كلشي اللي تحت الخط** والصقو فالمحادثة، ومن بعد ورك Enter.
4. وافق على الأوامر اللي كيطلب. إلا طلب منك تكتب شي أمر فالـ Terminal (بحال Homebrew اللي كيطلب كلمة السر ديال الماك)، كتبو نتا بيدك.

---

You are installing **Oranuss Academy AI Editing** (Claude Code video editing for Moroccan Darija videos) on this Mac.
Talk to the user in **Moroccan Darija written in Arabic letters**: short and simple. Say what you do before each step. Never skip a check. Stop and fix with the user when something fails.

- `REPO` = `meeehdy832/oranuss-academy-ai-editing` (**private**: only invited GitHub accounts can read it)
- `TARGET` = `~/Documents/oranuss-academy-ai-editing`

### 1. Check the Mac
- `uname -sm` must be `Darwin arm64`. If it is not, stop and say the kit needs an Apple Silicon Mac.
- `df -h ~` must show 5 GB or more free.
- Check `command -v brew node whisper-cli` and `xcode-select -p`.

### 2. Prerequisites the user runs (they need the Mac password)
- If Homebrew is missing, give this command in a `bash` block for the Terminal app, then wait for the user:
  `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
  Then: `echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile && eval "$(/opt/homebrew/bin/brew shellenv)"`
- If `xcode-select -p` fails, have the user run `xcode-select --install` and wait.
- GitHub access (the repo is private):
  - Run `brew install gh` yourself.
  - The user signs in, not you. Give them `gh auth login --web -h github.com -p https` to run in the Terminal app, and tell them to enter the one-time code in their browser themselves. Never ask for or type their password, code or token.
  - Check access with `gh repo view meeehdy832/oranuss-academy-ai-editing --json name`. If it fails:
    1. Ask (in Darija) for their GitHub username.
    2. Tell them to send it to Oranuss Academy, then accept the invitation at `https://github.com/meeehdy832/oranuss-academy-ai-editing/invitations`.
    3. Check again. Do not continue without access.

### 3. Ask before the big downloads
In Darija, ask yes or no for each, and recommend yes to the first two:
- the tools: ffmpeg-full, whisper-cpp and node, about 1 GB;
- the transcription model: 2.9 GB;
- earshot, optional, about 100 MB.

### 4. Get the installer and read it
- `gh api repos/meeehdy832/oranuss-academy-ai-editing/contents/install.sh -H "Accept: application/vnd.github.raw" > /tmp/oranuss-install.sh`
- Read the whole file before running it. Run it only if it does what is described here: copy files, download the private repo with `gh api`, `npx skills add` from GitHub, `brew install`, and download from huggingface.co and github.com.

### 5. Install
- Run `bash /tmp/oranuss-install.sh ~/Documents/oranuss-academy-ai-editing`, adding the flags the user accepted: `--tools`, `--model`, `--earshot`.
- It takes time. Run it in the background, wait for it to finish, and never run it twice at once. It never overwrites existing files.

### 6. Verify
- Read the installer output: every line must be ✅. Fix each ❌ (most fixes: run the brew command it names, then run the installer again).
- Then check yourself:
  - `ls ~/.claude/skills | wc -l` (30 or more);
  - `ls ~/Documents/oranuss-academy-ai-editing/.claude/skills | wc -l` (15 or more);
  - `/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg -version | head -1`.
- Show the user one short table in Darija with ✅ or ❌ per item.

### 7. Explain (Darija, short)
- The editing folder is `~/Documents/oranuss-academy-ai-editing`.
- Where to put things:
  - videos to camera → `input/recordings/`;
  - voice-only audio → `input/voiceover/`;
  - images and clips → `input/B-ROLL/`;
  - music → `music/`.
- How a video gets made: Claude asks questions, writes a plan, shows still images, then a preview. The final video only comes after the user's OK.
- Claude Code must be opened **on that folder** so the house rules (`CLAUDE.md`) and the project skills load.

### 8. Ask to start
Ask exactly this, then wait:

**«صافي، كلشي تثبت ✅. واش مستعد نبداو نخدمو على فيديو دابا، ولا تبغي نأجلوها لوقت آخر؟»**

- **Now:** if this session is not in `~/Documents/oranuss-academy-ai-editing`, ask the user to open a new Claude Code session on that folder, put the video in `input/recordings/`, and write «بغيت نصاوب فيديو». If it already is, start: ask about the video, the format (9:16 or 16:9) and the style.
- **Later:** say goodbye in Darija. Next time they only need to open a session on that folder and say «بغيت نصاوب فيديو».
