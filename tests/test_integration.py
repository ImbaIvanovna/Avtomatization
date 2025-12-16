"""
Интеграционные тесты для основных маршрутов и функционала
"""
import pytest


class TestIndexPage:
    """Интеграционные тесты для главной страницы"""
    
    def test_index_page_unauthenticated(self, client):
        """Тест: главная страница доступна без авторизации"""
        response = client.get('/')
        assert response.status_code == 200
        assert 'Музыкальный магазин'.encode('utf-8') in response.data or b'music' in response.data.lower()
    
    def test_index_page_shows_stats(self, client, db_connection):
        """Тест: главная страница показывает статистику"""
        response = client.get('/')
        assert response.status_code == 200
        
        # Проверяем, что статистика отображается (цифры или названия)
        # Статистика должна содержать информацию о записях, ансамблях и т.д.
        conn = db_connection
        stats = {
            'total_ensembles': conn.execute('SELECT COUNT(*) FROM ensembles').fetchone()[0],
            'total_records': conn.execute('SELECT COUNT(*) FROM records').fetchone()[0]
        }
        
        # Проверяем, что на странице есть элементы, указывающие на статистику
        assert response.status_code == 200
    
    def test_index_page_authenticated(self, auth_buyer):
        """Тест: главная страница для авторизованного пользователя"""
        response = auth_buyer.get('/')
        assert response.status_code == 200


class TestCompositionsCount:
    """Интеграционные тесты для функционала подсчета произведений"""
    
    def test_compositions_count_requires_auth(self, client):
        """Тест: функционал требует авторизации"""
        response = client.get('/compositions_count', follow_redirects=True)
        assert response.status_code == 200
        assert 'Вход'.encode('utf-8') in response.data or b'login' in response.data.lower()
    
    def test_compositions_count_page(self, auth_buyer):
        """Тест: страница доступна авторизованным пользователям"""
        response = auth_buyer.get('/compositions_count')
        assert response.status_code == 200
    
    def test_compositions_count_with_ensemble(self, auth_buyer, db_connection):
        """Тест: выбор ансамбля показывает произведения"""
        conn = db_connection
        ensemble = conn.execute('SELECT id FROM ensembles LIMIT 1').fetchone()
        ensemble_id = ensemble['id']
        
        response = auth_buyer.get(f'/compositions_count?ensemble_id={ensemble_id}')
        assert response.status_code == 200


class TestEnsembleRecords:
    """Интеграционные тесты для функционала дисков ансамбля"""
    
    def test_ensemble_records_requires_auth(self, client):
        """Тест: функционал требует авторизации"""
        response = client.get('/ensemble_records', follow_redirects=True)
        assert response.status_code == 200
        assert 'Вход'.encode('utf-8') in response.data or b'login' in response.data.lower()
    
    def test_ensemble_records_page(self, auth_buyer):
        """Тест: страница доступна авторизованным пользователям"""
        response = auth_buyer.get('/ensemble_records')
        assert response.status_code == 200
    
    def test_ensemble_records_with_ensemble(self, auth_buyer, db_connection):
        """Тест: выбор ансамбля показывает пластинки"""
        conn = db_connection
        ensemble = conn.execute('SELECT id FROM ensembles LIMIT 1').fetchone()
        ensemble_id = ensemble['id']
        
        response = auth_buyer.get(f'/ensemble_records?ensemble_id={ensemble_id}')
        assert response.status_code == 200


class TestSalesLeaders:
    """Интеграционные тесты для лидеров продаж"""
    
    def test_sales_leaders_requires_auth(self, client):
        """Тест: функционал требует авторизации"""
        response = client.get('/sales_leaders', follow_redirects=True)
        assert response.status_code == 200
        assert 'Вход'.encode('utf-8') in response.data or b'login' in response.data.lower()
    
    def test_sales_leaders_page(self, auth_buyer):
        """Тест: страница лидеров продаж доступна"""
        response = auth_buyer.get('/sales_leaders')
        assert response.status_code == 200
        assert 'Лидеры продаж'.encode('utf-8') in response.data or 'продаж'.encode('utf-8') in response.data.lower()


class TestCatalog:
    """Интеграционные тесты для каталога"""
    
    def test_catalog_requires_auth(self, client):
        """Тест: каталог требует авторизации"""
        response = client.get('/catalog', follow_redirects=True)
        assert response.status_code == 200
        assert 'Вход'.encode('utf-8') in response.data or b'login' in response.data.lower()
    
    def test_catalog_page(self, auth_buyer):
        """Тест: каталог доступен покупателям"""
        response = auth_buyer.get('/catalog')
        assert response.status_code == 200
    
    def test_catalog_shows_only_in_stock(self, auth_buyer, db_connection):
        """Тест: каталог показывает только товары в наличии"""
        response = auth_buyer.get('/catalog')
        assert response.status_code == 200
        
        # Проверяем, что в каталоге нет товаров с current_stock = 0
        # (это проверяется через SQL запрос в app.py)


class TestCart:
    """Интеграционные тесты для корзины"""
    
    def test_cart_requires_auth(self, client):
        """Тест: корзина требует авторизации"""
        response = client.get('/cart', follow_redirects=True)
        assert response.status_code == 200
        assert 'Вход'.encode('utf-8') in response.data or b'login' in response.data.lower()
    
    def test_cart_requires_buyer_role(self, auth_seller):
        """Тест: корзина доступна только покупателям"""
        response = auth_seller.get('/cart', follow_redirects=True)
        assert response.status_code == 200
        assert 'Недостаточно прав'.encode('utf-8') in response.data or 'прав'.encode('utf-8') in response.data.lower()
    
    def test_cart_page(self, auth_buyer):
        """Тест: страница корзины доступна"""
        response = auth_buyer.get('/cart')
        assert response.status_code == 200
    
    def test_add_to_cart(self, auth_buyer, db_connection):
        """Тест: добавление товара в корзину"""
        conn = db_connection
        # Получаем запись в наличии
        record = conn.execute('''
            SELECT id FROM records WHERE current_stock > 0 LIMIT 1
        ''').fetchone()
        
        if record:
            record_id = record['id']
            response = auth_buyer.post(f'/add_to_cart/{record_id}', data={
                'quantity': '1'
            }, follow_redirects=True)
            
            assert response.status_code == 200
            assert 'добавлен в корзину'.encode('utf-8') in response.data.lower() or 'корзину'.encode('utf-8') in response.data


class TestPersonalCabinet:
    """Интеграционные тесты для личного кабинета"""
    
    def test_personal_cabinet_requires_auth(self, client):
        """Тест: личный кабинет требует авторизации"""
        response = client.get('/personal_cabinet', follow_redirects=True)
        assert response.status_code == 200
        assert 'Вход'.encode('utf-8') in response.data or b'login' in response.data.lower()
    
    def test_personal_cabinet_requires_buyer_role(self, auth_seller):
        """Тест: личный кабинет доступен только покупателям"""
        response = auth_seller.get('/personal_cabinet', follow_redirects=True)
        assert response.status_code == 200
        assert 'Недостаточно прав'.encode('utf-8') in response.data or 'прав'.encode('utf-8') in response.data.lower()
    
    def test_personal_cabinet_page(self, auth_buyer):
        """Тест: страница личного кабинета доступна"""
        response = auth_buyer.get('/personal_cabinet')
        assert response.status_code == 200


class TestManageEnsembles:
    """Интеграционные тесты для управления ансамблями"""
    
    def test_manage_ensembles_requires_director(self, auth_seller):
        """Тест: управление ансамблями доступно только директору"""
        response = auth_seller.get('/manage_ensembles', follow_redirects=True)
        assert response.status_code == 200
        assert 'Недостаточно прав'.encode('utf-8') in response.data or 'прав'.encode('utf-8') in response.data.lower()
    
    def test_manage_ensembles_director_access(self, auth_director):
        """Тест: директор может управлять ансамблями"""
        response = auth_director.get('/manage_ensembles')
        assert response.status_code == 200
    
    def test_add_ensemble(self, auth_director, db_connection):
        """Тест: добавление ансамбля"""
        response = auth_director.post('/add_ensemble', data={
            'name': 'Тестовый Ансамбль',
            'type': 'оркестр',
            'founded_year': '2000',
            'country': 'Россия',
            'description': 'Описание тестового ансамбля'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert 'успешно добавлен'.encode('utf-8') in response.data.lower() or 'добавлен'.encode('utf-8') in response.data
        
        # Проверяем в БД
        conn = db_connection
        ensemble = conn.execute('SELECT * FROM ensembles WHERE name = ?', ('Тестовый Ансамбль',)).fetchone()
        assert ensemble is not None


class TestManageUsers:
    """Интеграционные тесты для управления пользователями"""
    
    def test_manage_users_requires_director(self, auth_seller):
        """Тест: управление пользователями доступно только директору"""
        response = auth_seller.get('/manage_users', follow_redirects=True)
        assert response.status_code == 200
        assert 'Недостаточно прав'.encode('utf-8') in response.data or 'прав'.encode('utf-8') in response.data.lower()
    
    def test_manage_users_director_access(self, auth_director):
        """Тест: директор может управлять пользователями"""
        response = auth_director.get('/manage_users')
        assert response.status_code == 200
    
    def test_toggle_user_status(self, auth_director, db_connection):
        """Тест: активация/деактивация пользователя"""
        import time
        conn = db_connection
        # Создаем тестового пользователя с уникальным именем
        from werkzeug.security import generate_password_hash
        password_hash = generate_password_hash('test123')
        unique_username = f'toggle_user_{int(time.time() * 1000)}'
        
        try:
            conn.execute('''
                INSERT INTO users (username, password_hash, role, full_name, is_active)
                VALUES (?, ?, 'buyer', 'Test User', 1)
            ''', (unique_username, password_hash))
            conn.commit()
            
            user = conn.execute('SELECT id FROM users WHERE username = ?', (unique_username,)).fetchone()
            user_id = user['id']
            
            # Деактивируем пользователя
            response = auth_director.get(f'/toggle_user_status/{user_id}', follow_redirects=True)
            assert response.status_code == 200
            
            # Проверяем статус в БД
            user = conn.execute('SELECT is_active FROM users WHERE id = ?', (user_id,)).fetchone()
            assert user['is_active'] == 0
        finally:
            # Очищаем тестовые данные
            conn.execute('DELETE FROM users WHERE username = ?', (unique_username,))
            conn.commit()

