@echo off
echo Восстановление всех файлов проекта...

"C:\Program Files\Git\bin\git.exe" checkout Actual_BD_Scheme
"C:\Program Files\Git\bin\git.exe" checkout main -- app.py database.py requirements.txt manage_db.py run_tests.py pytest.ini
"C:\Program Files\Git\bin\git.exe" checkout main -- Dockerfile docker-compose.yml nginx.conf env.example
"C:\Program Files\Git\bin\git.exe" checkout main -- .dockerignore .gitignore
"C:\Program Files\Git\bin\git.exe" checkout main -- DATABASE_SCHEMA.md DATABASE_TROUBLESHOOTING.md
"C:\Program Files\Git\bin\git.exe" checkout main -- DOCKER_GUIDE.md DOCKER_README.md QUICK_START.md docker-commands.md
"C:\Program Files\Git\bin\git.exe" checkout main -- static templates tests

echo.
echo Добавление файлов...
"C:\Program Files\Git\bin\git.exe" add .

echo.
echo Создание коммита...
"C:\Program Files\Git\bin\git.exe" commit -m "Восстановление всех файлов проекта и добавление схемы БД"

echo.
echo Отправка в GitHub...
"C:\Program Files\Git\bin\git.exe" push origin Actual_BD_Scheme

echo.
echo Готово!
pause

