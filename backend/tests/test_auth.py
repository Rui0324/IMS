import pytest
from rest_framework.test import APIClient

from apps.accounts.models import User


@pytest.mark.django_db
def test_login_flow(client):
    User.objects.create_user(username='admin', password='pass123', role='admin')
    client = APIClient()
    resp = client.post('/api/auth/login', {'username': 'admin', 'password': 'pass123'}, format='json')
    assert resp.status_code == 200
    data = resp.json()
    assert 'access' in data


@pytest.mark.django_db
def test_project_permissions(client):
    student = User.objects.create_user(username='stu', password='pass123', role='student')
    client = APIClient()
    client.force_authenticate(student)
    resp = client.post('/api/projects/', {'title': 'demo', 'description': 'desc'}, format='json')
    assert resp.status_code == 201
    project_id = resp.json()['id']
    resp_list = client.get('/api/projects/')
    assert resp_list.status_code == 200
    assert resp_list.json()[0]['id'] == project_id
