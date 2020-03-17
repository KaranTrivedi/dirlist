#!/projects/dirlist/venv/bin/python

'''
Api for getting files and folders
'''

#DEFAULTS
import configparser
import logging
#Added
import os
from os import path
import json

from typing import List
from fastapi import FastAPI, Query

APP = FastAPI()

#Define config and logger.
CONFIG = configparser.ConfigParser()
CONFIG.read('/projects/dirlist/conf/config.ini')
SECTION = 'test'
PATH = CONFIG[SECTION]["path"]

def show_sections(logger):
    '''
    Output all options for given section
    '''

    conf_str = "\n\n"
    for sect in CONFIG.sections():
        conf_str += "[" + sect + "]\n"
        for var in list(CONFIG[sect]):
            conf_str += var + "\t\t=\t" + CONFIG[sect][var] + "\n"
    logger.info(conf_str)

def get_items(q: List[str] = Query(None)):
    '''
    Pass path to function.
    Returns folders and files.
    '''

    results = {}

    query_items = {"q": q}
    entry = PATH + "/".join(query_items["q"])

    if os.path.isfile(entry):
        # return entry
        with open(entry, 'r') as f:
            data = f.read()
        return {"video/mkv": data}

    dirs = os.listdir(entry + "/")
    results["folders"] = [val for val in dirs if os.path.isdir(entry + "/"+val)]
    results["files"] = [val for val in dirs if os.path.isfile(entry + "/"+val)]
    results["path_vars"] = query_items["q"]

    return results

def main():
    '''
    Main function.
    '''
    logging.basicConfig(filename=CONFIG[SECTION]['log'],\
                        level=CONFIG[SECTION]['level'],\
                        format='%(asctime)s::%(name)s::%(funcName)s::%(levelname)s::%(message)s',\
                        datefmt='%Y-%m-%d %H:%M:%S')

    logger = logging.getLogger(SECTION)
    logger.info("####################STARTING####################")

    if CONFIG[SECTION]['level'] == "DEBUG":
        show_sections(logger=logger)

    print(get_items(["downloads","New.Girl.S05E05.1080p.WEB-DL.DD5.1.H.264-NTb.mkv"]))

if __name__ == "__main__":
    main()
