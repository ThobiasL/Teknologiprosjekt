from flask import Blueprint, request, redirect, url_for, session, render_template # Importerer nødvendige funksjoner fra Flask
import json # Importerer json-modulen for lesing og skriving til låsens JSON-fil

# Lager blueprint for 'lock'
autodoorlock = Blueprint('autodoorlock', __name__)

# Funksjon for å vise låsesiden
@autodoorlock.route('/lock')
def show_lock_page():
    '''
    lock_data = get_lock_data()
    lock_time = lock_data.get('lock_time')
    '''
    lock_time = '22:55'
    return render_template('lock.html', lock_time=lock_time)

'''
# Funksjon for å lese data fra låsens JSON-fil
def get_lock_data():
    with open(lock_path, 'r') as lock_file:
        lock_data = json.load(lock_file)
        return lock_data

# Funksjon for å lagre data til låsens JSON-fil
def set_lock_data(lock_status, lock_time):
    with open(lock_path, 'w') as lock_file:
        lock_data = {'lock_status': lock_status, 'lock_time': lock_time}
        json.dump(lock_data, lock_file)



# Funksjon for å oppdatere låsetid
@autodoorlock.route('/update_lock_time', methods=['POST'])
def update_lock_time():
    lock_data = get_lock_data()
    new_lock_time = request.form.get('lock_time')
    if new_lock_time:
        lock_data['lock_time'] = new_lock_time
        set_lock_data(lock_data['lock_status'], lock_data['lock_time'])
    return redirect(url_for('lock.show_lock_page'))

# Funksjon for å låse døren
@autodoorlock.route('/lock_door', methods=['POST'])
def lock_door():
    lock_data = get_lock_data()
    lock_data['lock_status'] = 1
    set_lock_data(lock_data['lock_status'], lock_data['lock_time'])
    return redirect(url_for('lock.show_lock_page'))

# Funksjon for å låse opp døren
@autodoorlock.route('/unlock_door', methods=['POST'])
def unlock_door():
    lock_data = get_lock_data()
    lock_data['lock_status'] = 0
    set_lock_data(lock_data['lock_status'], lock_data['lock_time'])
    return redirect(url_for('lock.show_lock_page'))

    '''