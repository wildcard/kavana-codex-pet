[CmdletBinding()]
param(
    [string]$CodexHome = $(if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }),
    [switch]$Repair
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$petId = "custom:kavana"
$configPath = Join-Path $CodexHome "config.toml"
$statePath = Join-Path $CodexHome ".codex-global-state.json"

function Set-SelectedPetInConfig {
    if (-not (Test-Path -LiteralPath $configPath)) { New-Item -ItemType File -Force -Path $configPath | Out-Null }
    $content = Get-Content -LiteralPath $configPath -Raw
    if ($content -match '(?m)^selected-avatar-id\s*=') {
        $content = $content -replace '(?m)^selected-avatar-id\s*=.*$', "selected-avatar-id = `"$petId`""
    } else {
        $content = $content.TrimEnd() + "`r`nselected-avatar-id = `"$petId`"`r`n"
    }
    Set-Content -LiteralPath $configPath -Value $content -NoNewline
}

function Set-SelectedPetInState {
    $state = if (Test-Path -LiteralPath $statePath) { Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json } else { [pscustomobject]@{} }
    if ($state.PSObject.Properties.Name -contains "selected-avatar-id") {
        $state."selected-avatar-id" = $petId
    } else {
        $state | Add-Member -NotePropertyName "selected-avatar-id" -NotePropertyValue $petId
    }
    $state | ConvertTo-Json -Depth 100 | Set-Content -LiteralPath $statePath
}

if ($Repair) {
    Set-SelectedPetInConfig
    Set-SelectedPetInState
}

$configOk = (Test-Path -LiteralPath $configPath) -and ((Get-Content -LiteralPath $configPath -Raw) -match 'selected-avatar-id\s*=\s*"custom:kavana"')
$stateOk = $false
if (Test-Path -LiteralPath $statePath) {
    try { $stateOk = ((Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json)."selected-avatar-id" -eq $petId) } catch { $stateOk = $false }
}

Write-Host "config.toml selected: $configOk"
Write-Host ".codex-global-state.json selected: $stateOk"
if (-not ($configOk -and $stateOk)) { exit 1 }
