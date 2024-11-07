from flask import Blueprint, request, redirect, url_for, render_template # Importerer nødvendige funksjoner fra Flask

# Lager blueprint for 'medication'
medication = Blueprint('medication', __name__)

# Funksjon for å vise medisinsiden
@medication.route('/medication')
def show_page():

    return render_template('medication.html')

def get_medication_time():
    return None

# Funksjon for å lagre data til pilleboksens JSON-fil
def set_medication_time(medication_time):
    return None


# Funksjon for å oppdatere låsetid
@medication.route('/update_medication_time', methods=['POST'])
def update_medication_time():
    medication_time = get_medication_time()
    new_medication_time = request.form.get('medication_time')
    if new_medication_time:
        medication_time = new_medication_time
        set_medication_time(medication_time)
    return redirect(url_for('medication.show_page'))
