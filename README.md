# Webapp - Installasjons- og kjøreguide - Pi OS / Linux

## Instruksjoner:

### 1. Gå til webapp\scripts-mappen
Naviger til scripts-mappen for å finne installasjons- og kjøre-skriptene.

### 2. Kjør setup-skriptet
- Kjør ***setup.sh***

Dette vil installere alle nødvendige avhengigheter og konfigurere prosjektet.

### 3. Kjør run-skriptet som passer til ditt OS

- Kjør ***run.sh***

Dette starter Flask-appen i utviklingsmodus.

<br>


**Alternativt:**

- For ***Windows:*** &nbsp;&nbsp; Kjør ***run_dev.bat***


Dette start Flask-appen uten behov for autentisering, for enkel utvikling.

### 4. Åpne webappen i nettleseren
Når serveren kjører, skriv inn en av IP-adressene fra kjøreloggen i nettleseren din for å få tilgang til webappen.


<br>
<br>

**Merk:**

*Disse instruksjonene er kun for et utviklingsmiljø, da de benytter Flask sin innebygde utviklingsserver, uten støtte for HTTPS. For produksjon anbefales en dedikert server, for å sikre bedre ytelse og sikkerhet.*