from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

# Lag Blueprint
main = Blueprint('main', __name__)

# Funksjon for å lese fra profiles.json
def load_profiles():
    with open(os.path.join(os.getenv('INSTANCE_PATH', 'instance'), 'profiles.json'), 'r') as f:
        return json.load(f)

@main.route('/')
def index():
    # Sjekk om brukeren er logget inn
    if 'username' not in session:
        return redirect(url_for('main.login'))
    # Hvis brukeren er logget inn, send til home-siden
    return redirect(url_for('main.home'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Last inn brukere fra profiles.json
        profiles = load_profiles()

        # Sjekk brukernavn og passord
        if username in profiles and check_password_hash(profiles[username]['password'], password):
            session['username'] = username  # Legger brukernavn i sesjonen
            return redirect(url_for('main.home'))  # Omdiriger til home-siden
        else:
            # Hvis innloggingen feiler, send en feilmelding
            error = 'Ugyldig brukernavn eller passord.'
            return render_template('login.html', error=error)
        
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('username', None)  # Fjerner brukeren fra sesjonen
    flash('Du er nå logget ut.', 'info')
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hasher passordet og lagrer det i profiles.json
        hashed_password = generate_password_hash(password)

        # Laster inn brukere fra profiles.json
        profiles = load_profiles()

        # Sjekker om brukernavn allerede eksisterer
        if username in profiles:
            error = 'Brukernavnet er allerede tatt.'
            return render_template('register.html', error=error)

        # Hvis ikke, legg til ny bruker
        profiles[username] = {
            'username': username,
            'password': hashed_password
        }

        # Lagre den oppdaterte profiles.json-filen
        with open(os.path.join(os.getenv('INSTANCE_PATH', 'instance'), 'profiles.json'), 'w') as f:
            json.dump(profiles, f)

        # Omdiriger til innloggingssiden etter vellykket registrering
        return redirect(url_for('main.login'))
    
    # Vis registreringssiden ved GET-forespørsel
    return render_template('register.html')

@main.route('/home')
def home():
    # Sjekker om brukeren er logget inn
    if 'username' not in session:
        return redirect(url_for('main.login'))
    # Hvis brukeren er logget inn, send til home-siden
    return render_template('home.html')