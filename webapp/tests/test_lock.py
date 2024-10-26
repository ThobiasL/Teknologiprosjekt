from app import lock

def test_load_lock_data():
    lock_data = lock.load_lock_data()
    assert lock_data == {'lock_status': 0, 'lock_time': 0}