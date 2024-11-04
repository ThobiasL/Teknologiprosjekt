from flask import Blueprint, request, redirect, url_for, render_template # Importerer nødvendige funksjoner fra Flask

# Lager blueprint for 'medication'
medication = Blueprint('medication', __name__)

# Funksjon for å vise medisinsiden
@medication.route('/medication')
def show_medication_page():

    return render_template('medication.html')

'''

# Funksjon for å lese data fra pilleboksens JSON-fil
def get_medication_time():
    with open(medication_path, 'r') as medication_file:
        medication_time = json.load(medication_file).get('medication_time')
        return medication_time

# Funksjon for å lagre data til pilleboksens JSON-fil
def set_medication_time(medication_time):
    with open(medication_path, 'w') as medication_file:
        medication_time = {'medication_time': medication_time}
        json.dump(medication_time, medication_file)



# Funksjon for å oppdatere låsetid
@medication.route('/update_medication_time', methods=['POST'])
def update_medication_time():
    medication_time = get_medication_time()
    new_medication_time = request.form.get('medication_time')
    if new_medication_time:
        medication_time = new_medication_time
        set_medication_time(medication_time)
    return redirect(url_for('medication.show_medication_page'))

'''