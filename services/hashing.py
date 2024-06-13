from passlib.context import CryptContext


class HashingService:
    def __init__(self, context: CryptContext) -> None:
        self.context = context
    
    def hash_string(self, value: str) -> str:
        return self.context.hash(value)
    
    def verify_string(self, value: str, hashed_value: str) -> bool:
        return self.context.verify(value, hashed_value)
