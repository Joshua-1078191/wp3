
import hashlib


def hash_password(password: str) -> str:

    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def verify_password(password_hash: str, password: str) -> bool:

    return password_hash == hash_password(password)


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


# Example usage and testing
if __name__ == '__main__':
    # Test password hashing
    test_password = "password123"

    # Hash a password
    hashed = hash_password(test_password)
    print(f"Original password: {test_password}")
    print(f"Hashed password: {hashed}\n")
    
    # Verify correct password
    print(f"Verify correct password: {verify_password(hashed, test_password)}")
    
    # Verify incorrect password
    print(f"Verify incorrect password: {verify_password(hashed, 'WrongPassword')}\n")
    
    hashed1 = hash_password(test_password)
    hashed2 = hash_password(test_password)

    # Show that different passwords have different hashes
    print("=== Different passwords (still insecure without salt) ===")
    print(f"'password123' -> {hash_password('password123')}")
    print(f"'password456' -> {hash_password('password456')}")
    print(f"'password123' -> {hash_password('password123')} (same as first!)\n")

