
from werkzeug.security import generate_password_hash, check_password_hash


PASSWORD_HASH_METHOD = 'scrypt:32768:8:1'


def hash_password(password: str) -> str:

    return generate_password_hash(password, method=PASSWORD_HASH_METHOD)


def verify_password(password_hash: str, password: str) -> bool:

    return check_password_hash(password_hash, password)


def is_password_strong(password: str) -> tuple[bool, str]:

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is strong"


if __name__ == '__main__':
    test_password = "password123"
    
    # Hash same password twice
    hash1 = hash_password(test_password)
    hash2 = hash_password(test_password)
    

    print(f"Password: {test_password}")
    print(f"Hash 1: {hash1}")
    print(f"Hash 2: {hash2}")
    print(f"Hashes different (salt working): {hash1 != hash2}")
    print(f"Both verify correctly: {verify_password(hash1, test_password) and verify_password(hash2, test_password)}")

