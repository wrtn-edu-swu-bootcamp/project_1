# GitHub 저장소 연동 스크립트

Write-Host "GitHub 저장소 연동을 시작합니다..." -ForegroundColor Green

# Git이 설치되어 있는지 확인
try {
    $gitVersion = git --version
    Write-Host "Git이 설치되어 있습니다: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "오류: Git이 설치되어 있지 않습니다." -ForegroundColor Red
    Write-Host "Git을 설치해주세요: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# 현재 디렉토리로 이동
Set-Location $PSScriptRoot

# Git 저장소 초기화 (이미 초기화되어 있지 않다면)
if (-not (Test-Path .git)) {
    Write-Host "Git 저장소를 초기화합니다..." -ForegroundColor Yellow
    git init
}

# 원격 저장소 확인 및 추가
$remoteExists = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "원격 저장소를 추가합니다..." -ForegroundColor Yellow
    git remote add origin https://github.com/wrtn-edu-swu-bootcamp/project_48.git
} else {
    Write-Host "원격 저장소가 이미 설정되어 있습니다: $remoteExists" -ForegroundColor Yellow
    Write-Host "원격 저장소를 업데이트합니다..." -ForegroundColor Yellow
    git remote set-url origin https://github.com/wrtn-edu-swu-bootcamp/project_48.git
}

# 파일 추가
Write-Host "변경사항을 스테이징합니다..." -ForegroundColor Yellow
git add .

# 커밋 (변경사항이 있는 경우)
$status = git status --porcelain
if ($status) {
    Write-Host "커밋을 생성합니다..." -ForegroundColor Yellow
    git commit -m "Initial commit"
} else {
    Write-Host "커밋할 변경사항이 없습니다." -ForegroundColor Yellow
}

# 브랜치를 main으로 설정
git branch -M main

Write-Host "`n연동이 완료되었습니다!" -ForegroundColor Green
Write-Host "원격 저장소로 푸시하려면 다음 명령어를 실행하세요:" -ForegroundColor Yellow
Write-Host "  git push -u origin main" -ForegroundColor Cyan
