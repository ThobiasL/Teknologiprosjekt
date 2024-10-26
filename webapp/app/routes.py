from flask import Blueprint, flash, session, redirect, url_for, render_template # importerer nødvendige funksjoner fra Flask

# Lager main-blueprint
main = Blueprint('main', __name__)

# Startside
@main.route('/')
def index():
    # Sjekk om brukeren ikke er logget inn
    if 'username' not in session:
        flash('Du er ikke logget inn', 'warning')
        return redirect(url_for('auth.login'))
    # Hvis brukeren er logget inn, send til home-siden
    return redirect(url_for('main.home'))


# Hovedside etter innlogging
@main.route('/home')
def home():
    # Sjekker om brukeren ikke er logget inn
    if 'username' not in session:
        flash('Du er ikke logget inn', 'warning')
        return redirect(url_for('auth.login'))
    # Hvis brukeren er logget inn, send til home-siden
    return render_template('home.html')