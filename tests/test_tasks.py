import pytest
from flask import session
from adapters.database import db
from core.models.task import Task
from core.models.user import User

def login(client, app, user, password):
    with app.app_context():
        response = client.post('/login', data={'id': user.id, 'password': password})
        assert response.status_code == 302
        assert '/home' in response.location
        
    return response