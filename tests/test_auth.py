"""
Юнит-тесты для аутентификации (login, logout, register)
"""
import pytest
from werkzeug.security import generate_password_hash
from app import get_db_connection


class TestLogin:
    """Тесты для функции входа в систему"""
    
    def test_login_page_get(self, client):
        """Тест: получение страницы входа"""
        response = client.get('/login')
        assert response.status_code == 200
        assert 'Вход'.encode('utf-8') in response.data or b'login' in response.data.lower()
    
    def test_login_success(self, client, db_connection):
        """Тест: успешный вход с правильными credentials"""
        response = client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Проверяем, что пользователь перенаправлен
        assert 'Музыкальный магазин'.encode('utf-8') in response.data or b'music' in response.data.lower()
        
        # Проверяем сессию
        with client.session_transaction() as sess:
            assert 'user_id' in sess
            assert sess['username'] == 'admin'
            assert sess['role'] == 'director'
    
    def test_login_wrong_password(self, client):
        """Тест: вход с неверным паролем"""
        response = client.post('/login', data={
            'username': 'admin',
            'password': 'wrong_password'
        })
        
        assert response.status_code == 200
        # Проверяем сообщение об ошибке
        assert 'Неверное имя пользователя или пароль'.encode('utf-8') in response.data
        
        # Проверяем, что сессия не создана
        with client.session_transaction() as sess:
            assert 'user_id' not in sess
    
    def test_login_nonexistent_user(self, client):
        """Тест: вход несуществующего пользователя"""
        response = client.post('/login', data={
            'username': 'nonexistent',
            'password': 'password123'
        })
        
        assert response.status_code == 200
        assert 'Неверное имя пользователя или пароль'.encode('utf-8') in response.data
    
    def test_login_inactive_user(self, client, db_connection):
        """Тест: вход неактивного пользователя"""
        import time
        # Создаем неактивного пользователя с уникальным именем
        conn = db_connection
        password_hash = generate_password_hash('test123')
        unique_username = f'inactive_user_{int(time.time() * 1000)}'
        
        try:
            conn.execute('''
                INSERT INTO users (username, password_hash, role, full_name, is_active)
                VALUES (?, ?, 'buyer', 'Test User', 0)
            ''', (unique_username, password_hash))
            conn.commit()
            
            response = client.post('/login', data={
                'username': unique_username,
                'password': 'test123'
            })
            
            assert response.status_code == 200
            response_text = response.data.decode('utf-8')
            assert 'Неверное имя пользователя или пароль' in response_text
        finally:
            # Очищаем тестовые данные
            conn.execute('DELETE FROM users WHERE username = ?', (unique_username,))
            conn.commit()


class TestLogout:
    """Тесты для функции выхода из системы"""
    
    def test_logout_authenticated(self, auth_buyer):
        """Тест: выход авторизованного пользователя"""
        # Проверяем, что пользователь авторизован
        with auth_buyer.session_transaction() as sess:
            assert 'user_id' in sess
        
        response = auth_buyer.get('/logout', follow_redirects=True)
        
        assert response.status_code == 200
        # Проверяем, что сессия очищена
        with auth_buyer.session_transaction() as sess:
            assert 'user_id' not in sess
    
    def test_logout_unauthenticated(self, client):
        """Тест: выход неавторизованного пользователя"""
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200


class TestRegister:
    """Тесты для функции регистрации"""
    
    def test_register_page_get(self, client):
        """Тест: получение страницы регистрации"""
        response = client.get('/register')
        assert response.status_code == 200
        assert 'Регистрация'.encode('utf-8') in response.data or b'register' in response.data.lower()
    
    def test_register_success(self, client, db_connection):
        """Тест: успешная регистрация нового пользователя"""
        import time
        unique_username = f'newuser_{int(time.time() * 1000)}'
        
        try:
            response = client.post('/register', data={
                'username': unique_username,
                'password': 'password123',
                'full_name': 'Новый Пользователь',
                'email': f'{unique_username}@test.com',
                'phone': '+7-999-123-4567'
            }, follow_redirects=True)
            
            assert response.status_code == 200
            response_text = response.data.decode('utf-8')
            assert 'Регистрация прошла успешно' in response_text or 'успешно' in response_text.lower()
            
            # Проверяем, что пользователь создан в БД
            conn = db_connection
            user = conn.execute('SELECT * FROM users WHERE username = ?', (unique_username,)).fetchone()
            assert user is not None
            assert user['role'] == 'buyer'
            assert user['full_name'] == 'Новый Пользователь'
        finally:
            # Очищаем тестовые данные
            conn = db_connection
            conn.execute('DELETE FROM users WHERE username = ?', (unique_username,))
            conn.commit()
    
    def test_register_duplicate_username(self, client):
        """Тест: регистрация с существующим именем пользователя"""
        response = client.post('/register', data={
            'username': 'admin',  # Уже существует в тестовых данных
            'password': 'password123',
            'full_name': 'Другой Пользователь'
        })
        
        assert response.status_code == 200
        assert 'уже существует'.encode('utf-8') in response.data.lower() or 'существует'.encode('utf-8') in response.data
    
    def test_register_minimal_data(self, client, db_connection):
        """Тест: регистрация с минимальными данными (без email и phone)"""
        response = client.post('/register', data={
            'username': 'minimaluser',
            'password': 'password123',
            'full_name': 'Минимальный Пользователь'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        # Проверяем, что пользователь создан
        conn = db_connection
        user = conn.execute('SELECT * FROM users WHERE username = ?', ('minimaluser',)).fetchone()
        assert user is not None

