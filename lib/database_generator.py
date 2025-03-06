from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime
import secrets

Base = declarative_base()


class Organisatie(Base):
    __tablename__ = 'organisatie'

    id = Column(Integer, primary_key=True, autoincrement=True)
    naam = Column(String, nullable=False, unique=True)
    website = Column(String, nullable=True)
    beschrijving = Column(String, nullable=True)
    contactpersoon = Column(String, nullable=True)
    telefoonnummer = Column(String, nullable=True)
    overige_details = Column(String, nullable=True)
    api_key = Column(String(32), unique=True, nullable=False)
    onderzoeken = relationship("Onderzoek", back_populates="organisatie")


#  Beheerder Table
class Beheerder(Base):
    __tablename__ = 'beheerder'

    id = Column(Integer, primary_key=True, autoincrement=True)
    voornaam = Column(String, nullable=False)
    achternaam = Column(String, nullable=False)
    emailadres = Column(String, nullable=False, unique=True)
    wachtwoord_hash = Column(String, nullable=False)  
    actief = Column(Boolean, default=True)
    aangemaakt_op = Column(DateTime, default=datetime.utcnow)

    onderzoeken = relationship("Onderzoek", back_populates="beheerder")


# 🔬 Onderzoek Table
class Onderzoek(Base):
    __tablename__ = 'onderzoeken'

    id = Column(Integer, primary_key=True, autoincrement=True)
    titel = Column(String, nullable=False)
    status = Column(String, nullable=False)
    beschikbaar = Column(Boolean, nullable=False, default=True)
    beschrijving = Column(String, nullable=True)
    datum_vanaf = Column(DateTime, nullable=False)
    datum_tot = Column(DateTime, nullable=False)
    type_onderzoek = Column(Integer, nullable=False)  
    locatie = Column(String, nullable=True)
    met_beloning = Column(Boolean, nullable=False, default=False)
    beloning = Column(String, nullable=True)
    doelgroep_leeftijd_van = Column(Integer, nullable=True)
    doelgroep_leeftijd_tot = Column(Integer, nullable=True)
    doelgroep_beperking = Column(Integer, nullable=True)

    # Foreign Keys
    beheerder_id = Column(Integer, ForeignKey('beheerder.id'), nullable=False)
    organisatie_id = Column(Integer, ForeignKey('organisatie.id'), nullable=False)
    ervaringsdeskundige_id = Column(Integer, ForeignKey('ervaringsdeskundige.id'), nullable=False)

    # Relationships
    beheerder = relationship("Beheerder", back_populates="onderzoeken")
    organisatie = relationship("Organisatie", back_populates="onderzoeken")
    ervaringsdeskundige = relationship("Ervaringsdeskundige", back_populates="onderzoeken")


class Beperking(Base):
    __tablename__ = 'beperkingen'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_beperking = Column(String, nullable=False)
    beperking = Column(String, nullable=False)

    ervaringsdeskundigen = relationship("Ervaringsdeskundige", back_populates="beperking")


class TypeOnderzoek(Base):
    __tablename__ = 'type_onderzoek'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_onderzoek = Column(String, nullable=False)
    beschrijving = Column(String, nullable=False)

    ervaringsdeskundigen = relationship("Ervaringsdeskundige", back_populates="type_onderzoek")


class Ervaringsdeskundige(Base):
    __tablename__ = 'ervaringsdeskundige'

    id = Column(Integer, primary_key=True, autoincrement=True)
    voornaam = Column(String, nullable=False)
    achternaam = Column(String, nullable=False)
    postcode = Column(String, nullable=False)
    geslacht = Column(String, nullable=False)
    emailadres = Column(String, nullable=False, unique=True)
    telefoonnummer = Column(String, nullable=True, unique=True)
    geboortedatum = Column(Date, nullable=False)
    gebruikte_hulpmiddelen = Column(String, nullable=True)
    kort_voorstellen = Column(String, nullable=True)
    bijzonderheden = Column(String, nullable=True)
    akkoord_voorwaarden = Column(Boolean, nullable=False, default=False)
    toezichthouder = Column(Boolean, nullable=False, default=False)
    naam_toezichthouder = Column(String, nullable=True)
    email_toezichthouder = Column(String, nullable=True)
    telefoon_toezichthouder = Column(String, nullable=True)
    voorkeur_benadering = Column(String, nullable=False, default='email')
    type_onderzoek_id = Column(Integer, ForeignKey('type_onderzoek.id'), nullable=True)
    beperking_id = Column(Integer, ForeignKey('beperkingen.id'), nullable=False)
    bijzonderheden_beschikbaarheid = Column(String, nullable=True)
    accepteerd = Column(Boolean, nullable=True)
    api_key = Column(String(32), nullable=False, unique=True, default=lambda: secrets.token_hex(16))
    # Relationships
    beperking = relationship("Beperking", back_populates="ervaringsdeskundigen")
    type_onderzoek = relationship("TypeOnderzoek", back_populates="ervaringsdeskundigen")
    onderzoeken = relationship("Onderzoek", back_populates="ervaringsdeskundige", foreign_keys="[Onderzoek.ervaringsdeskundige_id]")
    onderzoeken_2 = relationship("OnderzoekErvaringsdeskundige", back_populates="ervaringsdeskundige")

    __table_args__ = (
        CheckConstraint("voorkeur_benadering IN ('telefonisch', 'email')", name="check_voorkeur_benadering"),
    )


class OnderzoekErvaringsdeskundige(Base):
    __tablename__ = 'onderzoek_ervaringsdeskundige'

    onderzoek_id = Column(Integer, ForeignKey('onderzoeken.id'), primary_key=True)
    ervaringsdeskundige_id = Column(Integer, ForeignKey('ervaringsdeskundige.id'), primary_key=True)
    inschrijfdatum = Column(Date, nullable=False)

    ervaringsdeskundige = relationship("Ervaringsdeskundige", back_populates="onderzoeken_2")

# Database connection setup
DATABASE_URL = "sqlite:///databases/database.db"
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)

# Creating session
Session = sessionmaker(bind=engine)
db_session = Session()

print("✅ Database and tables created successfully!")

__all__ = ['db_session', 'Ervaringsdeskundige', 'User', 'validate_api_key']