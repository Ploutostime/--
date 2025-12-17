#!/usr/bin/env pwsh
Write-Host "Installing Python dependencies from requirements.txt..."
$req = Join-Path $PSScriptRoot "requirements.txt"
if (-not (Test-Path $req)) { Write-Error "requirements.txt not found at $req"; exit 1 }
python -m pip install --upgrade pip
python -m pip install -r $req
Write-Host "Done."
