from lib.database_generator import db_session, Beheerder, Organisatie
from src.password_security import hash_password

# Create a new admin user with securely hashed password
# Password is hashed using scrypt with automatic salt generation
# See src/password_security.py for detailed security documentation
admin = Beheerder(
    voornaam='test',
    achternaam='monkey',
    emailadres='123@123.com',
    wachtwoord_hash=hash_password('password123')
)

# Add to the session and commit
db_session.add(admin)
db_session.commit()

print("Dummy admin user added successfully!")

