from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from core.models.user import User
import adapters.database as db

auth = Blueprint('auth', __name__) # Lager blueprint for 'auth'

# Registreringsside, hvor brukere kan endre passord
@auth.route('/register', methods=['GET', 'POST'])
def register():
    users = User.query.all() 
    if request.method == 'POST':
        selected_id = request.form.get('id')
        password = request.form.get('password')

        id = int(selected_id) # Konverterer valgt ID til heltall, da det er en streng fra form
        user = User.query.filter_by(id=id).first() # Henter bruker fra databasen basert på ID

        # Sjekker om brukeren eksisterer og setter nytt passord med melding, for så å vise registreringssiden på nytt
        if user:
            user.set_password(password)
            flash('Passord endret', 'success')
            return redirect(url_for('auth.register', users=users))

    # Vis registreringssidena
    return render_template('global/register.html', users=users)

# Innloggingsside
@auth.route('/login', methods=['GET', 'POST'])
def login():
    users = User.query.all()
    selected_id = None  # Setter standardverdi for selected_id

    # Sjekker om innloggingsform er sendt inn
    if request.method == 'POST':
        selected_id = request.form.get('id') # Henter valgt ID fra form
        password = request.form.get('password') # Henter passord fra form

        user = User.query.filter_by(id=int(selected_id)).first() if selected_id else None
        # Sjekker om brukeren eksisterer og om passordet er riktig
        if user and user.check_password(password):
            session['username'] = user.name 
            flash('Logget inn', 'success') 
            return redirect(url_for('main.home'))
        else:
            flash('Feil passord', 'error') # Feilmelding ved feilet innlogging
            return render_template('global/login.html', users=users, selected_id=selected_id)

    return render_template('global/login.html', users=users, selected_id=selected_id)


# Utlogging
@auth.route('/logout')
def logout():
    session.pop('username', None)  # Fjerner brukeren fra sesjonen
    flash('Logget ut')
    return redirect(url_for('auth.login'))
    