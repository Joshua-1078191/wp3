from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from sqlalchemy.orm import sessionmaker
from lib.database_generator import engine, Organisatie, Beheerder, Ervaringsdeskundige
from src.user import UserLogin, UserRegistration, UserProfile
from werkzeug.security import check_password_hash

app = Flask(__name__, template_folder='template')
app.secret_key = 'your_secret_key'

# Creating session
Session = sessionmaker(bind=engine)
db_session = Session()

user_login = UserLogin()
user_registration = UserRegistration()
user_profile = UserProfile()

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
    return render_template('user/login_choice.html')

@app.route('/admin_login', methods=['POST'])
def admin_login():
    email = request.form.get('email')
    password = request.form.get('password')
    user_id, user_type = user_login.admin_login(email, password)
    if user_id:
        session['user_id'] = user_id
        session['user_type'] = user_type
        return redirect(url_for('admin_index'))
    return redirect(url_for('login'))

@app.route('/organization_login', methods=['POST'])
def organization_login():
    name = request.form.get('name')
    api_key = request.form.get('api_key')
    user_id, user_type = user_login.organization_login(name, api_key)
    if user_id:
        session['user_id'] = user_id
        session['user_type'] = user_type
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/admin/generate_api_key', methods=['POST'])
def admin_generate_api_key():
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return 'Unauthorized', 403

    name = request.form.get('name')
    api_key = user_login.generate_api_key(name)
    if api_key:
        return f'API key generated for {name}: {api_key}', 200
    return 'Organization not found', 404

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form_data = request.form
        user_registration.register(form_data)
        return redirect(url_for('register'))
    return render_template('user/register.html')

@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_type = session.get('user_type')
    if user_type == 'admin':
        user = db_session.query(Beheerder).filter_by(id=session['user_id']).first()
        session_name = user.voornaam + ' ' + user.achternaam
    elif user_type == 'organization':
        user = db_session.query(Organisatie).filter_by(id=session['user_id']).first()
        session_name = user.naam
    return render_template('user/user_index.html', user_type=user_type, session_name=session_name)

@app.route('/admin_index')
def admin_index():
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    admin_name = get_admin_name()
    return render_template('admin/admin_index.html', admin_name=admin_name)

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
    # Add logic to retrieve and display the accounts information
    return render_template('admin/table.html', admin_name=admin_name)

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

if __name__ == '__main__':
    app.run(debug=True)
