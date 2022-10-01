from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from common.hash import Hash
from common.oauth2 import create_access_token
from container import Container
from services.user import UserService

router = APIRouter(
    tags=["authentication"]
)


@router.post('/token')
@inject
def get_token(request: OAuth2PasswordRequestForm = Depends(),
              user_service: UserService = Depends(Provide[Container.user_service])):
    response = user_service.get_user_by_name(request.username)
    if not response.success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    user = response.data
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    access_token = create_access_token(data={'sub': user.username})
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username
    }



