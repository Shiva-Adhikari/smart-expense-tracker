from passlib.context import CryptContext


myctx = CryptContext(schemes=["sha256_crypt", "des_crypt"], deprecated='auto')


def hash_password(plain_password: str) -> str:
    return myctx.hash(plain_password)
    

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return myctx.verify(plain_password, hashed_password)
