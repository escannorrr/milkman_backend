from passlib.context import CryptContext

class Encrypt:

    def encrypt(password:str):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)