"""
Конфигурация pytest и фикстуры для тестирования Flask приложения
"""
import pytest
import os
import tempfile
import sqlite3
from app import app, get_db_connection
from database import init_database


@pytest.fixture(scope='session')
def test_db_path():
    """Создает временную базу данных для тестов"""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    # Сохраняем оригинальный путь
    original_db = os.environ.get('DATABASE_PATH')
    
    # Устанавливаем путь к тестовой БД
    os.environ['DATABASE_PATH'] = path
    
    # Инициализируем тестовую БД
    init_database(force_recreate=True)
    
    yield path
    
    # Очистка
    if os.path.exists(path):
        os.remove(path)
    
    # Восстанавливаем оригинальный путь
    if original_db:
        os.environ['DATABASE_PATH'] = original_db
    elif 'DATABASE_PATH' in os.environ:
        del os.environ['DATABASE_PATH']


@pytest.fixture
def client(test_db_path):
    """Создает тестовый клиент Flask"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        yield client


@pytest.fixture
def db_connection(test_db_path):
    """Создает соединение с тестовой БД"""
    conn = get_db_connection()
    yield conn
    conn.close()


@pytest.fixture
def auth_buyer(client):
    """Авторизует пользователя с ролью buyer"""
    # Создаем новую сессию через session_transaction
    with client.session_transaction() as sess:
        sess['user_id'] = 3  # buyer1 из тестовых данных
        sess['username'] = 'buyer1'
        sess['role'] = 'buyer'
    # Возвращаем клиент после установки сессии
    return client


@pytest.fixture
def auth_seller(client):
    """Авторизует пользователя с ролью seller"""
    with client.session_transaction() as sess:
        sess['user_id'] = 2  # seller1 из тестовых данных
        sess['username'] = 'seller1'
        sess['role'] = 'seller'
    return client


@pytest.fixture
def auth_director(client):
    """Авторизует пользователя с ролью director"""
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # admin из тестовых данных
        sess['username'] = 'admin'
        sess['role'] = 'director'
    return client

