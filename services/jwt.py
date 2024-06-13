from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose.jwt import encode, decode

from utils.settings import JwtSettings

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/login/token")


class JWTService:
    def __init__(self, jwt_settings: JwtSettings) -> None:
        self.settings = jwt_settings

    def create_access_token(self, email: str, user_id: int) -> str:
        return encode({
            'sub': email,
            'id': user_id,
            'exp': datetime.now(UTC) + timedelta(
                minutes=self.settings.expire_minutes
            )}, 
            self.settings.secret_key, 
            self.settings.algorithm
        )

    def get_user_by_token(self, token: Annotated[str, Depends(oauth2_bearer)]):
        try:
            pl = decode(
                token, self.settings.secret_key, self.settings.algorithm
            )
            return {'email': pl['sub'], 'id': pl['id']}
        except (JWTError, KeyError):
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, detail="Couldn't validate user."
            )