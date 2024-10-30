from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.adapters.database import db

auth = Blueprint('auth', __name__) # Lager blueprint for 'auth'

# Registreringsside
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].lower() # Brukernavn lagres i små bokstaver for å gjøre det case-insensitive
        password = request.form['password']
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error = 'Brukernavnet er allerede tatt.'
            return render_template('register.html', error=error)
        
        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Passord satt. Logg inn for å fortsette.')
        return redirect(url_for('auth.login'))
    
    # Vis registreringssiden
    return render_template('register.html')

# Innloggingsside
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].lower() # Brukernavn lagres i små bokstaver for å gjøre det case-insensitive
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            return redirect(url_for('main.home'))
        else:
            error = 'Feil passord.'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Utlogging
@auth.route('/logout')
def logout():
    session.pop('username', None)  # Fjerner brukeren fra sesjonen
    flash('Logget ut')
    return redirect(url_for('auth.login'))
    