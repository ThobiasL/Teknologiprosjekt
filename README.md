# Webapp - Installasjons- og kjøreguide

## Instruksjoner:

### 1. Gå til webapp\scripts-mappen
Naviger til scripts-mappen under webapp-katalogen for å finne installasjons- og kjøre-skriptene.

### 2. Kjør setup-skriptet som passer til ditt OS
- For ***Windows:*** &nbsp;&nbsp; Kjør ***setup.bat***
- For ***Linux:*** &nbsp;&nbsp; Kjør ***setup.sh***

Dette vil installere alle nødvendige avhengigheter og konfigurere prosjektet.

### 3. Kjør run-skriptet som passer til ditt OS
- For ***Windows:*** &nbsp;&nbsp; Kjør ***run.bat***
- For ***Linux:*** &nbsp;&nbsp; Kjør ***run.sh***

Dette starter Flask-appen i utviklingsmodus.

### 4. Åpne webappen i nettleseren
Når serveren kjører, skriv inn en av IP-adressene under i nettleseren din for å få tilgang til webappen.
    
    http://127.0.0.1:5000

    http://10.0.0.3:5000

<br>
<br>

**Merk:**

*Disse instruksjonene er kun for et utviklingsmiljø, da de benytter Flask sin innebygde utviklingsserver. For produksjon anbefales en dedikert server, for å sikre bedre ytelse og sikkerhet.*