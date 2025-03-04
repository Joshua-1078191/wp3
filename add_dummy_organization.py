from lib.database_generator import db_session, Organisatie
import secrets

# Create a new dummy organization
organization = Organisatie(
    naam='Dummy Organization',
    type=True,  # Assuming type is a boolean
    website='https://dummyorg.com',
    beschrijving='A dummy organization for testing purposes.',
    contactpersoon='contact@dummyorg.com',
    telefoonnummer='1234567890',
    overige_details='Some additional details about the organization.',
    api_key=secrets.token_hex(16)
)

# Add to the session and commit
db_session.add(organization)
db_session.commit()

print("Dummy organization added successfully!")
