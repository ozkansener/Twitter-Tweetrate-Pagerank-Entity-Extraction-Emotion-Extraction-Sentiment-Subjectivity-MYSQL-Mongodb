# -*- coding: utf-8 -*-
"""
Ozkan Sener ozkansener@gmail.com
"""
from pandas.io import sql
import MySQLdb
import pandas as pd
import pymysql
from sqlalchemy import create_engine

db=MySQLdb.connect(host="localhost",user="root",passwd="Quality123*",db="wbqual")

df = pd.read_sql_query('SELECT * FROM features', db)
print df