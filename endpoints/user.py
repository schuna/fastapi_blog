from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status

from common.hash import Hash
from common.oauth2 import get_current_user
from container import Container
from schemas.user import UserBase, UserDisplay
from services.user import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post('/', response_model=UserDisplay)
@inject
def create_user(request: UserBase, user_service: UserService = Depends(Provide[Container.user_service])):
    request.password = Hash.bcrypt(request.password)
    response = user_service.create_user(request)
    if response.success:
        return response.data
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{response.message}")


# noinspection PyShadowingBuiltins
@router.get("/{id}", response_model=UserDisplay)
@inject
def get_user(id: int, user_service: UserService = Depends(Provide[Container.user_service])):
    response = user_service.get_user(id)
    if response.success:
        return response.data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{response.message}")


# noinspection PyShadowingBuiltins
@router.post("/update/{id}", response_model=UserDisplay)
@inject
def update_user(id: int, request: UserBase, user_service: UserService = Depends(Provide[Container.user_service])):
    request.password = Hash.bcrypt(request.password)
    response = user_service.update_user(id, request)
    if response.success:
        return response.data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{response.message}")


# noinspection PyShadowingBuiltins
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_user(id: int,
                user_service: UserService = Depends(Provide[Container.user_service]),
                current_user: UserBase = Depends(get_current_user)):
    response = user_service.delete_user(id)
    if response.success:
        return response.data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{response.message}")
