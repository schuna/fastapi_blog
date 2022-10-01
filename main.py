from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from container import Container
import endpoints.post as post_endpoints
import endpoints.user as user_endpoints
import endpoints.authentication as auth_endpoints


def create_app() -> FastAPI:
    container = Container()
    db = container.db()
    db.create_database()

    fast_app = FastAPI()
    fast_app.container = container
    fast_app.include_router(auth_endpoints.router)
    fast_app.include_router(user_endpoints.router)
    fast_app.include_router(post_endpoints.router)

    origins = [
        'http://localhost:3000',
        'http://localhost:3001'
    ]

    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=['*']
    )
    fast_app.mount('/images',
                   StaticFiles(directory="images"),
                   name="images")
    return fast_app


app = create_app()
