from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import json

auth = Blueprint('auth', __name__) # Lager blueprint for 'auth'

profiles_path = 'data/profiles.json' # Path til profiles.json

# Funksjon for å lese fra profiles.json
def load_profiles():
    with open(profiles_path, 'r') as profiles_file:
        return json.load(profiles_file)

# Registreringsside
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].lower() # Brukernavn lagres i små bokstaver for å gjøre det case-insensitive
        password = request.form['password']
        
        # Hasher og salter passordet
        password_hash = generate_password_hash(password)

        # Laster inn brukere fra profiles.json
        profiles = load_profiles()

        # Sjekker om brukernavn allerede eksisterer
        if username in profiles:
            error = 'Brukernavnet er allerede tatt.'
            return render_template('register.html', error=error)

        # Hvis ikke, legg til ny bruker
        profiles[username] = {
            'username': username,
            'password': password_hash
        }

        # Lagre den oppdaterte profiles.json-filen
        with open(profiles_path, 'w') as profiles_file:
            json.dump(profiles, profiles_file)

        # Omdiriger til innloggingssiden etter vellykket registrering
        return redirect(url_for('auth.login'))
    
    # Vis registreringssiden
    return render_template('register.html')

# Innloggingsside
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].lower() # Brukernavn lagres i små bokstaver for å gjøre det case-insensitive
        password = request.form['password']

        # Last inn brukere fra profiles.json
        profiles = load_profiles()

        # Sjekk brukernavn og passord
        if username in profiles and check_password_hash(profiles[username]['password'], password):
            session['username'] = username  # Legger brukernavn i sesjonen
            return redirect(url_for('main.home'))  # Omdirigerer til home-siden
        else:
            # Hvis innloggingen feiler, send en feilmelding
            error = 'Ugyldig brukernavn eller passord.'
            return render_template('login.html', error=error)
    return render_template('login.html')

# Utlogging
@auth.route('/logout')
def logout():
    session.pop('username', None)  # Fjerner brukeren fra sesjonen
    return redirect(url_for('auth.login'))
