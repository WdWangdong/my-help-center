# -- coding: utf-8 --
# -必备模块
import main_yinru
import json
import os
import shutil
import sys
import time

import pythoncom
import win32com.client
from PIL import ImageGrab
from openpyxl import load_workbook
import pandas as pd
import redis
from redis.lock import Lock
from loguru import logger as log
import requests
import public
import public_api
import public_time
import urllib3


# --------------

def main():
    main_yinru.main()


if __name__ == '__main__':
    try:
        main()
    except:
        public.try_error('主入口')
