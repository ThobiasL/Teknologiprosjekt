# Rute for innlogging, registrering og utlogging av brukere.

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from adapters.database.flask.task_flask import User
from core.utils import hash_password, verify_password

auth = Blueprint('auth', __name__) # Lager blueprint for 'auth'

# Registreringsside, inkluderer funksjonalitet for endring og hashing av passord ved form.
@auth.route('/register', methods=['GET', 'POST'])
def register():
    users = User.query.all() 
    if request.method == 'POST':
        selected_id = request.form.get('id')
        password = request.form.get('password')

        user = User.query.filter_by(id=int(selected_id)).first()
      
        if user and password != '':
            user.password_hash = hash_password(password)
            user.save()
            flash('Passord endret', 'success')
            return redirect(url_for('auth.register'))
        else:
            flash('Bruker eller passord-feltet er tomt', 'error')

    # Vis registreringssiden
    return render_template('register.html', users=users)

# Innloggingsside, inkluderer funksjonalitet for å sjekke om bruker eksisterer og om passord er riktig.
@auth.route('/login', methods=['GET', 'POST'])
def login():
    users = User.query.all()
    selected_id = None 

    if request.method == 'POST':
        selected_id = request.form.get('id')
        password = request.form.get('password')

        if not selected_id or not password:
            flash('Fyll ut alle feltene', 'error')
            return render_template('login.html', users=users, selected_id=selected_id)
        
        user = User.query.filter_by(id=int(selected_id)).first()

        if not user:
            flash('Brukeren finnes ikke', 'error')
            return render_template('login.html', users=users, selected_id=selected_id)

        if verify_password(user.password_hash, password):
            session['user_id'] = user.id 
            flash('Logget inn', 'success') 
            return redirect(url_for('main.home'))
        else:
            flash('Feil passord', 'error')
            return render_template('login.html', users=users, selected_id=selected_id)

    return render_template('login.html', users=users, selected_id=selected_id)

# Utloggingsrute, fjerner brukeren fra sesjonen og sender brukeren til innloggingssiden.
@auth.route('/logout')
def logout():
    session.pop('user_id', None) 
    flash('Logget ut', 'success')
    return redirect(url_for('auth.login'))