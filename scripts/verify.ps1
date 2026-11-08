param([ValidateRange(1024, 65535)][int]$Port = 8765)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$python = Join-Path $root '.venv/Scripts/python.exe'
$bun = Get-Command bun -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Source
if (-not $bun) { $bun = Join-Path $env:USERPROFILE '.bun/bin/bun.exe' }
if (-not (Test-Path -LiteralPath $python)) { throw 'Create .venv as described in SETUP.md.' }
if (-not (Test-Path -LiteralPath $bun)) { throw 'Install Bun as described in SETUP.md.' }

function Invoke-Stage($Label, $Command, [string[]]$Arguments) {
    Write-Host "`n== $Label =="
    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$Label failed with exit code $LASTEXITCODE." }
    Write-Host "Passed $Label"
}

$previousDebug = $env:ATLAS_DEBUG
$previousOrigin = $env:ATLAS_BASE_URL
$server = $null
Push-Location $root
try {
    $env:ATLAS_DEBUG = '0'
    $env:ATLAS_BASE_URL = "http://127.0.0.1:$Port"
    Invoke-Stage 'Python dependencies' $python @('-m', 'pip', 'check')
    Invoke-Stage 'Django checks' $python @('manage.py', 'check')
    Invoke-Stage 'Translations' $python @('scripts/compile_translations.py')
    Invoke-Stage 'Vite production build' $bun @('run', '--bun', 'build')
    Invoke-Stage 'Static collection' $python @('manage.py', 'collectstatic', '--noinput', '--clear', '--verbosity', '0')
    Invoke-Stage 'Django tests' $python @('manage.py', 'test')

    if (Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue) {
        throw "Port $Port is already in use. Choose another port with -Port."
    }
    New-Item -ItemType Directory -Path verification -Force | Out-Null
    $server = Start-Process -FilePath $python -ArgumentList @('manage.py', 'runserver', "127.0.0.1:$Port", '--noreload') -WorkingDirectory $root -WindowStyle Hidden -PassThru -RedirectStandardOutput verification/server.out.log -RedirectStandardError verification/server.err.log
    $ready = $false
    for ($attempt = 0; $attempt -lt 40; $attempt++) {
        if ($server.HasExited) { throw "Verification server exited. See verification/server.err.log." }
        try {
            $response = Invoke-WebRequest -UseBasicParsing -Uri $env:ATLAS_BASE_URL -TimeoutSec 2
            $ready = $response.StatusCode -eq 200
        } catch {
            Start-Sleep -Milliseconds 250
        }
        if ($ready) { break }
    }
    if (-not $ready) { throw 'Verification server did not respond successfully. See verification/server.err.log.' }
    Invoke-Stage 'Browser acceptance tests' $bun @('run', '--bun', 'test:browser')
    Write-Host "`nAll automated verification stages passed."
} finally {
    if ($server -and -not $server.HasExited) { & taskkill.exe /PID $server.Id /T /F | Out-Null }
    $env:ATLAS_DEBUG = $previousDebug
    $env:ATLAS_BASE_URL = $previousOrigin
    Pop-Location
}
