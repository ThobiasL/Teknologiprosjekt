from application import create_app

app = create_app() # Oppretter en instans av create_app-funksjonen

# Starter applikasjonen
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
