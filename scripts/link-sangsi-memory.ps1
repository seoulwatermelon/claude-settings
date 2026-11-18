# link-sangsi-memory.ps1
#
# 현재(또는 지정한) 폴더의 Claude Code 프로젝트 키를 계산해서,
# 그 키의 memory 를 E:\SANGSI 의 메모리로 junction 연결한다.
#
# 폴더 이름을 바꾸거나 새 업무 폴더를 만든 뒤 한 번 실행하면 된다.
# junction 이므로 사본이 갈라지지 않는다(실체는 E--SANGSI\memory 한 곳).
#
#   powershell -ExecutionPolicy Bypass -File link-sangsi-memory.ps1
#   powershell -ExecutionPolicy Bypass -File link-sangsi-memory.ps1 "E:\SANGSI\무용학과"

param([string]$Path = (Get-Location).Path)

$ErrorActionPreference = 'Stop'
$projects = Join-Path $env:USERPROFILE '.claude\projects'
$master   = Join-Path $projects 'E--SANGSI\memory'

if (-not (Test-Path $master)) {
    Write-Error "메모리 실체가 없습니다: $master"
    exit 1
}

# Claude Code 의 키 규칙: 영숫자만 남기고 나머지(: \ 공백 한글 등)는 모두 '-'
function Get-ProjectKey([string]$p) {
    $full = (Resolve-Path -LiteralPath $p).Path.TrimEnd('\')
    -join ($full.ToCharArray() | ForEach-Object {
        if ($_ -match '[A-Za-z0-9]') { $_ } else { '-' }
    })
}

$key     = Get-ProjectKey $Path
$keyDir  = Join-Path $projects $key
$linkDir = Join-Path $keyDir 'memory'

Write-Output "대상 폴더 : $Path"
Write-Output "프로젝트 키: $key"

if ($key -eq 'E--SANGSI') {
    Write-Output "→ 루트 자체입니다. 연결 필요 없음."
    exit 0
}

New-Item -ItemType Directory -Force -Path $keyDir | Out-Null

if (Test-Path $linkDir) {
    $item = Get-Item $linkDir -Force
    if ($item.LinkType -eq 'Junction') {
        Write-Output "→ 이미 연결되어 있습니다: $($item.Target)"
        exit 0
    }
    # 실제 폴더가 있으면 지우지 않고 보존한 뒤 연결
    $bk = "$linkDir`_backup_" + (Get-Date -Format 'yyyyMMdd_HHmmss')
    Move-Item -LiteralPath $linkDir -Destination $bk
    Write-Output "→ 기존 memory 폴더를 보존했습니다: $bk"
}

cmd /c mklink /J "$linkDir" "$master" | Out-Null
$item = Get-Item $linkDir -Force
Write-Output "→ 연결 완료: $linkDir  ->  $($item.Target)"
Write-Output ("→ 보이는 메모리 " + (Get-ChildItem $linkDir -File | Measure-Object).Count + "개")
