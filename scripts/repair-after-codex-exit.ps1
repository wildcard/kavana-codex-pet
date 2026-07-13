[CmdletBinding()]
param(
    [string]$CodexHome = $(if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }),
    [int]$TimeoutSeconds = 600
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$deadline = (Get-Date).AddSeconds($TimeoutSeconds)
while (Get-Process -Name "Codex" -ErrorAction SilentlyContinue) {
    if ((Get-Date) -gt $deadline) { throw "Timed out while Codex Desktop was still running." }
    Start-Sleep -Seconds 2
}
& (Join-Path $PSScriptRoot "check-mobile-sync.ps1") -CodexHome $CodexHome -Repair
