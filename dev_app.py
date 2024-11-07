from application import create_app # Importerer create_app-funksjonen fra __init__.py

# Funksjon for å lage en instans av appen uten autentisering
def create_dev_app():
    app = create_app()  # Henter appen fra __init__.py
    app.config['SKIP_AUTH'] = True  # Hopper over autentisering for utvikling

    return app

app = create_dev_app()  # Lager en instans av appen
    
# Starter appen
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)