# Oranuss Academy AI Editing: installer for Windows 10/11. Developed by Mehdi ORANUSS | Powered by Claude
# usage (PowerShell):
#   powershell -ExecutionPolicy Bypass -File install.ps1 [-Target <folder>] [-Tools] [-Model] [-Earshot]
#   -Tools    winget: Git, FFmpeg (full build, libass), Node.js LTS, Python 3.12 + whisper.cpp from GitHub releases
#   -Model    whisper large-v3 model (2.9 GB, Hugging Face)
#   -Earshot  earshot (listen/judge sound) into a Python venv
# Oranuss files come from this public repo; every other piece comes from its own official link (SOURCES.md).
# Never overwrites an existing file.
param(
  [string]$Target = (Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'oranuss-academy-ai-editing'),
  [switch]$Tools, [switch]$Model, [switch]$Earshot
)
$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$Repo = 'meeehdy832/oranuss-academy-ai-editing'
function Ok($m) { Write-Host "   [OK] $m" -ForegroundColor Green }
function No($m) { Write-Host "   [X]  $m" -ForegroundColor Red }
function Have($c) { [bool](Get-Command $c -ErrorAction SilentlyContinue) }
function Refresh-Path { $env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User') }
function Copy-New($from, $to) { New-Item -ItemType Directory -Force -Path $to | Out-Null; robocopy $from $to /E /XC /XN /XO /NFL /NDL /NJH /NJS /NP | Out-Null }

Write-Host '== 1/8 Oranuss files'
if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot 'workspace')) -and (Test-Path (Join-Path $PSScriptRoot 'skills'))) {
  $Src = $PSScriptRoot
} else {
  $Tmp = Join-Path $env:TEMP ('oranuss-' + [guid]::NewGuid().ToString('N').Substring(0,8))
  New-Item -ItemType Directory -Force -Path $Tmp | Out-Null
  try {
    Invoke-WebRequest -UseBasicParsing -Uri "https://github.com/$Repo/archive/refs/heads/main.tar.gz" `
      -Headers @{ 'User-Agent' = 'oranuss-installer' } `
      -OutFile (Join-Path $Tmp 'repo.tgz')
  } catch { No 'could not download the Oranuss files. Check the internet and run again.'; exit 4 }
  tar -xzf (Join-Path $Tmp 'repo.tgz') -C $Tmp
  $Src = (Get-ChildItem $Tmp -Directory | Select-Object -First 1).FullName
}
$Skills = Join-Path $HOME '.claude\skills'
Copy-New (Join-Path $Src 'workspace') $Target
Copy-New (Join-Path $Src 'skills') $Skills
# paths written on the author's Mac -> this PC (forward slashes work in Python, ffmpeg and Node)
$T = $Target -replace '\\','/'; $H = $HOME -replace '\\','/'
foreach ($dir in @($Target, $Skills)) {
  Get-ChildItem $dir -Recurse -File -Include *.md,*.py,*.sh,*.js,*.json,*.css,*.html,*.txt,*.tsv -ErrorAction SilentlyContinue | ForEach-Object {
    $c = [IO.File]::ReadAllText($_.FullName)
    if ($c -match '/Users/Apple|/opt/homebrew') {
      $c = $c.Replace('/Users/Apple/Downloads/editing-ai', $T).Replace('/Users/Apple', $H)
      $c = $c.Replace('/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg', 'ffmpeg').Replace('/opt/homebrew/bin/', '')
      [IO.File]::WriteAllText($_.FullName, $c, (New-Object Text.UTF8Encoding $false))
    }
  }
}
Ok "workspace -> $Target ($((Get-ChildItem (Join-Path $Target '.claude\skills') -Directory).Count) project skills)"

Write-Host '== 2/8 Tools'
if ($Tools) {
  if (-not (Have 'winget')) { No 'winget missing: install "App Installer" from the Microsoft Store, then run again'; exit 2 }
  foreach ($id in 'Git.Git','Gyan.FFmpeg','OpenJS.NodeJS.LTS','Python.Python.3.12') {
    winget install --id $id -e --silent --accept-source-agreements --accept-package-agreements | Out-Null
  }
  Refresh-Path
  # whisper.cpp: official Windows build from the GitHub release
  $W = Join-Path $Target 'tools\whisper'
  if (-not (Test-Path (Join-Path $W 'whisper-cli.exe'))) {
    try {
      $rel = Invoke-RestMethod -UseBasicParsing -Uri 'https://api.github.com/repos/ggml-org/whisper.cpp/releases/latest' -Headers @{ 'User-Agent' = 'oranuss-installer' }
      $asset = $rel.assets | Where-Object { $_.name -eq 'whisper-bin-x64.zip' } | Select-Object -First 1
      $zip = Join-Path $env:TEMP 'whisper-bin-x64.zip'
      Invoke-WebRequest -UseBasicParsing -Uri $asset.browser_download_url -OutFile $zip
      Expand-Archive $zip -DestinationPath $W -Force
      $exe = Get-ChildItem $W -Recurse -Filter 'whisper-cli.exe' | Select-Object -First 1
      if ($exe) {
        $up = [Environment]::GetEnvironmentVariable('Path','User')
        if ($up -notlike "*$($exe.DirectoryName)*") { [Environment]::SetEnvironmentVariable('Path', "$up;$($exe.DirectoryName)", 'User') }
        Refresh-Path
      }
    } catch { No 'whisper.cpp download failed' }
  }
}
if (Have 'git') { Ok 'git' } else { No 'git (winget install --id Git.Git -e)' }
if (Have 'ffmpeg') { Ok 'ffmpeg' } else { No 'ffmpeg (winget install --id Gyan.FFmpeg -e)' }
if (Have 'whisper-cli') { Ok 'whisper-cli' } else { No 'whisper-cli (run again with -Tools)' }
if (Have 'node') { Ok "node $(node -v)" } else { No 'node (winget install --id OpenJS.NodeJS.LTS -e)' }
if (Have 'python') { Ok 'python' } else { No 'python (winget install --id Python.Python.3.12 -e)' }

Write-Host '== 3/8 Skills from their official repos'
if (Have 'npx') {
  npx -y skills add greensock/gsap-skills -g -a claude-code -s gsap-core -s gsap-timeline -y --copy *> $null; if ($LASTEXITCODE -eq 0) { Ok 'GSAP skills' } else { No 'GSAP skills' }
  npx -y skills add heygen-com/hyperframes -g -a claude-code -s '*' -y --copy *> $null; if ($LASTEXITCODE -eq 0) { Ok 'HyperFrames skills' } else { No 'HyperFrames skills' }
  npx -y skills add Leonxlnx/earshot -g -a claude-code -s '*' -y --copy *> $null; if ($LASTEXITCODE -eq 0) { Ok 'earshot skill' } else { No 'earshot skill' }
  Ok "global skills now: $((Get-ChildItem $Skills -Directory).Count)"
} else { No 'node missing: run again with -Tools' }

Write-Host '== 4/8 Fonts'
$FD = Join-Path $Target 'brand\fonts\free'; New-Item -ItemType Directory -Force -Path $FD | Out-Null
$F = Join-Path $FD 'NotoKufiArabic.ttf'
if (-not (Test-Path $F)) { try { Invoke-WebRequest -UseBasicParsing -Uri 'https://github.com/google/fonts/raw/main/ofl/notokufiarabic/NotoKufiArabic%5Bwght%5D.ttf' -OutFile $F } catch {} }
$UF = Join-Path $env:LOCALAPPDATA 'Microsoft\Windows\Fonts'; New-Item -ItemType Directory -Force -Path $UF | Out-Null
$fonts = @(Get-ChildItem (Join-Path $Target 'brand\fonts') -Recurse -Filter *.ttf)
foreach ($f in $fonts) {
  $dst = Join-Path $UF $f.Name
  if (-not (Test-Path $dst)) { Copy-Item $f.FullName $dst }
  New-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts' -Name "$($f.BaseName) (TrueType)" -Value $dst -PropertyType String -Force | Out-Null
}
Ok "$($fonts.Count) font file(s) installed for this user (Graphik Arabic is paid: add your licensed files to brand\fonts\graphik-arabic)"

Write-Host '== 5/8 Python + OpenCV (face tracking on Windows)'
$PV = Join-Path $Target 'project\.venv'
if (-not (Test-Path (Join-Path $PV 'Scripts\python.exe'))) {
  if (Have 'py') { py -3.12 -m venv $PV } elseif (Have 'python') { python -m venv $PV }
  & (Join-Path $PV 'Scripts\pip.exe') install -q 'opencv-python-headless<5' *> $null
}
if (Test-Path (Join-Path $PV 'Scripts\python.exe')) { Ok 'project\.venv (face tracker: project\tools\face_track.py)' } else { No 'Python venv' }

$YN = Join-Path $Target 'project\models\face_detection_yunet_2023mar.onnx'
New-Item -ItemType Directory -Force -Path (Split-Path $YN) | Out-Null
if (-not (Test-Path $YN)) { try { Invoke-WebRequest -UseBasicParsing -Uri 'https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx' -OutFile $YN } catch {} }
if (Test-Path $YN) { Ok 'YuNet face model (opencv_zoo)' } else { No 'YuNet face model' }

Write-Host '== 6/8 HyperFrames'
if (Have 'npx') { Push-Location $Target; npx -y hyperframes@0.9.9 doctor *> $null; if ($LASTEXITCODE -eq 0) { Ok 'HyperFrames ready' } else { No 'HyperFrames: run  npx hyperframes@0.9.9 doctor' }; Pop-Location }

Write-Host '== 7/8 Transcription model'
$M = Join-Path $Target 'project\models\ggml-large-v3.bin'
New-Item -ItemType Directory -Force -Path (Split-Path $M) | Out-Null
if ($Model -and -not (Test-Path $M)) { curl.exe -L --fail -o "$M.part" https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin; if ($LASTEXITCODE -eq 0) { Move-Item "$M.part" $M } }
if (Test-Path $M) { Ok 'whisper large-v3' } else { No 'model not installed (run again with -Model, 2.9 GB)' }

Write-Host '== 8/8 earshot (optional)'
if ($Earshot) {
  $E = Join-Path $Target 'tools\earshot\.venv'
  if (-not (Test-Path (Join-Path $E 'Scripts\earshot.exe'))) {
    if (Have 'py') { py -3.12 -m venv $E } else { python -m venv $E }
    & (Join-Path $E 'Scripts\pip.exe') install -q 'https://github.com/Leonxlnx/earshot/archive/refs/heads/main.zip' *> $null
  }
  if (Test-Path (Join-Path $E 'Scripts\earshot.exe')) { Ok 'earshot' } else { No 'earshot (optional)' }
} else { Write-Host '   (skipped)' }

Write-Host "DONE. Open this folder in Claude Code: $Target"
