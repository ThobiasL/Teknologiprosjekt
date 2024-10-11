from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/handle_redirect', methods=['POST'])
def handle_redirect():
    # Når skjemaet sendes, omdirigerer vi til en ny rute
    return redirect(url_for('redirected'))

if __name__ == '__main__':
    app.run(debug=True)