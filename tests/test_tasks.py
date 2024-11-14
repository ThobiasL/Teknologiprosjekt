import pytest
from flask import session
from application.database import db
from adapters.database.task_db import Task
from adapters.database.user_db import User

def login(client, app, user, password):
    with app.app_context():
        response = client.post('/login', data={'id': user.id, 'password': password})
        assert response.status_code == 302
        assert '/home' in response.location
        
    return response