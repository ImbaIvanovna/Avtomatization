CREATE TABLE cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            record_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (record_id) REFERENCES records (id)
        )


CREATE TABLE companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT,
            phone TEXT,
            email TEXT,
            is_wholesaler BOOLEAN DEFAULT 0
        )

CREATE TABLE compositions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            composer_id INTEGER,
            genre TEXT,
            year_composed INTEGER,
            duration_minutes INTEGER,
            FOREIGN KEY (composer_id) REFERENCES musicians (id)
        )

CREATE TABLE ensemble_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ensemble_id INTEGER NOT NULL,
            musician_id INTEGER NOT NULL,
            role_in_ensemble TEXT, 
            joined_year INTEGER,
            FOREIGN KEY (ensemble_id) REFERENCES ensembles (id),
            FOREIGN KEY (musician_id) REFERENCES musicians (id)
        )


CREATE TABLE ensembles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL, 
            founded_year INTEGER,
            country TEXT,
            description TEXT
        )


CREATE TABLE musicians (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,  
            instruments TEXT,   
            birth_year INTEGER,
            country TEXT
        )

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

CREATE TABLE record_tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_id INTEGER NOT NULL,
            performance_id INTEGER NOT NULL,
            track_number INTEGER,
            FOREIGN KEY (record_id) REFERENCES records (id),
            FOREIGN KEY (performance_id) REFERENCES performances (id)
        )


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


CREATE TABLE sqlite_sequence(name,seq)


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
