# Скрипт для восстановления всех файлов и отправки в ветку Actual_BD_Scheme

$gitPath = "C:\Program Files\Git\bin\git.exe"

Write-Host "=== Восстановление всех файлов проекта ===" -ForegroundColor Cyan

# Переключаемся на ветку Actual_BD_Scheme
Write-Host "`nПереключение на ветку Actual_BD_Scheme..." -ForegroundColor Yellow
& $gitPath checkout Actual_BD_Scheme

# Восстанавливаем все файлы из ветки main
Write-Host "`nВосстановление всех файлов из ветки main..." -ForegroundColor Yellow
& $gitPath checkout main -- app.py database.py requirements.txt manage_db.py run_tests.py pytest.ini
& $gitPath checkout main -- Dockerfile docker-compose.yml nginx.conf env.example
& $gitPath checkout main -- .dockerignore .gitignore
& $gitPath checkout main -- DATABASE_SCHEMA.md DATABASE_TROUBLESHOOTING.md
& $gitPath checkout main -- DOCKER_GUIDE.md DOCKER_README.md QUICK_START.md
& $gitPath checkout main -- docker-commands.md
& $gitPath checkout main -- static/ templates/ tests/

Write-Host "`nПроверка восстановленных файлов..." -ForegroundColor Yellow
& $gitPath status --short

Write-Host "`nДобавление всех файлов..." -ForegroundColor Yellow
& $gitPath add .

Write-Host "`nСоздание коммита..." -ForegroundColor Yellow
$commitMessage = @"
Восстановление всех файлов проекта и добавление схемы БД

- Восстановлены все файлы проекта из ветки main
- Добавлено поле rating DECIMAL(3,2) в таблицу records
- Создана миграция migration_add_rating.sql
- Выгружена актуальная схема БД в schema/schema.sql
- Создан скрипт export_schema.py для выгрузки схемы
"@

& $gitPath commit -m $commitMessage

Write-Host "`nОтправка в ветку Actual_BD_Scheme..." -ForegroundColor Yellow
& $gitPath push origin Actual_BD_Scheme

Write-Host "`n✅ Все файлы восстановлены и отправлены в GitHub!" -ForegroundColor Green

