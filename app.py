from flask import Flask, render_template, redirect, url_for, request, session
from sqlalchemy.orm import sessionmaker
from lib.database_generator import engine, Organisatie, Beheerder, Ervaringsdeskundige
from src.register_controller import register_bp
from src.login_controller import login_bp
from werkzeug.security import check_password_hash

app = Flask(__name__, template_folder='template')
app.secret_key = 'your_secret_key'

# Creating session
Session = sessionmaker(bind=engine)
db_session = Session()

app.register_blueprint(register_bp)
app.register_blueprint(login_bp)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        if user_type == 'admin':
            return redirect(url_for('admin_login'))
        elif user_type == 'organization':
            return redirect(url_for('organization_login'))
    return render_template('login_choice.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check credentials
        admin = db_session.query(Beheerder).filter_by(emailadres=email).first()
        if admin and check_password_hash(admin.wachtwoord_hash, password):
            session['user_id'] = admin.id
            session['user_type'] = 'admin'
            return redirect(url_for('index'))
    return render_template('admin_login.html')

@app.route('/organization_login', methods=['GET', 'POST'])
def organization_login():
    if request.method == 'POST':
        name = request.form.get('name')
        api_key = request.form.get('api_key')
        organization = db_session.query(Organisatie).filter_by(naam=name).first()
        if organization and organization.api_key == api_key:
            session['user_id'] = organization.id
            session['user_type'] = 'organization'
            return redirect(url_for('index'))
    return render_template('organization_login.html')

@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_type = session.get('user_type')
    return render_template('index.html', user_type=user_type)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
