import os
import random
import shutil
import string
from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File

from common.oauth2 import get_current_user
from common.utils import create_dir
from container import Container
from schemas.post import PostBase, PostDisplay
from schemas.user import UserBase
from services.post import PostService

router = APIRouter(
    prefix="/post",
    tags=["post"]
)


@router.post('/', response_model=PostDisplay)
@inject
def create_post(request: PostBase, post_service: PostService = Depends(Provide[Container.post_service])):
    response = post_service.create_post(request)
    if response.success:
        return response.data
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{response.message}")


# noinspection PyShadowingBuiltins
@router.get("/all", response_model=List[PostDisplay])
@inject
def get_posts(post_service: PostService = Depends(Provide[Container.post_service])):
    return post_service.get_posts()


# noinspection PyShadowingBuiltins
@router.get("/{id}", response_model=PostDisplay)
@inject
def get_post(id: int, post_service: PostService = Depends(Provide[Container.post_service])):
    response = post_service.get_post(id)
    if response.success:
        return response.data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{response.message}")


# noinspection PyShadowingBuiltins
@router.post("/update/{id}", response_model=PostDisplay)
@inject
def update_post(id: int, request: PostBase, post_service: PostService = Depends(Provide[Container.post_service])):
    response = post_service.update_post(id, request)
    if response.success:
        return response.data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{response.message}")


# noinspection PyShadowingBuiltins
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_post(id: int,
                post_service: PostService = Depends(Provide[Container.post_service]),
                current_user: UserBase = Depends(get_current_user)):
    response = post_service.delete_post(id)
    if response.success:
        return response.data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{response.message}")


@router.post("/image")
def upload_image(image: UploadFile = File(...)):
    letter = string.ascii_letters
    rand_string = ''.join(random.choice(letter) for _ in range(6))
    new = f"_{rand_string}."
    filename = new.join(image.filename.rsplit('.', 1))
    root_path = os.path.join(os.getcwd(), "images")

    path = os.path.join(root_path, filename)

    create_dir(root_path)
    try:
        with open(path, 'w+b') as wf:
            shutil.copyfileobj(image.file, wf)
        return {'filename': path}
    except OSError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Error: {e}')
