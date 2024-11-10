from flask import Blueprint, redirect, url_for, render_template # importerer nødvendige funksjoner fra Flask

# Lager main-blueprint
main = Blueprint('main', __name__)

# Startside
@main.route('/')
def index():
    return redirect(url_for('main.home'))

# Hovedside etter innlogging
@main.route('/home')
def home():
    return render_template('home.html')