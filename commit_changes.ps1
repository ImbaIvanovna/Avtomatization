# Скрипт для коммита изменений в git
# Запустите этот скрипт после настройки git

Write-Host "Инициализация git репозитория..." -ForegroundColor Cyan

# Инициализация репозитория
git init

# Настройка git config
Write-Host "Настройка git config..." -ForegroundColor Cyan
git config user.name "1Usinglable1"
git config user.email "ilya.razumov20022711@yandex.ru"

# Добавление всех файлов
Write-Host "Добавление файлов в staging area..." -ForegroundColor Cyan
git add .

# Создание коммита
Write-Host "Создание коммита..." -ForegroundColor Cyan
git commit -m "Добавлено поле rating в таблицу records и выгружена актуальная схема БД

- Добавлено поле rating DECIMAL(3,2) в таблицу records
- Создана миграция migration_add_rating.sql
- Выгружена актуальная схема БД в schema/schema.sql
- Создан скрипт export_schema.py для выгрузки схемы"

Write-Host "`n✅ Коммит создан успешно!" -ForegroundColor Green
Write-Host "`nДля просмотра истории коммитов используйте: git log" -ForegroundColor Yellow

