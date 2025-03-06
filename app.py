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
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_type = session.get('user_type')
    return render_template('admin/admin_index.html', user_type=user_type)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Add logic to retrieve and display the profile information
    return render_template('admin/profile.html')

@app.route('/accounts')
def accounts():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Add logic to retrieve and display the accounts information
    return render_template('admin/table.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
