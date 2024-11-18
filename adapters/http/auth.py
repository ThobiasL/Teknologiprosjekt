from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from adapters.database.user_flask import User
from core.utils import hash_password, verify_password

auth = Blueprint('auth', __name__) # Lager blueprint for 'auth'

# Registreringsside, hvor brukere kan endre passord
@auth.route('/register', methods=['GET', 'POST'])
def register():
    users = User.query.all() 
    if request.method == 'POST':
        selected_id = request.form.get('id')
        password = request.form.get('password')

        user = User.query.filter_by(id=int(selected_id)).first()
      
        # Sjekker om brukeren eksisterer og setter nytt passord med melding, for så å vise registreringssiden på nytt
        if user and password != '':
            user.password_hash = hash_password(password)
            user.save()
            flash('Passord endret', 'success')
            return redirect(url_for('auth.register'))
        else:
            flash('Bruker eller passord-feltet er tomt', 'error')

    # Vis registreringssiden
    return render_template('register.html', users=users)

# Innloggingsside
@auth.route('/login', methods=['GET', 'POST'])
def login():
    users = User.query.all()
    selected_id = None  # Setter standardverdi for selected_id

    # Sjekker om innloggingsform er sendt inn
    if request.method == 'POST':
        selected_id = request.form.get('id') # Henter valgt ID fra form
        password = request.form.get('password') # Henter passord fra form

        if not selected_id or not password:
            flash('Fyll ut alle feltene', 'error')
            return render_template('login.html', users=users, selected_id=selected_id)
        
        user = User.query.filter_by(id=int(selected_id)).first()

        if not user:
            flash('Brukeren finnes ikke', 'error') # Feilmelding ved feil brukernavn
            return render_template('login.html', users=users, selected_id=selected_id)

        # Sjekker om brukeren eksisterer og om passordet er riktig
        if verify_password(user.password_hash, password):
            session['user_id'] = user.id # Setter brukernavn i sessionen
            flash('Logget inn', 'success') 
            return redirect(url_for('main.home'))
        else:
            flash('Feil passord', 'error') # Feilmelding ved feil passord
            return render_template('login.html', users=users, selected_id=selected_id)

    # Viser innloggingssiden
    return render_template('login.html', users=users, selected_id=selected_id)


# Utlogging
@auth.route('/logout')
def logout():
    session.pop('user_id', None)  # Fjerner brukeren fra sesjonen
    flash('Logget ut', 'success')
    return redirect(url_for('auth.login'))
    