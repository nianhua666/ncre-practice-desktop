$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Get-Process NCREPractice -ErrorAction SilentlyContinue | Stop-Process -Force

python .\scripts\generate_seed_banks.py
python -m pip install -r .\requirements.txt

$version = @'
from backend.config import APP_VERSION
print(APP_VERSION)
'@ | python -
$version = $version.Trim()

python -m PyInstaller `
  --noconfirm `
  --clean `
  --name "NCREPractice" `
  --add-data "frontend;frontend" `
  --add-data "data;data" `
  .\main.py

python .\scripts\smoke_test_packaged.py

$zipPath = ".\dist\NCREPractice-v$version-win64.zip"
if (Test-Path $zipPath) {
  Remove-Item $zipPath -Force
}
Compress-Archive -Path .\dist\NCREPractice\* -DestinationPath $zipPath

if (Test-Path .\build) {
  Remove-Item .\build -Recurse -Force
}

Write-Host "Build finished. EXE output: dist\\NCREPractice\\NCREPractice.exe"
