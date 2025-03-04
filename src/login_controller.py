from flask import Blueprint, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from lib.database_generator import db_session, Beheerder, Organisatie
import secrets

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/admin_login', methods=['POST'])
def admin_login():
    email = request.form.get('email')
    password = request.form.get('password')
    admin = db_session.query(Beheerder).filter_by(emailadres=email).first()
    if admin and check_password_hash(admin.wachtwoord_hash, password):
        session['user_id'] = admin.id
        session['user_type'] = 'admin'
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@login_bp.route('/organization_login', methods=['POST'])
def organization_login():
    name = request.form.get('name')
    api_key = request.form.get('api_key')
    organization = db_session.query(Organisatie).filter_by(naam=name).first()
    if organization and organization.api_key == api_key:
        session['user_id'] = organization.id
        session['user_type'] = 'organization'
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@login_bp.route('/admin/generate_api_key', methods=['POST'])
def admin_generate_api_key():
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return 'Unauthorized', 403

    name = request.form.get('name')
    organization = db_session.query(Organisatie).filter_by(naam=name).first()
    if organization:
        # Generate a new API key
        api_key = secrets.token_hex(16)
        organization.api_key = api_key
        db_session.commit()
        return f'API key generated for {organization.naam}: {api_key}', 200
    return 'Organization not found', 404
