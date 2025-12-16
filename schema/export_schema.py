#!/usr/bin/env python3
"""
Скрипт для выгрузки схемы базы данных SQLite
"""

import sqlite3
import os
import sys

def apply_migration(db_path):
    """Применение миграции для добавления поля rating"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Проверяем, существует ли уже поле rating
        cursor.execute("PRAGMA table_info(records)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'rating' not in columns:
            print("Применение миграции: добавление поля rating...")
            cursor.execute("ALTER TABLE records ADD COLUMN rating DECIMAL(3,2) DEFAULT NULL")
            conn.commit()
            print("✅ Миграция применена успешно")
        else:
            print("ℹ️  Поле rating уже существует")
        
        conn.close()
    except Exception as e:
        print(f"❌ Ошибка при применении миграции: {e}")
        sys.exit(1)

def export_schema(db_path, output_file):
    """Выгрузка схемы базы данных"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Получаем список всех таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        schema_lines = []
        schema_lines.append("-- Схема базы данных музыкального магазина")
        schema_lines.append(f"-- Дата выгрузки: {os.popen('date /t').read().strip() if os.name == 'nt' else os.popen('date').read().strip()}")
        schema_lines.append("")
        
        # Для каждой таблицы получаем CREATE TABLE statement
        for (table_name,) in tables:
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            result = cursor.fetchone()
            if result and result[0]:
                schema_lines.append(f"-- Таблица: {table_name}")
                schema_lines.append(result[0])
                schema_lines.append("")
        
        # Получаем индексы
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='index' AND sql IS NOT NULL")
        indexes = cursor.fetchall()
        if indexes:
            schema_lines.append("-- Индексы")
            for (index_sql,) in indexes:
                schema_lines.append(index_sql)
                schema_lines.append("")
        
        conn.close()
        
        # Сохраняем схему в файл
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(schema_lines))
        
        print(f"✅ Схема выгружена в файл: {output_file}")
        
    except Exception as e:
        print(f"❌ Ошибка при выгрузке схемы: {e}")
        sys.exit(1)

if __name__ == "__main__":
    db_path = os.environ.get('DATABASE_PATH', 'data/music_store.db')
    
    if not os.path.exists(db_path):
        print(f"❌ База данных не найдена: {db_path}")
        sys.exit(1)
    
    # Применяем миграцию
    apply_migration(db_path)
    
    # Выгружаем схему
    output_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
    export_schema(db_path, output_file)

