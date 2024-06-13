from fastapi import APIRouter, HTTPException, status

from api.schemas import SignIn, SignUp, Token
from services import hashing_service, jwt_service, user_service_dependency

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/sign_in', response_model=Token)
async def sign_in(user_schema: SignIn, user_service: user_service_dependency):
    user = await user_service.authenticate(
        user_schema.email, hashing_service.hash_string(user_schema.password)
    )
    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Invalid email or password"
        )
    
    return {
        'access_token': jwt_service.create_access_token(user.email, user.id), 
        'token_type': 'bearer'
    }

@router.post('/sign_up')
async def sign_up(user_schema: SignUp, user_service: user_service_dependency):
    user = await user_service.get_user_by_email(user_schema.email)
    if user is not None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "User with this email already exists"
        )
    
    new_user = await user_service.create_user(
        user_schema.email, 
        hashing_service.hash_string(user_schema.password),
        user_schema.widgets
    )
    return {'access_token': jwt_service.create_access_token(new_user,)}
