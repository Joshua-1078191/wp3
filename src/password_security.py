"""
Password Security Module
========================

This module provides secure password hashing functionality for the application.
It implements ENISA recommendations for password storage with proper salting.

Author: Joshua
Date: October 2025
Purpose: School Assignment - Web Programming Project 3

Security Implementation:
-----------------------
Hash Algorithm: scrypt
Parameters: N=32768, r=8, p=1

Justification:
-------------
After researching ENISA recommendations and modern cryptographic standards,
scrypt was chosen for the following reasons:

1. Memory-hardness: scrypt requires significant memory to compute hashes,
   making it resistant to hardware-based brute-force attacks (GPUs, ASICs)

2. Configurable cost factor: The N parameter can be adjusted to increase
   difficulty as computing power improves

3. Built-in salting: Werkzeug's implementation automatically generates
   a cryptographically secure random salt for each password

4. Industry adoption: Used by major platforms and recommended by security experts

Alternative Methods Considered:
------------------------------
- PBKDF2-SHA256: Older standard, less resistant to GPU attacks
- PBKDF2-SHA512: Better than SHA256, but still less memory-hard than scrypt
- bcrypt: Good alternative, but scrypt provides better memory-hardness
- Argon2: Winner of Password Hashing Competition 2015, best choice for new projects
  (not used here due to additional dependency requirements)

ENISA Recommendations Met:
-------------------------
✓ Use of cryptographic hash function
✓ Unique salt per password (automatic)
✓ Sufficient computational cost (N=32768)
✓ Protection against rainbow table attacks
✓ Protection against brute-force attacks
"""

from werkzeug.security import generate_password_hash, check_password_hash

# scrypt configuration
# N=32768: CPU/Memory cost parameter (2^15)
# r=8: Block size parameter
# p=1: Parallelization parameter
PASSWORD_HASH_METHOD = 'scrypt:32768:8:1'

# For very high security environments, increase N to 65536 or higher
# PASSWORD_HASH_METHOD = 'scrypt:65536:8:1'

# For legacy systems or lower security requirements, PBKDF2 can be used:
# PASSWORD_HASH_METHOD = 'pbkdf2:sha256:600000'  # 600k iterations (OWASP 2023)


def hash_password(password: str) -> str:
    """
    Hash a password using scrypt with automatic salt generation.
    
    The salt is automatically generated using a cryptographically secure
    random number generator and is stored within the hash string itself.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password string containing method, salt, and hash
        Format: method$salt$hash
        
    Example:
        >>> hashed = hash_password('mySecurePassword123')
        >>> print(hashed)
        scrypt:32768:8:1$...$...
    """
    return generate_password_hash(password, method=PASSWORD_HASH_METHOD)


def verify_password(password_hash: str, password: str) -> bool:
    """
    Verify a password against its hash.
    
    This function extracts the salt from the stored hash and uses it
    to hash the provided password for comparison.
    
    Args:
        password_hash: Stored password hash (includes method and salt)
        password: Plain text password to verify
        
    Returns:
        True if password matches, False otherwise
        
    Example:
        >>> hashed = hash_password('myPassword')
        >>> verify_password(hashed, 'myPassword')
        True
        >>> verify_password(hashed, 'wrongPassword')
        False
    """
    return check_password_hash(password_hash, password)


def is_password_strong(password: str) -> tuple[bool, str]:
    """
    Check if a password meets minimum security requirements.
    
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    
    Args:
        password: Password to check
        
    Returns:
        Tuple of (is_valid, error_message)
    """
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
    test_password = "SecurePassword123!"
    
    print("=== Password Security Module Test ===\n")
    
    # Hash a password
    hashed = hash_password(test_password)
    print(f"Original password: {test_password}")
    print(f"Hashed password: {hashed}\n")
    
    # Verify correct password
    print(f"Verify correct password: {verify_password(hashed, test_password)}")
    
    # Verify incorrect password
    print(f"Verify incorrect password: {verify_password(hashed, 'WrongPassword')}\n")
    
    # Test same password generates different hashes (due to random salt)
    hashed1 = hash_password(test_password)
    hashed2 = hash_password(test_password)
    print("=== Salt Demonstration ===")
    print(f"Hash 1: {hashed1}")
    print(f"Hash 2: {hashed2}")
    print(f"Hashes are different: {hashed1 != hashed2}")
    print(f"Both verify correctly: {verify_password(hashed1, test_password) and verify_password(hashed2, test_password)}\n")
    
    # Test password strength
    print("=== Password Strength Tests ===")
    test_passwords = [
        "weak",
        "WeakPass",
        "WeakPass1",
        "WeakPass1!",
    ]
    
    for pwd in test_passwords:
        is_strong, message = is_password_strong(pwd)
        print(f"{pwd:20s} - {'✓' if is_strong else '✗'} {message}")

