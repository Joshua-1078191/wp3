# Salting Implementatie - Wachtwoordbeveiliging
**Student:** Joshua  
**Datum:** 7 oktober 2025  
**Vak:** Web Programming Project 3

---

## 1. Wat is Salting?

**Salt** is een willekeurige reeks karakters die aan elk wachtwoord wordt toegevoegd voordat het wordt gehashed. Dit zorgt ervoor dat twee gebruikers met hetzelfde wachtwoord **verschillende hashes** krijgen.

**Probleem zonder salt:**
- Twee gebruikers met wachtwoord "password123" krijgen identieke hashes
- Aanvaller ziet direct welke gebruikers hetzelfde wachtwoord hebben
- Rainbow table aanvallen zijn mogelijk (vooraf berekende hash-databases)

**Oplossing met salt:**
- Elke gebruiker krijgt een unieke willekeurige salt
- Zelfde wachtwoord resulteert in verschillende hashes
- Rainbow tables zijn nutteloos

---

## 2. Toegevoegde Code

### 2.1 Password Security Module (`src/password_security.py`)

```python
from werkzeug.security import generate_password_hash, check_password_hash

PASSWORD_HASH_METHOD = 'scrypt:32768:8:1'

def hash_password(password: str) -> str:
    return generate_password_hash(password, method=PASSWORD_HASH_METHOD)

def verify_password(password_hash: str, password: str) -> bool:
    return check_password_hash(password_hash, password)
```

**Uitleg:**
- `PASSWORD_HASH_METHOD`: Definieert het hash-algoritme (scrypt) en parameters
- `hash_password()`: Neemt een wachtwoord en maakt er een hash van **met automatische salt**
- `verify_password()`: Controleert of een ingevoerd wachtwoord correct is
- `werkzeug.security`: Python library die de salt automatisch genereert en opslaat

---

### 2.2 Integratie in Login Systeem (`src/user.py`)

**Aangepaste code:**
```python
from src.password_security import hash_password, verify_password

class UserLogin:
    def admin_login(self, email, password):
        admin = db_session.query(Beheerder).filter_by(emailadres=email).first()
        if admin and verify_password(admin.wachtwoord_hash, password):
            return admin.id, 'admin'
        return None, None
```

**Uitleg:**
- Bij login wordt `verify_password()` gebruikt in plaats van directe hash vergelijking
- De functie extraheert automatisch de salt uit de opgeslagen hash
- Herberekent de hash met dezelfde salt en vergelijkt

---

### 2.3 Admin Aanmaken (`add_admin.py`)

```python
from src.password_security import hash_password

admin = Beheerder(
    voornaam='test',
    achternaam='monkey',
    emailadres='123@123.com',
    wachtwoord_hash=hash_password('password123')
)
```

**Uitleg:**
- Bij het aanmaken van een admin wordt `hash_password()` gebruikt
- Het wachtwoord wordt nooit in plaintext opgeslagen
- De hash bevat automatisch een unieke salt

---

## 3. Hoe Werkt Het?

### 3.1 Wachtwoord Opslaan (Registratie)

```
Stap 1: Gebruiker voert wachtwoord in
        Input: "MijnWachtwoord123"

Stap 2: Systeem genereert willekeurige salt
        Salt: "aBc123XyZ" (voorbeeld, in werkelijkheid langer)

Stap 3: Combineer wachtwoord + salt en hash
        scrypt("MijnWachtwoord123" + "aBc123XyZ") = hash

Stap 4: Sla op in database
        Database waarde: "scrypt:32768:8:1$aBc123XyZ$hash..."
                         ↑              ↑           ↑
                      Methode        Salt        Hash
```

### 3.2 Wachtwoord Verifiëren (Login)

```
Stap 1: Gebruiker voert wachtwoord in bij login
        Input: "MijnWachtwoord123"

Stap 2: Haal opgeslagen hash op uit database
        Opgeslagen: "scrypt:32768:8:1$aBc123XyZ$hash..."

Stap 3: Extraheer de salt uit opgeslagen hash
        Salt: "aBc123XyZ"

Stap 4: Bereken hash met ingevoerd wachtwoord + salt
        scrypt("MijnWachtwoord123" + "aBc123XyZ") = nieuwe_hash

Stap 5: Vergelijk nieuwe_hash met opgeslagen hash
        Match? → Login succesvol ✓
        Geen match? → Login geweigerd ✗
```

---

## 4. Praktisch Voorbeeld

### Voorbeeld: Twee Gebruikers, Zelfde Wachtwoord

**ZONDER salt (onveilig):**
```
User A: wachtwoord = "password123"
        hash = "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"

User B: wachtwoord = "password123"  
        hash = "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"
        
→ IDENTIEKE HASHES! Aanvaller ziet dat ze hetzelfde wachtwoord hebben.
```

**MET salt (veilig):**
```
User A: wachtwoord = "password123"
        salt = "aBc123XyZ"
        hash = "scrypt:32768:8:1$aBc123XyZ$d4f6a8b2c5e7..."

User B: wachtwoord = "password123"
        salt = "DeF456UvW"  ← Andere salt!
        hash = "scrypt:32768:8:1$DeF456UvW$h9j2k4m6n8p0..."
        
→ VERSCHILLENDE HASHES! Aanvaller kan niet zien dat ze hetzelfde wachtwoord hebben.
```

---

## 5. Waarom scrypt?

**scrypt** is een "memory-hard" hash algoritme met de volgende eigenschappen:

| Eigenschap | Betekenis |
|------------|-----------|
| **Memory-hard** | Vereist veel geheugen, moeilijk te paralleliseren op GPU's |
| **CPU-intensief** | Langzaam te berekenen, beschermt tegen brute-force |
| **Automatische salt** | Werkzeug genereert en slaat salt automatisch op |
| **Configureerbaar** | Parameters (N=32768) kunnen verhoogd worden voor meer security |

**Parameters uitleg:**
- `N=32768`: Geheugen/CPU cost factor (hoger = veiliger maar langzamer)
- `r=8`: Block size parameter
- `p=1`: Parallelization parameter

---

## 6. Beveiliging Voordelen

### 6.1 Bescherming tegen Rainbow Tables
**Rainbow table** = vooraf berekende database met miljarden wachtwoorden en hun hashes.

- **Zonder salt:** Aanvaller zoekt hash op in rainbow table → instant crack
- **Met salt:** Rainbow table is nutteloos omdat elke salt uniek is

### 6.2 Bescherming tegen Database Leak
Als de database gestolen wordt:

- **Zonder salt:** Alle identieke wachtwoorden zijn zichtbaar en snel te kraken
- **Met salt:** Elke hash moet individueel gekraakt worden (veel tijdrovender)

### 6.3 Bescherming tegen Brute-Force
**Brute-force** = alle mogelijke wachtwoorden proberen.

- **SHA-256 (snel):** GPU kan ~10 miljard hashes/seconde berekenen
- **scrypt (traag):** GPU kan ~1.000 hashes/seconde berekenen (10.000x langzamer!)

---

## 7. Testresultaten

**Test uitvoeren:**
```bash
py src/password_security.py
```

**Resultaat:**
```
Password: password123
Hash 1: scrypt:32768:8:1$iOzx3LrX9QKGJmTS$ac619b5b8e17c791...
Hash 2: scrypt:32768:8:1$ZUayQThgXdkvq5oJ$f2d3f97c351ed464...
Hashes different (salt working): True
Both verify correctly: True
```

**Conclusie:** Zelfde wachtwoord geeft twee verschillende hashes → Salt werkt! ✓

---

## 8. Database Structuur

### Beheerder Tabel
```sql
CREATE TABLE beheerder (
    id INTEGER PRIMARY KEY,
    voornaam VARCHAR,
    achternaam VARCHAR,
    emailadres VARCHAR UNIQUE,
    wachtwoord_hash VARCHAR,  -- Bevat: methode$salt$hash
    actief BOOLEAN
);
```

**Voorbeeld database waarde:**
```
wachtwoord_hash = "scrypt:32768:8:1$aBc123XyZ$d4f6a8b2c5e7..."
```

De `wachtwoord_hash` kolom bevat:
1. Hash methode en parameters (`scrypt:32768:8:1`)
2. Unieke salt (`aBc123XyZ`)
3. Actual hash van wachtwoord+salt (`d4f6a8b2c5e7...`)

Alles in één string, gescheiden door `$` tekens.

---

## 9. Conclusie

### Wat is er toegevoegd?
1. ✓ Central `password_security.py` module met salt functionaliteit
2. ✓ `hash_password()` - genereert hash met automatische unieke salt
3. ✓ `verify_password()` - verifieert wachtwoorden met salt extractie
4. ✓ scrypt algoritme - memory-hard en GPU-resistent
5. ✓ Integratie in login en registratie systeem

### Security verbetering
- **Voor:** SHA-256 zonder salt (kwetsbaar)
- **Na:** scrypt met automatische salt per wachtwoord (veilig)

### Resultaat
- Elk wachtwoord krijgt unieke hash, zelfs bij identieke wachtwoorden
- Rainbow table aanvallen zijn onmogelijk
- Brute-force aanvallen zijn extreem langzaam
- Database leak is minder gevaarlijk
- Voldoet aan moderne security standards (OWASP, ENISA)

---

## 10. Bronnen

- OWASP Password Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- Werkzeug Security Documentation: https://werkzeug.palletsprojects.com/en/3.0.x/utils/#module-werkzeug.security
- scrypt RFC 7914: https://tools.ietf.org/html/rfc7914
- ENISA Cryptographic Guidelines

---

**Einde document**
