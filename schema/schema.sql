
-- Дата выгрузки: 16.12.2025

-- Таблица: cart
CREATE TABLE cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            record_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (record_id) REFERENCES records (id)
        )

-- Таблица: companies
CREATE TABLE companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT,
            phone TEXT,
            email TEXT,
            is_wholesaler BOOLEAN DEFAULT 0
        )

-- Таблица: compositions
CREATE TABLE compositions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            composer_id INTEGER,
            genre TEXT,
            year_composed INTEGER,
            duration_minutes INTEGER,
            FOREIGN KEY (composer_id) REFERENCES musicians (id)
        )

-- Таблица: ensemble_members
CREATE TABLE ensemble_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ensemble_id INTEGER NOT NULL,
            musician_id INTEGER NOT NULL,
            role_in_ensemble TEXT,  -- роль в ансамбле
            joined_year INTEGER,
            FOREIGN KEY (ensemble_id) REFERENCES ensembles (id),
            FOREIGN KEY (musician_id) REFERENCES musicians (id)
        )

-- Таблица: ensembles
CREATE TABLE ensembles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,  -- оркестр, джазовая группа, квартет, квинтет и т.д.
            founded_year INTEGER,
            country TEXT,
            description TEXT
        )

-- Таблица: musicians
CREATE TABLE musicians (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,  -- исполнитель, композитор, дирижер, руководитель
            instruments TEXT,    -- инструменты для исполнителей
            birth_year INTEGER,
            country TEXT
        )

-- Таблица: performances
CREATE TABLE performances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            composition_id INTEGER NOT NULL,
            ensemble_id INTEGER NOT NULL,
            conductor_id INTEGER,
            recording_date DATE,
            venue TEXT,
            FOREIGN KEY (composition_id) REFERENCES compositions (id),
            FOREIGN KEY (ensemble_id) REFERENCES ensembles (id),
            FOREIGN KEY (conductor_id) REFERENCES musicians (id)
        )

-- Таблица: purchases
CREATE TABLE purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            record_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            price DECIMAL(10,2) NOT NULL,
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            seller_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (record_id) REFERENCES records (id),
            FOREIGN KEY (seller_id) REFERENCES users (id)
        )

-- Таблица: record_tracks
CREATE TABLE record_tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_id INTEGER NOT NULL,
            performance_id INTEGER NOT NULL,
            track_number INTEGER,
            FOREIGN KEY (record_id) REFERENCES records (id),
            FOREIGN KEY (performance_id) REFERENCES performances (id)
        )

-- Таблица: records
CREATE TABLE records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            catalog_number TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            company_id INTEGER NOT NULL,
            release_date DATE,
            wholesale_price DECIMAL(10,2),
            retail_price DECIMAL(10,2),
            current_stock INTEGER DEFAULT 0,
            sold_last_year INTEGER DEFAULT 0,
            sold_this_year INTEGER DEFAULT 0,
            rating DECIMAL(3,2) DEFAULT NULL,
            FOREIGN KEY (company_id) REFERENCES companies (id)
        )

-- Таблица: sqlite_sequence
CREATE TABLE sqlite_sequence(name,seq)

-- Таблица: users
CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'buyer',
            full_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
