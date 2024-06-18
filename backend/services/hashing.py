from passlib.context import CryptContext

hashing_service = CryptContext(schemes=['bcrypt'], deprecated='auto')
