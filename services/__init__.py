from passlib.context import CryptContext

from .hashing import HashingService
from .jwt import JWTService
from .user import user_service_dependency
from utils.settings import settings

hashing_service = HashingService(CryptContext(schemes=['bcrypt'], deprecated='auto'))
jwt_service = JWTService(settings.jwt)

