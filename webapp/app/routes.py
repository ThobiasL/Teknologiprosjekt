from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def login():
    return render_template('login.html')

@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/lock')
def lock():
    return render_template('lock.html')