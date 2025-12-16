# Скрипт для восстановления всех файлов проекта из ветки main

$gitPath = "C:\Program Files\Git\bin\git.exe"

Write-Host "Восстановление всех файлов из ветки main..." -ForegroundColor Cyan

# Восстанавливаем все файлы из main
& $gitPath checkout main -- .

Write-Host "`nПроверка восстановленных файлов..." -ForegroundColor Cyan
& $gitPath status --short

Write-Host "`n✅ Файлы восстановлены!" -ForegroundColor Green

