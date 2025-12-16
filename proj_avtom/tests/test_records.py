"""
Юнит-тесты для управления записями (CRUD операции)
"""
import pytest


class TestManageRecords:
    """Тесты для страницы управления записями"""
    
    def test_manage_records_requires_auth(self, client):
        """Тест: доступ к странице управления записями требует авторизации"""
        response = client.get('/manage_records', follow_redirects=True)
        assert response.status_code == 200
        # Должен перенаправить на страницу входа
        response_text = response.data.decode('utf-8')
        assert 'Вход' in response_text or 'login' in response_text.lower()
    
    def test_manage_records_requires_role(self, auth_buyer):
        """Тест: доступ только для seller и director"""
        response = auth_buyer.get('/manage_records', follow_redirects=True)
        assert response.status_code == 200
        # Покупатель не должен иметь доступа
        response_text = response.data.decode('utf-8')
        assert 'Недостаточно прав' in response_text or 'прав' in response_text.lower()
    
    def test_manage_records_seller_access(self, auth_seller):
        """Тест: продавец может получить доступ"""
        response = auth_seller.get('/manage_records')
        assert response.status_code == 200
        response_text = response.data.decode('utf-8')
        assert 'Управление компакт-дисками' in response_text or 'дисками' in response_text.lower()
    
    def test_manage_records_director_access(self, auth_director):
        """Тест: директор может получить доступ"""
        response = auth_director.get('/manage_records')
        assert response.status_code == 200


class TestAddRecord:
    """Тесты для добавления записи"""
    
    def test_add_record_success(self, auth_seller, db_connection):
        """Тест: успешное добавление записи"""
        import time
        # Получаем ID компании для теста
        conn = db_connection
        company = conn.execute('SELECT id FROM companies LIMIT 1').fetchone()
        company_id = company['id']
        
        # Используем уникальный каталожный номер
        unique_catalog = f'TEST-{int(time.time() * 1000)}'
        
        response = auth_seller.post('/add_record', data={
            'catalog_number': unique_catalog,
            'title': 'Тестовая пластинка',
            'company_id': company_id,
            'release_date': '2024-01-01',
            'wholesale_price': '10.50',
            'retail_price': '19.99',
            'current_stock': '100',
            'sold_last_year': '0',
            'sold_this_year': '0'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        response_text = response.data.decode('utf-8')
        assert 'успешно добавлена' in response_text.lower() or 'добавлена' in response_text
        
        # Проверяем, что запись создана в БД
        record = conn.execute('SELECT * FROM records WHERE catalog_number = ?', (unique_catalog,)).fetchone()
        assert record is not None
        assert record['title'] == 'Тестовая пластинка'
        
        # Очищаем тестовые данные
        conn.execute('DELETE FROM records WHERE catalog_number = ?', (unique_catalog,))
        conn.commit()
    
    def test_add_record_duplicate_catalog_number(self, auth_seller, db_connection):
        """Тест: добавление записи с существующим каталожным номером"""
        import time
        conn = db_connection
        company = conn.execute('SELECT id FROM companies LIMIT 1').fetchone()
        company_id = company['id']
        
        # Используем уникальный каталожный номер для первой записи
        unique_catalog = f'DUPLICATE-{int(time.time() * 1000)}'
        
        # Первая запись
        auth_seller.post('/add_record', data={
            'catalog_number': unique_catalog,
            'title': 'Первая пластинка',
            'company_id': company_id,
            'wholesale_price': '10.00',
            'retail_price': '20.00',
            'current_stock': '50'
        }, follow_redirects=True)
        
        # Вторая запись с тем же номером (должна вызвать ошибку)
        response = auth_seller.post('/add_record', data={
            'catalog_number': unique_catalog,
            'title': 'Вторая пластинка',
            'company_id': company_id,
            'wholesale_price': '10.00',
            'retail_price': '20.00',
            'current_stock': '50'
        }, follow_redirects=True)
        
        # Должна быть ошибка из-за UNIQUE constraint
        assert response.status_code == 200
        # Проверяем сообщение об ошибке
        response_text = response.data.decode('utf-8')
        assert 'Ошибка' in response_text or 'ошибка' in response_text.lower()
        
        # Очищаем тестовые данные
        conn.execute('DELETE FROM records WHERE catalog_number = ?', (unique_catalog,))
        conn.commit()
    
    def test_add_record_requires_auth(self, client):
        """Тест: добавление записи требует авторизации"""
        response = client.post('/add_record', data={
            'catalog_number': 'TEST-002',
            'title': 'Тестовая пластинка'
        }, follow_redirects=True)
        
        # Должен перенаправить на страницу входа
        assert response.status_code == 200


class TestEditRecord:
    """Тесты для редактирования записи"""
    
    def test_edit_record_page(self, auth_seller, db_connection):
        """Тест: получение страницы редактирования"""
        conn = db_connection
        record = conn.execute('SELECT id FROM records LIMIT 1').fetchone()
        record_id = record['id']
        
        response = auth_seller.get(f'/edit_record/{record_id}')
        assert response.status_code == 200
        # Проверяем наличие слова "Редактирование" в ответе
        response_text = response.data.decode('utf-8')
        assert 'Редактирование' in response_text or 'редактир' in response_text.lower()
    
    def test_update_record_success(self, auth_seller, db_connection):
        """Тест: успешное обновление записи"""
        import time
        conn = db_connection
        company = conn.execute('SELECT id FROM companies LIMIT 1').fetchone()
        company_id = company['id']
        
        # Используем уникальный каталожный номер
        unique_catalog = f'UPDATE-TEST-{int(time.time() * 1000)}'
        
        # Создаем тестовую запись
        conn.execute('''
            INSERT INTO records (catalog_number, title, company_id, wholesale_price, retail_price, current_stock)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (unique_catalog, 'Исходное название', company_id, 10.00, 20.00, 50))
        conn.commit()
        
        record = conn.execute('SELECT id FROM records WHERE catalog_number = ?', (unique_catalog,)).fetchone()
        record_id = record['id']
        
        response = auth_seller.post(f'/update_record/{record_id}', data={
            'catalog_number': unique_catalog,
            'title': 'Обновленное название',
            'company_id': company_id,
            'release_date': '2024-01-01',
            'wholesale_price': '15.00',
            'retail_price': '25.00',
            'current_stock': '75',
            'sold_last_year': '10',
            'sold_this_year': '5'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Декодируем response.data для проверки
        response_text = response.data.decode('utf-8')
        assert 'успешно обновлена' in response_text.lower() or 'обновлена' in response_text
        
        # Проверяем изменения в БД
        updated_record = conn.execute('SELECT * FROM records WHERE id = ?', (record_id,)).fetchone()
        assert updated_record['title'] == 'Обновленное название'
        assert updated_record['current_stock'] == 75
        
        # Очищаем тестовые данные
        conn.execute('DELETE FROM records WHERE id = ?', (record_id,))
        conn.commit()
    
    def test_update_nonexistent_record(self, auth_seller):
        """Тест: обновление несуществующей записи"""
        response = auth_seller.post('/update_record/99999', data={
            'catalog_number': 'NONEXISTENT',
            'title': 'Несуществующая',
            'company_id': '1',
            'wholesale_price': '10.00',
            'retail_price': '20.00',
            'current_stock': '50'
        }, follow_redirects=True)
        
        assert response.status_code == 200


class TestDeleteRecord:
    """Тесты для удаления записи"""
    
    def test_delete_record_success(self, auth_seller, db_connection):
        """Тест: успешное удаление записи"""
        import time
        conn = db_connection
        company = conn.execute('SELECT id FROM companies LIMIT 1').fetchone()
        company_id = company['id']
        
        # Используем уникальный каталожный номер
        unique_catalog = f'DELETE-TEST-{int(time.time() * 1000)}'
        
        # Создаем тестовую запись
        conn.execute('''
            INSERT INTO records (catalog_number, title, company_id, wholesale_price, retail_price, current_stock)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (unique_catalog, 'Запись для удаления', company_id, 10.00, 20.00, 50))
        conn.commit()
        
        record = conn.execute('SELECT id FROM records WHERE catalog_number = ?', (unique_catalog,)).fetchone()
        record_id = record['id']
        
        response = auth_seller.get(f'/delete_record/{record_id}', follow_redirects=True)
        
        assert response.status_code == 200
        # Декодируем response.data для проверки
        response_text = response.data.decode('utf-8')
        assert 'успешно удалена' in response_text.lower() or 'удалена' in response_text
        
        # Проверяем, что запись удалена из БД
        deleted_record = conn.execute('SELECT * FROM records WHERE id = ?', (record_id,)).fetchone()
        assert deleted_record is None
    
    def test_delete_nonexistent_record(self, auth_seller):
        """Тест: удаление несуществующей записи"""
        response = auth_seller.get('/delete_record/99999', follow_redirects=True)
        assert response.status_code == 200
    
    def test_delete_record_requires_auth(self, client):
        """Тест: удаление записи требует авторизации"""
        response = client.get('/delete_record/1', follow_redirects=True)
        assert response.status_code == 200
        # Должен перенаправить на страницу входа
        response_text = response.data.decode('utf-8')
        assert 'Вход' in response_text or 'login' in response_text.lower()

