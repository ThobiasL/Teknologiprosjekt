# Hovedsiderute 

from flask import Blueprint, redirect, url_for, render_template # importerer nødvendige funksjoner fra Flask

# Lager main-blueprint
main = Blueprint('main', __name__)

# Root-rute, omdirigerer til /home, evt. login hvis ikke innlogget
@main.route('/')
def index():
    return redirect(url_for('main.home'))

# Hovedsiderute
@main.route('/home')
def home():
    return render_template('home.html')