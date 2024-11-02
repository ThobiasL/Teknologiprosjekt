from app import create_app # Importerer create_app-funksjonen fra __init__.py

app = create_app() # Oppretter en instans av create_app-funksjonen

# Starter applikasjonen
if __name__ == "__main__":
    app.run()
    