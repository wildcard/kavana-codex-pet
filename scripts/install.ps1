[CmdletBinding()]
param(
    [string]$CodexHome = $(if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }),
    [switch]$Select
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$target = Join-Path $CodexHome "pets\kavana"
New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item (Join-Path $root "dist\kavana\pet.json") $target -Force
Copy-Item (Join-Path $root "dist\kavana\spritesheet.webp") $target -Force

if ($Select) {
    & (Join-Path $PSScriptRoot "check-mobile-sync.ps1") -CodexHome $CodexHome -Repair
}

Write-Host "Installed Kavana to $target"
if (-not $Select) { Write-Host "Select Kavana in Codex Desktop: Settings > Appearance > Pets." }
