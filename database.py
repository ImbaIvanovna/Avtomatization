import sqlite3
import os

def init_database(force_recreate=False):
    """Инициализация базы данных с созданием всех необходимых таблиц"""
    
    # Поддержка Docker - используем переменную окружения для пути к БД
    db_path = os.environ.get('DATABASE_PATH', 'music_store.db')
    
    # Создаем директорию для базы данных если её нет
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    
    # Проверяем, существует ли база данных
    if os.path.exists(db_path) and not force_recreate:
        print(f"База данных уже существует: {db_path}")
        return
    
    # Удаляем существующую базу данных только если принудительное пересоздание
    if os.path.exists(db_path) and force_recreate:
        os.remove(db_path)
        print(f"База данных пересоздается: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Таблица музыкантов
    cursor.execute('''
        CREATE TABLE musicians (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,  -- исполнитель, композитор, дирижер, руководитель
            instruments TEXT,    -- инструменты для исполнителей
            birth_year INTEGER,
            country TEXT
        )
    ''')
    
    # Таблица ансамблей
    cursor.execute('''
        CREATE TABLE ensembles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,  -- оркестр, джазовая группа, квартет, квинтет и т.д.
            founded_year INTEGER,
            country TEXT,
            description TEXT
        )
    ''')
    
    # Таблица участников ансамблей (связь многие-ко-многим)
    cursor.execute('''
        CREATE TABLE ensemble_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ensemble_id INTEGER NOT NULL,
            musician_id INTEGER NOT NULL,
            role_in_ensemble TEXT,  -- роль в ансамбле
            joined_year INTEGER,
            FOREIGN KEY (ensemble_id) REFERENCES ensembles (id),
            FOREIGN KEY (musician_id) REFERENCES musicians (id)
        )
    ''')
    
    # Таблица музыкальных произведений
    cursor.execute('''
        CREATE TABLE compositions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            composer_id INTEGER,
            genre TEXT,
            year_composed INTEGER,
            duration_minutes INTEGER,
            FOREIGN KEY (composer_id) REFERENCES musicians (id)
        )
    ''')
    
    # Таблица исполнений произведений
    cursor.execute('''
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
    ''')
    
    # Таблица компаний-производителей
    cursor.execute('''
        CREATE TABLE companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT,
            phone TEXT,
            email TEXT,
            is_wholesaler BOOLEAN DEFAULT 0
        )
    ''')
    
    # Таблица пластинок/компакт-дисков
    cursor.execute('''
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
    ''')
    
    # Таблица записей на пластинках (связь многие-ко-многим между пластинками и исполнениями)
    cursor.execute('''
        CREATE TABLE record_tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_id INTEGER NOT NULL,
            performance_id INTEGER NOT NULL,
            track_number INTEGER,
            FOREIGN KEY (record_id) REFERENCES records (id),
            FOREIGN KEY (performance_id) REFERENCES performances (id)
        )
    ''')
    
    # Таблица пользователей
    cursor.execute('''
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
    ''')
    
    # Таблица покупок
    cursor.execute('''
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
    ''')
    
    # Таблица корзины
    cursor.execute('''
        CREATE TABLE cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            record_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (record_id) REFERENCES records (id)
        )
    ''')
    
    # Вставляем тестовые данные
    insert_test_data(cursor)
    
    conn.commit()
    conn.close()
    print("База данных успешно создана!")

def insert_test_data(cursor):
    """Вставка тестовых данных в базу"""
    
    # Музыканты
    musicians_data = [
        ('Людвиг ван Бетховен', 'композитор', None, 1770, 'Германия'),
        ('Вольфганг Амадей Моцарт', 'композитор', None, 1756, 'Австрия'),
        ('Иоганн Себастьян Бах', 'композитор', None, 1685, 'Германия'),
        ('Герберт фон Караян', 'дирижер', None, 1908, 'Австрия'),
        ('Владимир Горовиц', 'исполнитель', 'фортепиано', 1903, 'Россия'),
        ('Ицхак Перлман', 'исполнитель', 'скрипка', 1945, 'Израиль'),
        ('Йо-Йо Ма', 'исполнитель', 'виолончель', 1955, 'Китай'),
        ('Майлз Дэвис', 'исполнитель', 'труба', 1926, 'США'),
        ('Джон Колтрейн', 'исполнитель', 'саксофон', 1926, 'США')
    ]
    
    cursor.executemany('''
        INSERT INTO musicians (name, role, instruments, birth_year, country)
        VALUES (?, ?, ?, ?, ?)
    ''', musicians_data)
    
    # Ансамбли
    ensembles_data = [
        ('Венский филармонический оркестр', 'оркестр', 1842, 'Австрия', 'Один из лучших оркестров мира'),
        ('Берлинский филармонический оркестр', 'оркестр', 1882, 'Германия', 'Знаменитый немецкий оркестр'),
        ('Квартет имени Бородина', 'квартет', 1945, 'Россия', 'Русский струнный квартет'),
        ('Майлз Дэвис Квинтет', 'квинтет', 1955, 'США', 'Легендарный джазовый квинтет'),
        ('Трио Оскара Питерсона', 'трио', 1953, 'Канада', 'Джазовое трио')
    ]
    
    cursor.executemany('''
        INSERT INTO ensembles (name, type, founded_year, country, description)
        VALUES (?, ?, ?, ?, ?)
    ''', ensembles_data)
    
    # Компании
    companies_data = [
        ('EMI Records', 'Лондон, Великобритания', '+44-20-7795-7000', 'info@emi.com', 1),
        ('Deutsche Grammophon', 'Гамбург, Германия', '+49-40-380-0', 'info@dg.com', 1),
        ('Sony Classical', 'Нью-Йорк, США', '+1-212-833-8000', 'info@sonyclassical.com', 1),
        ('Blue Note Records', 'Нью-Йорк, США', '+1-212-333-8000', 'info@bluenote.com', 1),
        ('Мелодия', 'Москва, Россия', '+7-495-123-4567', 'info@melody.ru', 1)
    ]
    
    cursor.executemany('''
        INSERT INTO companies (name, address, phone, email, is_wholesaler)
        VALUES (?, ?, ?, ?, ?)
    ''', companies_data)
    
    # Произведения
    compositions_data = [
        ('Симфония №9', 1, 'классическая', 1824, 65),
        ('Реквием', 2, 'классическая', 1791, 50),
        ('Бранденбургские концерты', 3, 'барокко', 1721, 20),
        ('Концерт для фортепиано №21', 2, 'классическая', 1785, 30),
        ('Kind of Blue', 8, 'джаз', 1959, 45),
        ('A Love Supreme', 9, 'джаз', 1965, 33)
    ]
    
    cursor.executemany('''
        INSERT INTO compositions (title, composer_id, genre, year_composed, duration_minutes)
        VALUES (?, ?, ?, ?, ?)
    ''', compositions_data)
    
    # Исполнения
    performances_data = [
        (1, 1, 4, '1985-01-15', 'Венская государственная опера'),
        (2, 2, 4, '1991-03-20', 'Концертный зал Берлинской филармонии'),
        (3, 1, 4, '1988-06-10', 'Золотой зал Венского музыкального общества'),
        (4, 2, 4, '1990-09-05', 'Концертный зал Берлинской филармонии'),
        (5, 4, None, '1959-03-02', 'Студия Columbia Records'),
        (6, 4, None, '1964-12-09', 'Студия Impulse! Records')
    ]
    
    cursor.executemany('''
        INSERT INTO performances (composition_id, ensemble_id, conductor_id, recording_date, venue)
        VALUES (?, ?, ?, ?, ?)
    ''', performances_data)
    
    # Пластинки
    records_data = [
        ('DG-427-123', 'Бетховен: Симфония №9', 2, '1985-06-15', 15.50, 25.99, 50, 25, 15),
        ('DG-427-124', 'Моцарт: Реквием', 2, '1991-09-20', 18.00, 29.99, 30, 20, 12),
        ('EMI-567-890', 'Бах: Бранденбургские концерты', 1, '1988-12-01', 22.00, 35.99, 25, 15, 8),
        ('EMI-567-891', 'Моцарт: Концерт для фортепиано №21', 1, '1990-11-15', 16.50, 27.99, 40, 30, 18),
        ('BN-123-456', 'Майлз Дэвис: Kind of Blue', 4, '1959-08-17', 12.00, 19.99, 100, 80, 45),
        ('IMP-789-012', 'Джон Колтрейн: A Love Supreme', 4, '1965-02-01', 14.00, 22.99, 60, 40, 25)
    ]
    
    cursor.executemany('''
        INSERT INTO records (catalog_number, title, company_id, release_date, wholesale_price, retail_price, current_stock, sold_last_year, sold_this_year)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', records_data)
    
    # Участники ансамблей
    ensemble_members_data = [
        (1, 4, 'главный дирижер', 1955),
        (2, 4, 'главный дирижер', 1989),
        (3, 5, 'первая скрипка', 1945),
        (3, 6, 'вторая скрипка', 1950),
        (4, 8, 'лидер группы', 1955),
        (4, 9, 'саксофон', 1960),
        (5, 5, 'фортепиано', 1953)
    ]
    
    cursor.executemany('''
        INSERT INTO ensemble_members (ensemble_id, musician_id, role_in_ensemble, joined_year)
        VALUES (?, ?, ?, ?)
    ''', ensemble_members_data)
    
    # Записи на пластинках
    record_tracks_data = [
        (1, 1, 1),
        (2, 2, 1),
        (3, 3, 1),
        (4, 4, 1),
        (5, 5, 1),
        (6, 6, 1)
    ]
    
    cursor.executemany('''
        INSERT INTO record_tracks (record_id, performance_id, track_number)
        VALUES (?, ?, ?)
    ''', record_tracks_data)
    
    # Пользователи (пароли: admin123, seller123, buyer123)
    from werkzeug.security import generate_password_hash
    
    users_data = [
        ('admin', generate_password_hash('admin123'), 'director', 'Иван Петрович Администратор', 'admin@musicstore.ru', '+7-495-123-4567'),
        ('seller1', generate_password_hash('seller123'), 'seller', 'Анна Сергеевна Продавец', 'seller@musicstore.ru', '+7-495-123-4568'),
        ('buyer1', generate_password_hash('buyer123'), 'buyer', 'Михаил Иванович Покупатель', 'buyer@musicstore.ru', '+7-495-123-4569')
    ]
    
    cursor.executemany('''
        INSERT INTO users (username, password_hash, role, full_name, email, phone)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', users_data)

if __name__ == '__main__':
    init_database()
