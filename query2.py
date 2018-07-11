from pandas.io import sql
import MySQLdb
import pandas as pd
df= pd.read_csv('merged.csv')

db=MySQLdb.connect(host="localhost",user="root",passwd="Quality123*",db="wbqual")
df.to_sql(con=db, name='features', if_exists='append', flavor='mysql')
#df.to_sql(con=db, name='features', if_exists='replace', flavor='mysql')
