[CmdletBinding()]
param([string]$Python = "python")

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
& $Python (Join-Path $PSScriptRoot "verify.py")
