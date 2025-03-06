from lib.database_generator import db_session, Beheerder, Organisatie
from werkzeug.security import generate_password_hash

# Create a new admin user
admin = Beheerder(
    voornaam='test',
    achternaam='monkey',
    emailadres='123@123.com',
    wachtwoord_hash=generate_password_hash('password123')
)

# Add to the session and commit
db_session.add(admin)
db_session.commit()

print("Dummy admin user added successfully!")

