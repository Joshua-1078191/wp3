from werkzeug.security import check_password_hash
from lib.database_generator import db_session, Beheerder, Organisatie, Ervaringsdeskundige
from src.password_security import hash_password, verify_password
import secrets
from datetime import datetime

class UserLogin:
    def admin_login(self, email, password):
        """
        Authenticate admin user with email and password.
        Uses secure password hashing with salt for verification.
        
        Args:
            email: Admin email address
            password: Plain text password to verify
            
        Returns:
            Tuple of (user_id, user_type) if successful, (None, None) otherwise
        """
        admin = db_session.query(Beheerder).filter_by(emailadres=email).first()
        if admin and check_password_hash(admin.wachtwoord_hash, password):
            return admin.id, 'admin'
        return None, None

    def organization_login(self, name, api_key):
        organization = db_session.query(Organisatie).filter_by(naam=name).first()
        if organization and organization.api_key == api_key:
            return organization.id, 'organization'
        return None, None

    def generate_api_key(self, name):
        organization = db_session.query(Organisatie).filter_by(naam=name).first()
        if organization:
            api_key = secrets.token_hex(16)
            organization.api_key = api_key
            db_session.commit()
            return api_key
        return None
    def ervaringsdeskundige_login(self, api_key, email):
            ervaringsdeskundige = db_session.query(Ervaringsdeskundige).filter_by(
                emailadres=email
            ).first()
            
            if ervaringsdeskundige and ervaringsdeskundige.api_key == api_key:
                if ervaringsdeskundige.accepteerd:
                    full_name = f"{ervaringsdeskundige.voornaam} {ervaringsdeskundige.achternaam}"
                    return ervaringsdeskundige.id, 'ervaringsdeskundige', full_name
                else:
                    return None, 'not_approved', None
            return None, None, None



class UserProfile:
    def get_admin_profile(self, user_id):
        return db_session.query(Beheerder).filter_by(id=user_id).first()

    def update_admin_profile(self, user_id, form_data):
        admin = db_session.query(Beheerder).filter_by(id=user_id).first()
        if admin:
            admin.voornaam = form_data.get('voornaam', admin.voornaam)
            admin.achternaam = form_data.get('achternaam', admin.achternaam)
            admin.emailadres = form_data.get('emailadres', admin.emailadres)
            db_session.commit()

class UserRegistration:
    def register(self, form_data):
        toezichthouder_checked = form_data.get('toezichthouder') == 'on'
        new_ervaringsdeskundige = Ervaringsdeskundige(
            voornaam=form_data['voornaam'],
            achternaam=form_data['achternaam'],
            postcode=form_data['postcode'],
            geslacht=form_data['geslacht'],
            emailadres=form_data['emailadres'],
            telefoonnummer=form_data['telefoonnummer'],
            geboortedatum=datetime.strptime(form_data['geboortedatum'], '%Y-%m-%d').date(),
            gebruikte_hulpmiddelen=form_data.get('gebruikte_hulpmiddelen'),
            kort_voorstellen=form_data.get('kort_voorstellen'),
            bijzonderheden=form_data.get('bijzonderheden'),
            akkoord_voorwaarden=form_data.get('akkoord_voorwaarden') == 'on',
            toezichthouder=toezichthouder_checked,
            naam_toezichthouder=form_data.get('naam_toezichthouder') if toezichthouder_checked else None,
            email_toezichthouder=form_data.get('email_toezichthouder') if toezichthouder_checked else None,
            telefoon_toezichthouder=form_data.get('telefoon_toezichthouder') if toezichthouder_checked else None,
            beperking_id=form_data.get('beperking_id', 1),
            accepteerd=None,
            api_key=None
        )
        db_session.add(new_ervaringsdeskundige)
        db_session.commit()

class AdminActions:
    def approve_ervaringsdeskundige(self, user_id):
        user = db_session.query(Ervaringsdeskundige).get(user_id)
        if user:
            user.accepteerd = True
            user.api_key = secrets.token_hex(32)
            db_session.commit()
            return True
        return False
    def disapprove_ervaringsdeskundige(self, user_id):
        ervaringsdeskundige = db_session.query(Ervaringsdeskundige).filter_by(id=user_id).first()
        if ervaringsdeskundige:
            ervaringsdeskundige.accepteerd = False
            db_session.commit()
            return True
        return False

    def get_pending_ervaringsdeskundigen(self):
        return db_session.query(Ervaringsdeskundige).filter_by(accepteerd=None).all()