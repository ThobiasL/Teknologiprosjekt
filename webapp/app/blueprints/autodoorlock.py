from flask import Blueprint, request, redirect, url_for, render_template, flash # Importerer nødvendige funksjoner fra Flask
from core.models.autodoorlock import AutoDoorLock

# Lager blueprint for 'lock'
autodoorlock = Blueprint('autodoorlock', __name__)

# Funksjon for å vise låsesiden
@autodoorlock.route('/lock')
def show_lock_page():
    time = AutoDoorLock.query.get(1).time
    
    return render_template('lock.html', time=time)

# Funksjon for å oppdatere låsetid
@autodoorlock.route('/update_lock_time', methods=['POST'])
def update_lock_time():
    autodoorlock = AutoDoorLock.query.get(1)
    time = request.form.get('time')

    if time:
        autodoorlock.set_time(time)
        flash('Låsetid endret', 'message')

    return redirect(url_for('autodoorlock.show_lock_page'))

# Funksjon for å låse døren
@autodoorlock.route('/lock_door', methods=['POST'])
def lock_door():
    autodoorlock = AutoDoorLock.query.get(1)
    autodoorlock.set_status(True)
    flash('Dør låst', 'message')

    return redirect(url_for('autodoorlock.show_lock_page'))

# Funksjon for å låse opp døren
@autodoorlock.route('/unlock_door', methods=['POST'])
def unlock_door():
    autodoorlock = AutoDoorLock.query.get(1)
    autodoorlock.set_status(False)
    flash('Dør låst opp', 'message')

    return redirect(url_for('autodoorlock.show_lock_page'))
