#!/usr/bin/env python3
"""
Скрипт для коммита изменений через Python
Пытается найти git и выполнить коммит
"""

import os
import subprocess
import sys
from pathlib import Path

def find_git():
    """Поиск исполняемого файла git"""
    # Стандартные пути установки git на Windows
    possible_paths = [
        r"C:\Program Files\Git\bin\git.exe",
        r"C:\Program Files (x86)\Git\bin\git.exe",
        r"C:\Program Files\Git\cmd\git.exe",
        os.path.expanduser(r"~\AppData\Local\Programs\Git\bin\git.exe"),
    ]
    
    # Проверяем PATH
    for path_dir in os.environ.get('PATH', '').split(os.pathsep):
        git_path = os.path.join(path_dir, 'git.exe')
        if os.path.exists(git_path):
            return git_path
    
    # Проверяем стандартные пути
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def run_git_command(git_exe, *args):
    """Выполнение команды git"""
    try:
        cmd = [git_exe] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    git_exe = find_git()
    
    if not git_exe:
        print("❌ Git не найден в системе")
        print("\nПожалуйста, установите Git или используйте скрипт commit_changes.ps1")
        print("Скачать Git: https://git-scm.com/download/win")
        print("\nАльтернативно, выполните команды вручную:")
        print("  git init")
        print('  git config user.name "1Usinglable1"')
        print('  git config user.email "ilya.razumov20022711@yandex.ru"')
        print("  git add .")
        print('  git commit -m "Добавлено поле rating в таблицу records и выгружена актуальная схема БД"')
        return 1
    
    print(f"✅ Найден git: {git_exe}")
    print("\nИнициализация репозитория...")
    
    # Инициализация
    success, stdout, stderr = run_git_command(git_exe, "init")
    if not success and "already a git repository" not in stderr.lower():
        print(f"⚠️  Предупреждение: {stderr}")
    
    # Настройка пользователя
    print("Настройка git config...")
    run_git_command(git_exe, "config", "user.name", "1Usinglable1")
    run_git_command(git_exe, "config", "user.email", "ilya.razumov20022711@yandex.ru")
    
    # Добавление файлов
    print("Добавление файлов...")
    success, stdout, stderr = run_git_command(git_exe, "add", ".")
    if not success:
        print(f"❌ Ошибка при добавлении файлов: {stderr}")
        return 1
    
    # Коммит
    print("Создание коммита...")
    commit_message = """Добавлено поле rating в таблицу records и выгружена актуальная схема БД

- Добавлено поле rating DECIMAL(3,2) в таблицу records
- Создана миграция migration_add_rating.sql
- Выгружена актуальная схема БД в schema/schema.sql
- Создан скрипт export_schema.py для выгрузки схемы"""
    
    success, stdout, stderr = run_git_command(
        git_exe, "commit", "-m", commit_message
    )
    
    if success:
        print("✅ Коммит создан успешно!")
        print("\nДля просмотра истории:")
        print("  git log")
        return 0
    else:
        if "nothing to commit" in stderr.lower():
            print("ℹ️  Нет изменений для коммита")
        else:
            print(f"❌ Ошибка при создании коммита: {stderr}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

