# Docker Commands для музыкального магазина

## Основные команды

### Запуск в production режиме
```bash
# Сборка и запуск
docker-compose up --build

# Запуск в фоне
docker-compose up -d --build

# Остановка
docker-compose down
```

### Запуск в development режиме
```bash
# С hot reload (автоматическая перезагрузка при изменении файлов)
docker-compose -f docker-compose.dev.yml up --build

# В фоне
docker-compose -f docker-compose.dev.yml up -d --build
```

### Управление контейнерами
```bash
# Просмотр логов
docker-compose logs -f

# Просмотр статуса
docker-compose ps

# Перезапуск сервиса
docker-compose restart web

# Выполнение команд в контейнере
docker-compose exec web bash
```

### Работа с базой данных
```bash
# Инициализация базы данных
docker-compose exec web python database.py

# Просмотр базы данных
docker-compose exec web sqlite3 data/music_store.db
```

### Очистка
```bash
# Остановка и удаление контейнеров
docker-compose down

# Удаление образов
docker-compose down --rmi all

# Удаление volumes
docker-compose down -v

# Полная очистка
docker system prune -a
```

## Доступ к приложению

После запуска приложение будет доступно по адресу:
- Production: http://localhost:5000
- Development: http://localhost:5000

## Структура данных

База данных сохраняется в директории `./data/` на хосте, что позволяет сохранять данные между перезапусками контейнера.



