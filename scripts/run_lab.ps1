param([ValidateSet('test', 'benchmark', 'demo', 'finalize')][string]$Task = 'test', [string]$Question = '')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $projectRoot
try {
    $portable = Join-Path $projectRoot '.runtime/python311/python.exe'
    if (Test-Path -LiteralPath $portable) {
        $labPython = $portable
    } elseif (Test-Path -LiteralPath '.venv/Scripts/python.exe') {
        $labPython = Join-Path $projectRoot '.venv/Scripts/python.exe'
    } else {
        $labPython = 'python'
    }
    if ($Task -eq 'test') { & $labPython -X utf8 -m pytest tests/ -v }
    elseif ($Task -eq 'benchmark') { & $labPython -X utf8 -m scripts.run_benchmark }
    elseif ($Task -eq 'finalize') { & $labPython -X utf8 -m scripts.finalize_lab }
    else { & $labPython -X utf8 -m scripts.demo_integrity $Question }
    if ($LASTEXITCODE -ne 0) { throw "Lab command failed with exit code $LASTEXITCODE" }
} finally { Pop-Location }
