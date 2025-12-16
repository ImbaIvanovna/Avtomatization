"""
Юнит-тесты для декораторов авторизации (login_required, role_required)
"""
import pytest


class TestLoginRequired:
    """Тесты для декоратора login_required"""
    
    def test_login_required_allows_authenticated(self, auth_buyer):
        """Тест: авторизованный пользователь имеет доступ"""
        response = auth_buyer.get('/personal_cabinet')
        assert response.status_code == 200
    
    def test_login_required_redirects_unauthenticated(self, client):
        """Тест: неавторизованный пользователь перенаправляется на вход"""
        response = client.get('/personal_cabinet', follow_redirects=True)
        assert response.status_code == 200
        # Должен перенаправить на страницу входа
        assert 'Вход'.encode('utf-8') in response.data or b'login' in response.data.lower()
        assert 'Необходимо войти'.encode('utf-8') in response.data or 'войти'.encode('utf-8') in response.data.lower()
    
    def test_login_required_with_compositions_count(self, client):
        """Тест: compositions_count требует авторизации"""
        response = client.get('/compositions_count', follow_redirects=True)
        assert response.status_code == 200
        assert 'Вход'.encode('utf-8') in response.data or b'login' in response.data.lower()
    
    def test_login_required_allows_access_when_logged_in(self, auth_buyer):
        """Тест: доступ разрешен после входа"""
        response = auth_buyer.get('/compositions_count')
        assert response.status_code == 200


class TestRoleRequired:
    """Тесты для декоратора role_required"""
    
    def test_role_required_allows_correct_role(self, auth_seller):
        """Тест: пользователь с правильной ролью имеет доступ"""
        response = auth_seller.get('/manage_records')
        assert response.status_code == 200
    
    def test_role_required_allows_director(self, auth_director):
        """Тест: директор имеет доступ ко всем функциям"""
        response = auth_director.get('/manage_records')
        assert response.status_code == 200
        
        response = auth_director.get('/manage_ensembles')
        assert response.status_code == 200
        
        response = auth_director.get('/manage_users')
        assert response.status_code == 200
    
    def test_role_required_denies_wrong_role(self, auth_buyer):
        """Тест: пользователь с неправильной ролью не имеет доступа"""
        # Покупатель не должен иметь доступа к manage_records
        response = auth_buyer.get('/manage_records', follow_redirects=True)
        assert response.status_code == 200
        assert 'Недостаточно прав'.encode('utf-8') in response.data or 'прав'.encode('utf-8') in response.data.lower()
        
        # Покупатель не должен иметь доступа к manage_ensembles
        response = auth_buyer.get('/manage_ensembles', follow_redirects=True)
        assert response.status_code == 200
        assert 'Недостаточно прав'.encode('utf-8') in response.data or 'прав'.encode('utf-8') in response.data.lower()
        
        # Покупатель не должен иметь доступа к manage_users
        response = auth_buyer.get('/manage_users', follow_redirects=True)
        assert response.status_code == 200
        assert 'Недостаточно прав'.encode('utf-8') in response.data or 'прав'.encode('utf-8') in response.data.lower()
    
    def test_role_required_redirects_unauthenticated(self, client):
        """Тест: неавторизованный пользователь перенаправляется"""
        response = client.get('/manage_records', follow_redirects=True)
        assert response.status_code == 200
        assert 'Вход'.encode('utf-8') in response.data or b'login' in response.data.lower()
    
    def test_role_required_buyer_only(self, client):
        """Тест: доступ только для покупателей"""
        # Персонализированный кабинет только для buyer
        response = client.get('/personal_cabinet', follow_redirects=True)
        assert response.status_code == 200
        
        # Авторизуемся как buyer
        response = client.post('/login', data={
            'username': 'buyer1',
            'password': 'buyer123'
        }, follow_redirects=True)
        
        response = client.get('/personal_cabinet')
        assert response.status_code == 200
    
    def test_role_required_seller_cannot_access_director_only(self, auth_seller):
        """Тест: продавец не может получить доступ к функциям директора"""
        # manage_ensembles только для director
        response = auth_seller.get('/manage_ensembles', follow_redirects=True)
        assert response.status_code == 200
        assert 'Недостаточно прав'.encode('utf-8') in response.data or 'прав'.encode('utf-8') in response.data.lower()
        
        # manage_users только для director
        response = auth_seller.get('/manage_users', follow_redirects=True)
        assert response.status_code == 200
        assert 'Недостаточно прав'.encode('utf-8') in response.data or 'прав'.encode('utf-8') in response.data.lower()

