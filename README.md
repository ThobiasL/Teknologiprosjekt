# Webapp - Installasjons- og kjøreguide - Pi OS / Linux

## 1. Setup

### Kjør setup-scriptet

```
bash scripts/setup.sh
```

Dette vil installere alle nødvendige avhengigheter og konfigurere prosjektet.
Her vil du bli bedt om å skrive inn sudo-passord.

## 2. Oppstart

### For kjøring av webapp

```
bash scripts/run.sh
```

Dette vil starte opp serverprosessene

<br>

### For kjøring av tester

```
bash scripts/test.sh
```

Dette vil kjøre alle de konfigurerte testene

## 3. Åpne webappen i nettleseren

<br>

Når serveren kjører, skriv inn IP-adressen fra kjøreloggen i nettleseren din for å få tilgang til webappen.

<br>
<br>


Merk: Ettersom en DNS-server ikke er satt opp, kjører HTTPS-serveren med en uoffisiell signatur. Dette vil føre til en advarsel i nettleseren ved tilgang.