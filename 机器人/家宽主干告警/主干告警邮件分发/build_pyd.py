import os
from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='any words.....',
    ext_modules=cythonize([
        os.getcwd() + "\\main_yinru.py",
        "D:\王东\支撑程序\public.py",
        "D:\王东\支撑程序\public_api.py",
        "D:\王东\支撑程序\public_time.py",
    ], language_level='3')
)
