import http
import json

from app import app
from unittest.mock import patch
from app.services.actor_service import ActorService
from app.database.models import Actor 

class TestActors:
    uuid = []
    
    def test_get_actors_with_db(self):
        client = app.test_client()
        response = client.get('/actors')
        assert response.status_code == http.HTTPStatus.OK
    
    @patch('app.services.actor_service.ActorService.fetch_all_actors', autospec=True)
    def test_get_actors_with_mock(self, mock_db_call):
        client = app.test_client()
        response = client.get('/actors')
        
        mock_db_call.assert_called_once()
        assert response.status_code == http.HTTPStatus.OK
        assert len(response.json) == 0
    
    def test_create_actor_with_db(self):
        client = app.test_client()
        data = {
            'name': 'Test Actor',
            'birthday': '1990-01-01',
            'is_active': True
        }
        response = client.post('/actors', data=json.dumps(data), content_type='application/json')
        assert response.status_code == http.HTTPStatus.CREATED
        assert response.json['name'] == 'Test Actor'
        self.uuid.append(response.json['id'])
    
    def test_create_actors_with_mock_db(self):
        with patch('app.db.session.add', autospec=True) as mock_session_add, \
            patch('app.db.session.commit', autospec=True) as mock_session_commit:
                client = app.test_client()
                data = {
                    'name': 'Test Actor',
                    'birthday': '1990-01-01',
                    'is_active': True
                }
                resp = client.post('/actors', data=json.dumps(data), content_type='application/json')
                mock_session_add.assert_called_once()
                mock_session_commit.assert_called_once()
            
    def test_update_actor_with_db(self):
        client = app.test_client()
        url = f'/actors/{self.uuid[0]}'
        data = {
            'name': 'Updated Actor',
            'birthday': '1990-01-01',
            'is_active': False
        }
        resp = client.put(url, data=json.dumps(data), content_type='application/json')
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json['name'] == 'Updated Actor'

    def test_update_actor_with_mock_db(self):
        with patch('app.services.actor_service.ActorService.fetch_actor_by_id') as mocked_query, \
                patch('app.db.session.add', autospec=True) as mock_session_add, \
                patch('app.db.session.commit', autospec=True) as mock_session_commit:
            mocked_query.return_value = Actor(name='Test Actor', birthday='1990-01-01', is_active=True)
            client = app.test_client()
            url = f'/actors/1'
            data = {
                'name': 'Updated Actor',
                'birthday': '1990-01-01',
                'is_active': False
            }
            resp = client.put(url, data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_delete_actor_with_db(self):
        client = app.test_client()
        url = f'/actors/{self.uuid[0]}'
        resp = client.delete(url)
        assert resp.status_code == http.HTTPStatus.NO_CONTENT
    
    def test_delete_actor_with_mock_db(self):
        with patch('app.services.actor_service.ActorService.fetch_actor_by_id') as mocked_query, \
                patch('app.db.session.delete', autospec=True) as mock_session_delete, \
                patch('app.db.session.commit', autospec=True) as mock_session_commit:
            mocked_query.return_value = Actor(name='Delete Actor', birthday='1990-01-01', is_active=True)
            client = app.test_client()
            url = f'/actors/1'
            resp = client.delete(url)
            mock_session_delete.assert_called_once()
            mock_session_commit.assert_called_once()
            assert resp.status_code == http.HTTPStatus.NO_CONTENT

