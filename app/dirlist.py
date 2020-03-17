#!/projects/dirlist/venv/bin/python

'''
Api for getting files and folders
'''

# DEFAULTS
import configparser
# Added
import os
from os import path
from logging.handlers import RotatingFileHandler
import logging

from typing import List
from fastapi import FastAPI, Query, File, HTTPException, Form, UploadFile
from fastapi.logger import logger as fastapi_logger
# from fastapi.staticfiles import StaticFiles

from starlette.responses import FileResponse

import uvicorn

app = FastAPI()

# Define config and logger.
CONFIG = configparser.ConfigParser()
CONFIG.read('/projects/dirlist/conf/config.ini')
SECTION = 'dirlist'
PATH = CONFIG[SECTION]["path"]

logging.basicConfig(filename=CONFIG[SECTION]['log'],
                    level=CONFIG[SECTION]['level'],
                    format='%(asctime)s::%(name)s::%(funcName)s::%(levelname)s::%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(SECTION)

# formatter = logging.Formatter(
#         "[%(asctime)s.%(msecs)03d] %(levelname)s [%(thread)d] - %(message)s", "%Y-%m-%d %H:%M:%S")
# handler = RotatingFileHandler(CONFIG[SECTION]["log"], backupCount=0)
# logging.getLogger().setLevel(logging.NOTSET)
# fastapi_logger.addHandler(handler)
# handler.setFormatter(formatter)
# fastapi_logger.info('****************** Starting Server *****************')

@app.get("/")
def read_root():
    '''
    Root function.
    '''
    return {"Hello": "World"}

# app.mount("/files", StaticFiles(directory="/shows"), name="shows")

@app.get("/shows/")
async def get_items(q: List[str] = Query(None)):
    '''
    Pass path to function.
    Returns folders and files.
    '''

    results = {}

    query_items = {"q": q}
    if query_items["q"]:
        entry = PATH + "/".join(query_items["q"])
    else:
        entry = PATH

    if os.path.isfile(entry):
        logger.info(entry)
        return FileResponse(entry)

    dirs = os.listdir(entry + "/")
    results["folders"] = [
        val for val in dirs if os.path.isdir(entry + "/"+val)]
    results["files"] = [val for val in dirs if os.path.isfile(entry + "/"+val)]
    results["path_vars"] = query_items["q"]

    return results

def main():
    '''
    Main function.
    '''
    uvicorn.run("dirlist:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == '__main__':
    main()
