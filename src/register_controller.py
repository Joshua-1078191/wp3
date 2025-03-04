from flask import Blueprint, request, redirect, url_for, render_template
from lib.database_generator import db_session, Ervaringsdeskundige
from datetime import datetime

register_bp = Blueprint('register_bp', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve form data
        voornaam = request.form.get('voornaam')
        achternaam = request.form.get('achternaam')
        postcode = request.form.get('postcode')
        geslacht = request.form.get('geslacht')
        emailadres = request.form.get('emailadres')
        telefoonnummer = request.form.get('telefoonnummer')
        geboortedatum = datetime.strptime(request.form.get('geboortedatum'), '%Y-%m-%d').date()
        gebruikte_hulpmiddelen = request.form.get('gebruikte_hulpmiddelen')
        kort_voorstellen = request.form.get('kort_voorstellen')
        bijzonderheden = request.form.get('bijzonderheden')
        akkoord_voorwaarden = request.form.get('akkoord_voorwaarden') == 'on'
        toezichthouder = request.form.get('toezichthouder') == 'on'
        naam_toezichthouder = request.form.get('naam_toezichthouder')
        email_toezichthouder = request.form.get('email_toezichthouder')
        telefoon_toezichthouder = request.form.get('telefoon_toezichthouder')
        beperking_id = request.form.get('beperking_id')
        if beperking_id is None:
            beperking_id = 1  # Default value

        # Create a new Ervaringsdeskundige instance
        new_ervaringsdeskundige = Ervaringsdeskundige(
            voornaam=voornaam,
            achternaam=achternaam,
            postcode=postcode,
            geslacht=geslacht,
            emailadres=emailadres,
            telefoonnummer=telefoonnummer,
            geboortedatum=geboortedatum,
            gebruikte_hulpmiddelen=gebruikte_hulpmiddelen,
            kort_voorstellen=kort_voorstellen,
            bijzonderheden=bijzonderheden,
            akkoord_voorwaarden=akkoord_voorwaarden,
            toezichthouder=toezichthouder,
            naam_toezichthouder=naam_toezichthouder,
            email_toezichthouder=email_toezichthouder,
            telefoon_toezichthouder=telefoon_toezichthouder,
            beperking_id=beperking_id
        )

        # Add to the session and commit
        db_session.add(new_ervaringsdeskundige)
        db_session.commit()

        return redirect(url_for('register_bp.register'))
    return render_template('register.html')
