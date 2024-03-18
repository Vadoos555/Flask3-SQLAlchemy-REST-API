import http
import json
import uuid

from dataclasses import dataclass
from app import app
from unittest.mock import patch


@dataclass
class FakeFilm:
    title = 'Fake Film'
    distributed_by = 'Fake'
    release_date = '2002-12-03'
    description = 'Fake description'
    length = 100
    rating = 8.0
    uuid = str(uuid.uuid4())
    

class TestFilms:
    uuid = []
    
    def test_get_films_with_db(self):
        client = app.test_client()
        response = client.get('/films')
        assert response.status_code == http.HTTPStatus.OK
    
    @patch('app.services.film_service.FilmService.fetch_all_films', autospec=True)
    def test_get_films_with_mock(self, mock_db_call):
        client = app.test_client()
        response = client.get('/films')
        
        mock_db_call.assert_called_once()
        assert response.status_code == http.HTTPStatus.OK
        assert len(response.json) == 0
    
    def test_create_film_with_db(self):
        client = app.test_client()
        data = {
            'title': 'Test Title',
            'distributed_by': 'Test Company',
            'release_date': '2010-04-01',
            'uuid': str(uuid.uuid4()),
            'description': '',
            'length': 100,
            'rating': 8.0
        }
        response = client.post('/films', data=json.dumps(data), content_type='application/json')
        assert response.status_code == http.HTTPStatus.CREATED
        assert response.json['title'] == 'Test Title'
        self.uuid.append(response.json['uuid'])
    
    def test_create_films_with_mock_db(self):
        with patch('app.db.session.add', autospec=True) as mock_session_add, \
            patch('app.db.session.commit', autospec=True) as mock_session_commit:
            client = app.test_client()
            data = {
                        'title': 'Test Title',
                        'distributed_by': 'Test Company',
                        'release_date': '2010-04-01',
                        'uuid': str(uuid.uuid4()),
                        'description': '',
                        'length': 100,
                        'rating': 8.0
                    }
            resp = client.post('/films', data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()
            
    def test_update_film_with_db(self):
        client = app.test_client()
        url = f'/films/{self.uuid[0]}'
        data = {
            'title': 'Update Title',
            'distributed_by': 'update',
            'release_date': '2010-04-01',
        }
        resp = client.put(url, data=json.dumps(data), content_type='application/json')
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json['title'] == 'Update Title'

    def test_update_film_with_mock_db(self):
        with patch('app.services.film_service.FilmService.fetch_film_by_uuid') as mocked_query, \
                patch('app.db.session.add', autospec=True) as mock_session_add, \
                patch('app.db.session.commit', autospec=True) as mock_session_commit:
            mocked_query.return_value = FakeFilm()
            client = app.test_client()
            url = f'/films/1'
            data = {
                'title': 'Update Title',
                'distributed_by': 'update',
                'release_date': '2010-04-01',
            }
            resp = client.put(url, data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_delete_film_with_db(self):
        client = app.test_client()
        url = f'/films/{self.uuid[0]}'
        resp = client.delete(url)
        assert resp.status_code == http.HTTPStatus.NO_CONTENT
    
    def test_delete_film_with_mock_db(self):
        with patch('app.services.film_service.FilmService.fetch_film_by_uuid') as mocked_query, \
                patch('app.db.session.delete', autospec=True) as mock_session_delete, \
                patch('app.db.session.commit', autospec=True) as mock_session_commit:
                    
            mocked_query.return_value = FakeFilm()
            client = app.test_client()
            url = f'/films/1'
            resp = client.delete(url)
            mock_session_delete.assert_called_once()
            mock_session_commit.assert_called_once()
            assert resp.status_code == http.HTTPStatus.NO_CONTENT
