import configparser
import logging
import os
from fastapi import FastAPI

from app.routers.views import root_router
from app.routers.shows.views import shows_router

#Define config and logger.
CONFIG = configparser.ConfigParser()
CONFIG.read('/projects/dirlist/conf/config.ini')
SECTION = 'dirlist'
PATH = CONFIG[SECTION]["path"]

logging.basicConfig(filename=CONFIG[SECTION]['log'],
                    level=CONFIG[SECTION]['level'],
                    format='%(asctime)s::%(name)s::%(funcName)s::%(levelname)s::%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(SECTION)

def add_routes(app: FastAPI):
    logger.info("Mounting routes")
    app.include_router(root_router)
    app.include_router(shows_router, prefix="/shows")

def create_root_app() -> FastAPI:
    app = FastAPI(
        title="First api",
        description="How does this look",
        version="0.1"
    )
    add_routes(app)

    return app