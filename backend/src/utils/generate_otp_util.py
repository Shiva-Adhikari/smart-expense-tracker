import secrets

LIMIT = 6

def generate_otp():
    return secrets.randbelow(900000) + 100000
