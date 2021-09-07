from . import app
from .routers import main as main_route, upload_to_gdrive, auth, frontend

from fastapi.middleware.cors import CORSMiddleware


def main():
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router=main_route.router)
    app.include_router(router=upload_to_gdrive.router)
    app.include_router(router=frontend.router)
    app.include_router(router=auth.router)
