# Memento

<br>

## Installasjons- og kjøreguide - Pi OS / Linux

Merk: Dette programmet har for øyeblikket kun støtte for kjøring på Linux-baserte operativsystemer.

<br>

## 1. Setup

### Kjør setup-scriptet

```
bash scripts/setup.sh
```

Dette vil installere alle nødvendige avhengigheter og konfigurere prosjektet.
Her vil du mest sannsynlig bli bedt om å skrive inn sudo-passord, da Caddy-serveren installeres system-wide.

<br>

## 2. Oppstart

### For kjøring av hele systemet:

```
bash scripts/run.sh
```

Dette vil starte opp alt. Merk: krever komplett system, inkl. eksterne moduler.

<br>

### For kjøring av webapp:

```
bash scripts/run_webapp.sh
```

Dette vil starte opp serverprosessene og webapplikasjonen for isolert kjøring.

<br>

### For kjøring av tester

```
bash scripts/test.sh
```

Dette vil kjøre alle de konfigurerte testene

<br>

## 3. Åpne webappen i nettleseren

<br>

Når serveren kjører, skriv inn IP-adressen fra kjøreloggen i nettleseren din for å få tilgang til webappen.

Merk: Du vil få en advarsel i nettleseren ved tilgang. Dette er fordi HTTPS-serveren benytter seg av selvsignert signatur, da den ikke har en DNS-server med domenenavn satt opp.