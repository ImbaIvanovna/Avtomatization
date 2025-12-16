# Восстановление всех файлов проекта из ветки main

$ErrorActionPreference = "Continue"

Write-Host "=== ВОССТАНОВЛЕНИЕ ВСЕХ ФАЙЛОВ ПРОЕКТА ===" -ForegroundColor Green
Write-Host ""

# Убеждаемся, что мы на правильной ветке
Write-Host "1. Переключение на ветку Actual_BD_Scheme..." -ForegroundColor Yellow
& "C:\Program Files\Git\bin\git.exe" checkout Actual_BD_Scheme 2>&1 | Out-Null

Write-Host "2. Восстановление ВСЕХ файлов из ветки main..." -ForegroundColor Yellow
& "C:\Program Files\Git\bin\git.exe" checkout main -- . 2>&1

Write-Host ""
Write-Host "3. Проверка восстановленных файлов..." -ForegroundColor Yellow
$status = & "C:\Program Files\Git\bin\git.exe" status --short
Write-Host $status

Write-Host ""
Write-Host "4. Добавление всех файлов..." -ForegroundColor Yellow
& "C:\Program Files\Git\bin\git.exe" add . 2>&1

Write-Host ""
Write-Host "5. Создание коммита..." -ForegroundColor Yellow
$msg = "Восстановление всех файлов проекта из main и добавление схемы БД с полем rating"
& "C:\Program Files\Git\bin\git.exe" commit -m $msg 2>&1

Write-Host ""
Write-Host "6. Отправка в GitHub..." -ForegroundColor Yellow
& "C:\Program Files\Git\bin\git.exe" push origin Actual_BD_Scheme 2>&1

Write-Host ""
Write-Host "=== ГОТОВО! ===" -ForegroundColor Green

