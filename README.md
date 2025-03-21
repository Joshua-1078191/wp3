# WP3-2025 Accessibility Hub

## Projectbeschrijving

De WP3-2025 Accessibility Hub is een op Flask gebaseerde webapplicatie die is ontworpen om een toegankelijkheidshub te creëren die tools en middelen biedt voor het verbeteren van webtoegankelijkheid. De applicatie stelt organisaties en experts in staat om samen te werken aan het toegankelijker maken van producten en diensten voor iedereen.

## Kenmerken

- Gebruikersauthenticatie en rolgebaseerde toegangscontrole (Admin, Organisatie, Ervaringsdeskundige)
- Applicatiebeheer met goedkeurings- en afkeuringsfunctionaliteit
- Notificatiesysteem voor statusupdates van applicaties
- Responsief ontwerp met een gebruiksvriendelijke interface

## Aan de Slag

### Vereisten

- Python 3.x
- pip (Python pakketbeheerder)

### Installatie

1. Clone de repository:
   ```bash
   git clone https://github.com/jouwgebruikersnaam/wp3-2025-accessibility-hub.git
   cd wp3-2025-accessibility-hub

2.
Installeer de vereiste pakketten:
- pip install flask
- pip install sqlalchemy
- pip install flask-swagger-ui

3.
Stel de database in:
Voer het databasegenerator-script uit om de SQLite-database te maken:
python lib/database_generator.py

### De Applicatie Uitvoeren
1.
Start de Flask-applicatie:
flask run

2.
Open je webbrowser en navigeer naar http://localhost:5000 om toegang te krijgen tot de applicatie.

### Gebruik
Admin Dashboard: Beheer applicaties, keur applicaties goed of af, en bekijk in behandeling zijnde applicaties.
Organisatie Dashboard: Dien applicaties in en bekijk de status van ingediende applicaties.
Expert Dashboard: Bekijk en solliciteer voor beschikbare kansen.

### Projectstructuur
assets/: Bevat afbeeldingen, lettertypen en stylesheets.
databases/: Bevat het SQLite-databasebestand.
lib/: Bevat het databasegenerator-script.
src/: Bevat de kernfunctionaliteit van de applicatie.
static/: Bevat JavaScript- en CSS-bestanden.
template/: Bevat HTML-sjablonen voor verschillende gebruikersrollen.

### Licentie
Dit project is gelicentieerd onder de MIT-licentie. Zie het LICENSE bestand voor details.