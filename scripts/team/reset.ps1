# Reset the local Horilla test database to a known state.
# Stop the dev server first (Windows keeps the SQLite file locked while it runs).
#
# Usage (from anywhere):
#   powershell -ExecutionPolicy Bypass -File scripts\team\reset.ps1            # fast: restore snapshot (builds it if missing)
#   powershell -ExecutionPolicy Bypass -File scripts\team\reset.ps1 -Rebuild   # slow: fresh migrate + seed, refresh snapshot
#   powershell -ExecutionPolicy Bypass -File scripts\team\reset.ps1 -Rebuild -Demo   # also load Horilla's synthetic demo data
#
# A fresh `migrate` takes 10+ minutes (hundreds of migrations), so the first
# build is saved to tests/team/.baseline.sqlite3 (git-ignored) and later resets
# just copy it back. Rebuild after pulling new migrations or changing the seed.
param([switch]$Rebuild, [switch]$Demo)
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..\..")
$py = ".\.venv\Scripts\python.exe"
$db = "TestDB.sqlite3"
$snapshot = "tests\team\.baseline.sqlite3"

# Horilla runs SQLite in WAL mode (horilla/settings/base.py), so the database
# has -wal/-shm side files. They must go with the old database: a stale WAL
# replayed onto the restored snapshot corrupts it ("database disk image is
# malformed").
function Remove-Database {
    foreach ($f in @($db, "$db-wal", "$db-shm", "$db-journal")) {
        if (Test-Path $f) { Remove-Item $f -Force }
    }
}

if ((Test-Path $snapshot) -and -not $Rebuild) {
    Remove-Database
    Copy-Item $snapshot $db -Force
    Write-Host "Reset complete (restored snapshot)."
    exit 0
}

Remove-Database
& $py manage.py migrate --no-input
if ($LASTEXITCODE -ne 0) { throw "migrate failed" }

if ($Demo) {
    & $py manage.py load_demo_data --flush --no-input
    if ($LASTEXITCODE -ne 0) { throw "load_demo_data failed" }
}

& $py manage.py shell -c "exec(open('scripts/team/seed_team.py', encoding='utf-8').read())"
if ($LASTEXITCODE -ne 0) { throw "team seed failed" }

# Fold the WAL into the main file so the snapshot is complete on its own.
& $py -c "import sqlite3; c = sqlite3.connect('$db'); c.execute('PRAGMA wal_checkpoint(TRUNCATE)'); c.close()"
Copy-Item $db $snapshot -Force
Write-Host "Reset complete (rebuilt; snapshot saved to $snapshot)."
