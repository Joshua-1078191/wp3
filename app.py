from flask import Flask, render_template, redirect, url_for, request, session, jsonify, flash
from sqlalchemy.orm import sessionmaker, Query
from lib.database_generator import engine, Organisatie, Beheerder, Ervaringsdeskundige, Onderzoek
from src.user import UserLogin, UserRegistration, UserProfile, AdminActions
from werkzeug.security import check_password_hash
import random
import string
import secrets
from datetime import datetime
from sqlalchemy import or_

app = Flask(__name__, template_folder='template')
app.secret_key = 'your_secret_key'

# Creating session
Session = sessionmaker(bind=engine)
db_session = Session()

user_login = UserLogin()
user_registration = UserRegistration()
user_profile = UserProfile()

admin_actions = AdminActions()

@app.route('/')
def home():
    return render_template('user/home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        if user_type == 'admin':
            return redirect(url_for('admin_login'))
        elif user_type == 'organization':
            return redirect(url_for('organization_login'))
        elif user_type == 'ervaringsdeskundige':
            return redirect(url_for('ervaringsdeskundige_login'))
    return render_template('user/login_choice.html')

@app.route('/admin_login', methods=['POST'])
def admin_login():
    email = request.form.get('email')
    password = request.form.get('password')
    user_login = UserLogin()
    user_id, user_type = user_login.admin_login(email, password)
    if user_id:
        session['user_id'] = user_id
        session['user_type'] = user_type
        admin = db_session.query(Beheerder).get(user_id)
        session['admin_name'] = f"{admin.voornaam} {admin.achternaam}"
        return redirect(url_for('admin_index'))
    flash('Login failed. Please check your email and password.', 'error')
    return redirect(url_for('login'))

@app.route('/organization_login', methods=['POST'])
def organization_login():
    name = request.form.get('name')
    api_key = request.form.get('api_key')
    user_login = UserLogin()
    organization_id, user_type = user_login.organization_login(name, api_key)
    if organization_id:
        session['user_id'] = organization_id
        session['user_type'] = user_type
        organization = db_session.query(Organisatie).get(organization_id)
        session['organization'] = {'naam': organization.naam}
        return redirect(url_for('user_index'))
    flash('Login failed. Please check your organization name and API key.', 'error')
    return redirect(url_for('login'))

@app.route('/ervaringsdeskundige_login', methods=['POST'])
def ervaringsdeskundige_login():
    api_key = request.form.get('api_key')
    email = request.form.get('email')

    user_id, user_type, full_name = user_login.ervaringsdeskundige_login(api_key, email)

    if user_id:
        session['user_id'] = user_id
        session['user_type'] = 'ervaringsdeskundige'
        session['full_name'] = full_name
        return redirect(url_for('user_index'))
    elif user_type == 'not_approved':
        flash('Your account is pending approval. Please wait for admin confirmation.', 'warning')
    else:
        flash('Login failed. Please check your API key and email.', 'error')
    return redirect(url_for('login'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form_data = request.form.to_dict()

        # Check if email already exists
        existing_user = db_session.query(Ervaringsdeskundige).filter_by(emailadres=form_data['emailadres']).first()

        if existing_user:
            flash('Email address is already registered. Please use a different email.', 'error')
            return redirect(url_for('register'))

        user_registration = UserRegistration()
        user_registration.register(form_data)
        flash('Registration successful. Please wait for admin approval.', 'success')

    return render_template('user/register.html')



@app.route('/user/user_index')
def user_index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_type = session.get('user_type')
    user_info = {}

    if user_type == 'admin':
        admin = db_session.query(Beheerder).filter_by(id=session['user_id']).first()
        user_info = {
            'type': 'Admin',
            'name': f"{admin.voornaam} {admin.achternaam}"
        }
    elif user_type == 'organization':
        org = db_session.query(Organisatie).filter_by(id=session['user_id']).first()
        user_info = {
            'type': 'Organisatie',
            'name': org.naam
        }
    elif user_type == 'ervaringsdeskundige':
        erv = db_session.query(Ervaringsdeskundige).filter_by(id=session['user_id']).first()
        user_info = {
            'type': 'Ervaringsdeskundige',
            'name': f"{erv.voornaam} {erv.achternaam}"
        }
    else:
        return redirect(url_for('login'))

    return render_template('user/user_index.html', user_info=user_info)

@app.route('/admin_index', methods=['GET', 'POST'])
def admin_index():
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    admin_name = get_admin_name() 
    
    if request.method == 'POST':
        onderzoek_id = request.form.get('onderzoek_id')
        action = request.form.get('action')
        
        onderzoek = db_session.query(Onderzoek).get(onderzoek_id)
        if not onderzoek:
            flash('Onderzoek niet gevonden.', 'error')
            return redirect(url_for('admin_index'))
        
        if action == 'approve':
            onderzoek.status = 'open'
            onderzoek.beheerder_id = session['user_id']  
            onderzoek.datum_vanaf = datetime.now()
            onderzoek.datum_tot = datetime.now()  
            onderzoek.type_onderzoek = 1        
            db_session.commit()
            flash('Onderzoek is goedgekeurd!', 'success')
        
        elif action == 'disapprove':

            db_session.delete(onderzoek)
            db_session.commit()
            flash('Onderzoek is afgekeurd en verwijderd!', 'success')
        
        return redirect(url_for('admin_index'))
    

    pending_onderzoeken = db_session.query(Onderzoek).filter_by(status='pending').all()
    
    return render_template(
        'admin/admin_index.html',
        admin_name=admin_name,
        pending_onderzoeken=pending_onderzoeken
    )

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        form_data = {
            'voornaam': request.form.get('voornaam'),
            'achternaam': request.form.get('achternaam'),
            'emailadres': request.form.get('email')
        }
        user_profile.update_admin_profile(session['user_id'], form_data)
        return redirect(url_for('profile'))

    admin_profile = user_profile.get_admin_profile(session['user_id'])
    admin_name = get_admin_name()
    return render_template('admin/profile.html', beheerder=admin_profile, admin_name=admin_name)

@app.route('/accounts')
def accounts():
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    
    admin_name = get_admin_name()
    search_query = request.args.get('search', '')
    account_type = request.args.get('account_type', 'all')

    # Start with query objects
    ervaringsdeskundigen = db_session.query(Ervaringsdeskundige).filter_by(accepteerd=True)
    beheerders = db_session.query(Beheerder)
    organisaties = db_session.query(Organisatie)

    if search_query:
        ervaringsdeskundigen = ervaringsdeskundigen.filter(
            (Ervaringsdeskundige.voornaam.ilike(f'%{search_query}%')) |
            (Ervaringsdeskundige.achternaam.ilike(f'%{search_query}%')) |
            (Ervaringsdeskundige.emailadres.ilike(f'%{search_query}%'))
        )
        beheerders = beheerders.filter(
            (Beheerder.voornaam.ilike(f'%{search_query}%')) |
            (Beheerder.achternaam.ilike(f'%{search_query}%')) |
            (Beheerder.emailadres.ilike(f'%{search_query}%'))
        )
        organisaties = organisaties.filter(
            (Organisatie.naam.ilike(f'%{search_query}%')) 
        )

    if account_type != 'all':
        if account_type == 'expert':
            beheerders = beheerders.filter(False)
            organisaties = organisaties.filter(False)
        elif account_type == 'admin':
            ervaringsdeskundigen = ervaringsdeskundigen.filter(False)
            organisaties = organisaties.filter(False)
        elif account_type == 'organization':
            ervaringsdeskundigen = ervaringsdeskundigen.filter(False)
            beheerders = beheerders.filter(False)

    # Execute the queries to get the results
    ervaringsdeskundigen = ervaringsdeskundigen.all()
    beheerders = beheerders.all()
    organisaties = organisaties.all()

    return render_template('admin/accounts.html', 
                           admin_name=admin_name,
                           ervaringsdeskundigen=ervaringsdeskundigen, 
                           beheerders=beheerders, 
                           organisaties=organisaties,
                           search_query=search_query,
                           account_type=account_type)



@app.route('/generate_api_key', methods=['POST'])
def generate_api_key():
    account_id = request.form.get('account_id')
    account_type = request.form.get('account_type')

    if account_type == 'organization':
        account = db_session.query(Organisatie).get(account_id)
    elif account_type == 'ervaringsdeskundige':
        account = db_session.query(Ervaringsdeskundige).get(account_id)
    else:
        return jsonify({'success': False, 'message': 'Invalid account type'})

    if account:
        new_api_key = secrets.token_hex(16)
        account.api_key = new_api_key
        db_session.commit()
        return jsonify({'success': True, 'api_key': new_api_key})
    else:
        return jsonify({'success': False, 'message': 'Account not found'})


@app.route('/user/onderzoeken')
def onderzoeken():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_type = session.get('user_type')
    user_info = {}
    if user_type == 'admin':
        admin = db_session.query(Beheerder).filter_by(id=session['user_id']).first()
        user_info = {'type': 'Admin','name': f"{admin.voornaam} {admin.achternaam}"}
    elif user_type == 'organization':
        org = db_session.query(Organisatie).filter_by(id=session['user_id']).first()
        user_info = {'type': 'Organisatie','name': org.naam}
    elif user_type == 'ervaringsdeskundige':
        erv = db_session.query(Ervaringsdeskundige).filter_by(id=session['user_id']).first()
        user_info = {'type': 'Ervaringsdeskundige','name': f"{erv.voornaam} {erv.achternaam}"}
    else:
        return redirect(url_for('login'))
    

    from lib.database_generator import Onderzoek  
    approved_onderzoeken = db_session.query(Onderzoek).filter(Onderzoek.status.in_(['open','bezig'])).all()
    
    return render_template('user/onderzoeken.html',
                           user_info=user_info,
                           onderzoeken=approved_onderzoeken)

@app.route('/api/onderzoek/<int:onderzoek_id>', methods=['GET'])
def get_onderzoek_details(onderzoek_id):
    """Возвращает JSON с детальной информацией об исследовании."""
    onderzoek = db_session.query(Onderzoek).get(onderzoek_id)
    if not onderzoek:
        return jsonify(success=False, message="Onderzoek niet gevonden"), 404

    data = {
        'id': onderzoek.id,
        'titel': onderzoek.titel,
        'status': onderzoek.status,
        'beschrijving': onderzoek.beschrijving or '',
        'datum_vanaf': onderzoek.datum_vanaf.isoformat() if onderzoek.datum_vanaf else '',
        'datum_tot': onderzoek.datum_tot.isoformat() if onderzoek.datum_tot else '',
        'type_onderzoek': onderzoek.type_onderzoek,  
        'locatie': onderzoek.locatie or '',
        'beheerder': (f"{onderzoek.beheerder.voornaam} {onderzoek.beheerder.achternaam}"
                      if onderzoek.beheerder else ''),
        'organisatie': (onderzoek.organisatie.naam
                        if onderzoek.organisatie else ''),
        'ervaringsdeskundige': (f"{onderzoek.ervaringsdeskundige.voornaam} {onderzoek.ervaringsdeskundige.achternaam}"
                                if onderzoek.ervaringsdeskundige else '')
    }

    return jsonify(success=True, onderzoek=data)

@app.route('/user/onderzoeken/new', methods=['POST'])
def new_onderzoek():
    """Ervaringsdeskundige maakt een nieuw onderzoek aan met status 'pending'."""

    if 'user_id' not in session:
        return redirect(url_for('login'))


    if session.get('user_type') != 'ervaringsdeskundige':
        flash('Alleen Ervaringsdeskundigen kunnen een onderzoek aanmaken.', 'error')
        return redirect(url_for('onderzoeken'))


    titel = request.form.get('titel', '').strip()
    beschrijving = request.form.get('beschrijving', '').strip()
    if not titel or not beschrijving:
        flash('Vul a.u.b. titel en beschrijving in.', 'error')
        return redirect(url_for('onderzoeken'))


    now = datetime.now()


    default_admin_id = 1       
    default_org_id   = 1        

   
    erv_id = session['user_id']

    nieuw = Onderzoek(
        titel=titel,
        beschrijving=beschrijving,
        status='pending',
        beschikbaar=True,       
        datum_vanaf=now,
        datum_tot=now,
        type_onderzoek=1,        
        locatie=None,            
        met_beloning=False,
        beloning=None,
        doelgroep_leeftijd_van=None,
        doelgroep_leeftijd_tot=None,
        doelgroep_beperking=None,
        
        beheerder_id=default_admin_id,
        organisatie_id=default_org_id,
        ervaringsdeskundige_id=erv_id
    )

    try:
        db_session.add(nieuw)
        db_session.commit()
        flash('Onderzoek is aangemaakt en wacht nu op goedkeuring van de admin.', 'success')
    except Exception as e:
        db_session.rollback()
        flash(f'Fout bij het aanmaken van onderzoek: {str(e)}', 'error')

    return redirect(url_for('onderzoeken'))

@app.route('/user/account')
def account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_type = session.get('user_type')
    account = None
    user_info = {}

    if user_type == 'admin':
        admin = db_session.query(Beheerder).filter_by(id=session['user_id']).first()
        if admin:
            account = admin
            user_info = {
                'type': 'Admin',
                'name': f"{admin.voornaam} {admin.achternaam}"
            }
    elif user_type == 'organization':
        org = db_session.query(Organisatie).filter_by(id=session['user_id']).first()
        if org:
            account = org
            user_info = {
                'type': 'Organisatie',
                'name': org.naam
            }
    elif user_type == 'ervaringsdeskundige':
        erv = db_session.query(Ervaringsdeskundige).filter_by(id=session['user_id']).first()
        if erv:
            account = erv
            user_info = {
                'type': 'Ervaringsdeskundige',
                'name': f"{erv.voornaam} {erv.achternaam}"
            }


    if not account:
        return redirect(url_for('login'))

    return render_template(
        'user/account.html',
        account=account,
        user_type=user_type,
        user_info=user_info
    )



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/toggle_edit_mode', methods=['POST'])
def toggle_edit_mode():
    edit_mode = request.json.get('editMode')
    return jsonify({'success': True, 'editMode': edit_mode})

def get_admin_name():
    if 'user_id' in session and session.get('user_type') == 'admin':
        admin = db_session.query(Beheerder).filter_by(id=session['user_id']).first()
        return f"{admin.voornaam} {admin.achternaam}"
    return None

@app.route('/pending', methods=['GET', 'POST'])
def pending():
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))

    admin_name = get_admin_name()

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        action = request.form.get('action')

        if action == 'approve':
            if admin_actions.approve_ervaringsdeskundige(user_id):
                flash('Ervaringsdeskundige approved successfully', 'success')
            else:
                flash('Failed to approve Ervaringsdeskundige', 'error')
        elif action == 'disapprove':
            if admin_actions.disapprove_ervaringsdeskundige(user_id):
                flash('Ervaringsdeskundige disapproved successfully', 'success')
            else:
                flash('Failed to disapprove Ervaringsdeskundige', 'error')
        return redirect(url_for('pending'))
    
    pending_users = admin_actions.get_pending_ervaringsdeskundigen()
    return render_template('admin/pending.html', admin_name=admin_name, pending_users=pending_users)


def admin_accounts():
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))

    admin_name = get_admin_name()
    ervaringsdeskundigen = db_session.query(Ervaringsdeskundige).all()
    beheerders = db_session.query(Beheerder).all()
    organisaties = db_session.query(Organisatie).all()

    return render_template('admin/accounts.html', 
                           admin_name=admin_name, 
                           ervaringsdeskundigen=ervaringsdeskundigen,
                           beheerders=beheerders,
                           organisaties=organisaties)



@app.route('/add_organization', methods=['GET', 'POST'])
def add_organization():
    if request.method == 'POST':
        new_organization = Organisatie(
            naam=request.form['naam'],
            website=request.form['website'],
            beschrijving=request.form['beschrijving'],
            contactpersoon=request.form['contactpersoon'],
            telefoonnummer=request.form['telefoonnummer'],
            overige_details=request.form['overige_details'],
            api_key=secrets.token_hex(16)
        )

        try:
            db_session.add(new_organization)
            db_session.commit()
            flash('Organization added successfully!', 'success')
            return redirect(url_for('accounts'))
        except Exception as e:
            db_session.rollback()
            flash(f'Error adding organization: {str(e)}', 'error')

    return render_template('admin/add_organization.html')


@app.route('/get_account/<account_type>/<int:account_id>')
def get_account(account_type, account_id):
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    if account_type == 'organization':
        account = db_session.query(Organisatie).filter_by(id=account_id).first()
    elif account_type == 'ervaringsdeskundige':
        account = db_session.query(Ervaringsdeskundige).filter_by(id=account_id).first()
    else:
        return jsonify({'success': False, 'message': 'Invalid account type'}), 400

    if account:
        return jsonify({
            'success': True,
            'account': {
                'name': account.naam if account_type == 'organization' else f"{account.voornaam} {account.achternaam}",
                'email': account.emailadres
            }
        })
    else:
        return jsonify({'success': False, 'message': 'Account not found'}), 404

@app.route('/edit_account/<string:account_type>/<int:account_id>', methods=['GET', 'POST'])
def edit_account(account_type, account_id):
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    admin_name = get_admin_name()

    if account_type == 'organization':
        account = db_session.query(Organisatie).get(account_id)
    elif account_type == 'ervaringsdeskundige':
        account = db_session.query(Ervaringsdeskundige).get(account_id)
    else:
        flash('Invalid account type', 'error')
        return redirect(url_for('accounts'))

    if not account:
        flash('Account not found', 'error')
        return redirect(url_for('accounts'))

    if request.method == 'POST':
        try:
            if account_type == 'organization':
                account.naam = request.form['naam']
                account.website = request.form['website']
                account.beschrijving = request.form['beschrijving']
                account.contactpersoon = request.form['contactpersoon']
                account.telefoonnummer = request.form['telefoonnummer']
                account.overige_details = request.form['overige_details']
            elif account_type == 'ervaringsdeskundige':
                account.voornaam = request.form['voornaam']
                account.achternaam = request.form['achternaam']
                account.postcode = request.form['postcode']
                account.geslacht = request.form['geslacht']
                account.emailadres = request.form['emailadres']
                account.telefoonnummer = request.form['telefoonnummer']
                account.geboortedatum = datetime.strptime(request.form['geboortedatum'], '%Y-%m-%d').date()

            db_session.commit()
            flash('Account updated successfully', 'success')
            return redirect(url_for('accounts'))
        except Exception as e:
            db_session.rollback()
            flash(f'Error updating account: {str(e)}', 'error')

    return render_template('admin/edit_account.html', account=account, account_type=account_type, admin_name=admin_name, )



if __name__ == '__main__':
    app.run(debug=True)
