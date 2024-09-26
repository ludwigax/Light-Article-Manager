from sqlalchemy.orm import relationship, sessionmaker, declarative_base

import os
import csv
from typing import List

import database
# from utils import opn

import numpy as np

database.import_articles("repository.db")

os.environ["LAM_WORK_DIR"] = os.path.dirname(os.path.abspath(__file__))

