import requests
import jwt
import json
import os.path
from os import path
import time
from tqdm import tqdm
import datetime
import collections
from collections import defaultdict
import sys
import glob
import re
from pprint import pprint
import pandas as pd
import numpy as np
from functools import reduce
import itertools
import sqlite3
import json
import xlrd
import xlwt
import string
# Set default encoding to utf-8
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import warnings
import openpyxl
from openpyxl import Workbook

# Create a new workbook
workbook = Workbook()

# Suppress the warning about default style
warnings.filterwarnings("ignore", message="Workbook contains no default style*")

# Use the workbook to write data to Excel and save the workbook
# ...

