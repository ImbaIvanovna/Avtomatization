# Скрипт для переноса изменений в ветку Actual_BD_Scheme

$gitPath = "C:\Program Files\Git\bin\git.exe"

Write-Host "Проверка текущей ветки..." -ForegroundColor Cyan
& $gitPath branch --show-current

Write-Host "`nДобавление всех изменений..." -ForegroundColor Cyan
& $gitPath add .

Write-Host "`nПроверка статуса..." -ForegroundColor Cyan
& $gitPath status --short

Write-Host "`nСоздание коммита..." -ForegroundColor Cyan
$commitMessage = @"
Добавлено поле rating в таблицу records и выгружена актуальная схема БД

- Добавлено поле rating DECIMAL(3,2) в таблицу records
- Создана миграция migration_add_rating.sql
- Выгружена актуальная схема БД в schema/schema.sql
- Создан скрипт export_schema.py для выгрузки схемы
"@

& $gitPath commit -m $commitMessage

Write-Host "`nОтправка в ветку Actual_BD_Scheme..." -ForegroundColor Cyan
& $gitPath push origin Actual_BD_Scheme

Write-Host "`n✅ Готово!" -ForegroundColor Green

