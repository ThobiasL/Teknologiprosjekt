import pytest
from flask import session
from webapp.adapters.database import db
from autodoorlock import AutoDoorLock

def test_autodoorlock_show_state():

def test_autodoorlock_initial_state():
    doorlock = AutoDoorLock()
    assert doorlock.is_locked() == False

def test_autodoorlock_lock():
    doorlock = AutoDoorLock()
    doorlock.lock()
    assert doorlock.is_locked() == True

def test_autodoorlock_unlock():
    doorlock = AutoDoorLock()
    doorlock.lock()
    doorlock.unlock()
    assert doorlock.is_locked() == False

if __name__ == "__main__":
    pytest.main()