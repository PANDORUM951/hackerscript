from distutils.core import setup
import py2exe
import os
import time
import random
import sqlite3
from pathlib import Path
import re
import glob
from shutil import copyfile

setup(zipfile=None,
      options={"py2exe": {"bundle_files": 1}},
      windows=["hackerscript.py"])
