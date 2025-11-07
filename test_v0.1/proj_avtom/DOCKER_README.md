# Docker Setup для Музыкального Магазина

Этот проект настроен для работы в Docker контейнерах с поддержкой как production, так и development окружений.

## Быстрый старт

### 1. Production режим
```bash
# Сборка и запуск
docker-compose up --build

# Приложение будет доступно по адресу: http://localhost:5000
```

### 2. Development режим (с hot reload)
```bash
# Запуск с автоматической перезагрузкой при изменении файлов
docker-compose -f docker-compose.dev.yml up --build

# Приложение будет доступно по адресу: http://localhost:5000
```

## Структура Docker файлов

- `Dockerfile` - основной образ приложения
- `docker-compose.yml` - production конфигурация
- `docker-compose.dev.yml` - development конфигурация с hot reload
- `.dockerignore` - файлы, игнорируемые при сборке
- `docker-commands.md` - полный список Docker команд

## Особенности

### База данных
- SQLite база данных сохраняется в директории `./data/` на хосте
- Данные сохраняются между перезапусками контейнера
- База данных автоматически инициализируется при первом запуске

### Переменные окружения
- `SECRET_KEY` - секретный ключ Flask (по умолчанию: 'your-secret-key-here')
- `DATABASE_PATH` - путь к файлу базы данных (по умолчанию: '/app/data/music_store.db')
- `FLASK_ENV` - окружение Flask ('production' или 'development')

### Volumes
- `./data:/app/data` - персистентное хранение базы данных
- `./static:/app/static` - статические файлы (в production)
- `./templates:/app/templates` - шаблоны (в production)
- `.:/app` - весь проект (только в development режиме)

## Управление

### Остановка
```bash
docker-compose down
```

### Просмотр логов
```bash
docker-compose logs -f
```

### Перезапуск
```bash
docker-compose restart
```

### Доступ к контейнеру
```bash
docker-compose exec web bash
```

## Безопасность

⚠️ **Важно для production:**
1. Измените `SECRET_KEY` в переменных окружения
2. Используйте HTTPS в production
3. Настройте firewall для порта 5000
4. Регулярно обновляйте базовый образ Python

## Troubleshooting

### Проблемы с портами
Если порт 5000 занят, измените в docker-compose.yml:
```yaml
ports:
  - "8080:5000"  # Использовать порт 8080 вместо 5000
```

### Проблемы с базой данных
```bash
# Пересоздать базу данных
docker-compose down
rm -rf data/
docker-compose up --build
```

### Проблемы с правами доступа
```bash
# На Linux/Mac может потребоваться изменить права
sudo chown -R $USER:$USER data/
```
