# Rute for AutoDoorLock-modulen, inkluderer funksjonalitet for å endre låsetid og låse/åpne døren.

from flask import Blueprint, request, redirect, url_for, render_template, flash # Importerer nødvendige funksjoner fra Flask
from adapters.database.flask.autodoorlock_flask import AutoDoorLock
from core.utils import is_valid_time

# Lager blueprint for 'lock'
autodoorlock = Blueprint('autodoorlock', __name__)

# Funksjon for å vise låsesiden og hente nåværende låsetid
@autodoorlock.route('/lock_control')
def show_page():
    autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)

    time = autodoorlock.get('time')
    
    return render_template('lock.html', time=time)

# Funksjon for å oppdatere låsetid fra form
@autodoorlock.route('/update_lock_time', methods=['POST'])
def update_lock_time():
    autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)
    time = request.form.get('time')

    if not is_valid_time(time):
        flash('Ugyldig tid', 'error')
        return redirect(url_for('autodoorlock.show_page'))
    
    autodoorlock.set('time', time)
    flash('Låsetid endret', 'success')
    return redirect(url_for('autodoorlock.show_page'))

# Funksjon for å låse døren ved tastetrykk
@autodoorlock.route('/lock_door', methods=['POST'])
def lock_door():
    autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)

    autodoorlock.set('status', True)

    flash('Dør låst', 'success')

    return redirect(url_for('autodoorlock.show_page'))

# Funksjon for å låse opp døren ved tastetrykk
@autodoorlock.route('/unlock_door', methods=['POST'])
def unlock_door():

    autodoorlock = AutoDoorLock.get_by_id(AutoDoorLock, 1)

    autodoorlock.set('status', False)

    flash('Dør låst opp', 'success')

    return redirect(url_for('autodoorlock.show_page'))
