#!/projects/dirlist/venv/bin/python

'''
Api for getting files and folders
'''

#DEFAULTS
import configparser
#Added
import os
from os import path
from pydantic import BaseModel
from typing import List
from fastapi import FastAPI, Query, File, UploadFile, HTTPException, Response
from fastapi.logger import logger as fastapi_logger
import uvicorn
from logging.handlers import RotatingFileHandler
import logging

class Data(BaseModel):
    data: bytes

app = FastAPI()

#Define config and logger.
CONFIG = configparser.ConfigParser()
CONFIG.read('/projects/dirlist/conf/config.ini')
SECTION = 'dirlist'
PATH = CONFIG[SECTION]["path"]

logging.basicConfig(filename=CONFIG[SECTION]['log'],\
                        level=CONFIG[SECTION]['level'],\
                        format='%(asctime)s::%(name)s::%(funcName)s::%(levelname)s::%(message)s',\
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

@app.get("/items/{item_id}")
def read_item(item_id: int, query: str = None):
    '''
    Sample function.
    '''
    return {"item_id": item_id, "q": query}

@app.get("/items/")
async def read_items(q: List[str] = Query(None)):
    '''
    List function
    '''
    query_items = {"q": q}

    return "/".join(query_items["q"])

@app.get("/shows/")
def get_items(q: List[str] = Query(None)):
    '''
    Pass path to function.
    Returns folders and files.
    '''

    results = {}

    query_items = {"q": q}
    entry = PATH + "/".join(query_items["q"])

    if os.path.isfile(entry):
        with open(entry, 'rb') as f:
            data = f.read()
        return data

    logger.info(entry)

    dirs = os.listdir(entry + "/")
    results["folders"] = [val for val in dirs if os.path.isdir(entry + "/"+val)]
    results["files"] = [val for val in dirs if os.path.isfile(entry + "/"+val)]
    results["path_vars"] = query_items["q"]

    return results

@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

# def show_sections(logger):
#     '''
#     Output all options for given section
#     '''
#     conf_str = "\n\n"
#     for sect in CONFIG.sections():
#         conf_str += "[" + sect + "]\n"
#         for var in list(CONFIG[sect]):
#             conf_str += var + "\t\t=\t" + CONFIG[sect][var] + "\n"
#     logger.info(conf_str)

def main():
    '''
    Main function.
    '''
    # logging.basicConfig(filename=CONFIG[SECTION]['log'],\
    #                     level=CONFIG[SECTION]['level'],\
    #                     format='%(asctime)s::%(name)s::%(funcName)s::%(levelname)s::%(message)s',\
    #                     datefmt='%Y-%m-%d %H:%M:%S')

    # logger = logging.getLogger(SECTION)
    # logger.info("####################STARTING####################")

    uvicorn.run("dirlist:app", host="0.0.0.0", port=8000, reload=True, access_log=False)

    # if CONFIG[SECTION]['level'] == "DEBUG":
    #     show_sections(logger=logger)

if __name__ == '__main__':
    main()