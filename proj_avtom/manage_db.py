#!/usr/bin/env python3
"""
Скрипт для управления базой данных музыкального магазина
"""

import sys
import os
from database import init_database

def main():
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python manage_db.py init     - создать базу данных (если не существует)")
        print("  python manage_db.py recreate - пересоздать базу данных (удалить все данные)")
        print("  python manage_db.py status   - проверить статус базы данных")
        return
    
    command = sys.argv[1]
    db_path = os.environ.get('DATABASE_PATH', 'music_store.db')
    
    if command == "init":
        print("Инициализация базы данных...")
        init_database(force_recreate=False)
        print("✅ База данных готова к работе")
        
    elif command == "recreate":
        print("⚠️  ВНИМАНИЕ: Это удалит все данные!")
        confirm = input("Вы уверены? Введите 'yes' для подтверждения: ")
        if confirm.lower() == 'yes':
            print("Пересоздание базы данных...")
            init_database(force_recreate=True)
            print("✅ База данных пересоздана")
        else:
            print("❌ Операция отменена")
            
    elif command == "status":
        if os.path.exists(db_path):
            size = os.path.getsize(db_path)
            print(f"✅ База данных существует: {db_path}")
            print(f"📊 Размер: {size} байт")
        else:
            print(f"❌ База данных не найдена: {db_path}")
            
    else:
        print(f"❌ Неизвестная команда: {command}")
        print("Доступные команды: init, recreate, status")

if __name__ == "__main__":
    main()



