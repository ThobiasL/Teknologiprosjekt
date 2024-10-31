from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user import User
from app.adapters.database import db

auth = Blueprint('auth', __name__) # Lager blueprint for 'auth'

# Registreringsside
@auth.route('/register', methods=['GET', 'POST'])
def register():
    users = User.query.all()
    if request.method == 'POST':
        selected_id = request.form.get('id')
        password = request.form.get('password')

        id = int(selected_id)
        user = User.query.get(id)
        if user:
            user.set_password(password)
            flash('Passord endret', 'success')
            return redirect(url_for('auth.register', users=users))

    # Vis registreringssiden
    return render_template('global/register.html', users=users)

# Innloggingsside
@auth.route('/login', methods=['GET', 'POST'])
def login():
    users = User.query.all()
    if request.method == 'POST':
        selected_id = request.form.get('id')
        password = request.form.get('password')

        user = User.query.get(int(selected_id))
        if user and user.check_password(password):
            session['username'] = user.name
            flash('Logget inn', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Feil passord', 'error')
            return redirect(url_for('auth.login', users=users))

    return render_template('global/login.html', users=users)

# Utlogging
@auth.route('/logout')
def logout():
    session.pop('username', None)  # Fjerner brukeren fra sesjonen
    flash('Logget ut')
    return redirect(url_for('auth.login'))
    