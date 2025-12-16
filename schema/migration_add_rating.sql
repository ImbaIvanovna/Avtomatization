-- Миграция: добавление поля rating в таблицу records
-- Дата: 2025-12-16

-- Добавляем поле rating в таблицу records
ALTER TABLE records ADD COLUMN rating DECIMAL(3,2) DEFAULT NULL;

