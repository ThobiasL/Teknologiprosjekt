from flask import Blueprint, request, redirect, url_for, session, render_template # Importerer nødvendige funksjoner fra Flask
import json # Importerer json-modulen for lesing og skriving til låsens JSON-fil

# Lager blueprint for 'medication'
medication = Blueprint('medication', __name__)

# Path til JSON-filen
medication_path = 'data/medication.json'

# Funksjon for å lese data fra pilleboksens JSON-fil
def get_medication_time():
    with open(medication_path, 'r') as medication_file:
        medication_time = json.load(medication_file).get('medication_time', '00:00')
        return medication_time

# Funksjon for å lagre data til pilleboksens JSON-fil
def set_medication_time(medication_time):
    with open(medication_path, 'w') as medication_file:
        medication_time = {'medication_time': medication_time}
        json.dump(medication_time, medication_file)

# Funksjon for å vise medisinsiden
@medication.route('/medication')
def show_medication_page():
    # Sjekk om brukeren ikke er logget inn
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    # Hvis brukeren er logget inn, send til medication-siden
    medication_time = get_medication_time()
    return render_template('medication.html', medication_time=medication_time)

# Funksjon for å oppdatere låsetid
@medication.route('/update_medication_time', methods=['POST'])
def update_medication_time():
    medication_time = get_medication_time()
    new_medication_time = request.form.get('medication_time')
    if new_medication_time:
        medication_time = new_medication_time
        set_medication_time(medication_time)
    return redirect(url_for('medication.show_medication_page'))