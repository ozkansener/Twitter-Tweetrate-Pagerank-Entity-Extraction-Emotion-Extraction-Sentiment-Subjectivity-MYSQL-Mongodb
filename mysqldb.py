#import MySQLdb
#
def dbconnect():
    try:
        db = MySQLdb.connect(
            host='localhost',
            user='root',
            passwd='Quality123*',
            db='wbqual'
        )
    except Exception as e:
        sys.exit("Can't connect to database")
    return db

#def insertDb():
#    try:
#        db = dbconnect()
#        cursor = db.cursor()
#        cursor.execute("""
#        INSERT INTO nameoftable(nameofcolumn) \
#        VALUES (%s) """, (data))
#        cursor.close()
#    except Exception as e:
#        print e
#mongo

#import csv
#import MySQLdb
#
#mydb = MySQLdb.connect(host='localhost',
#    user='co302mc',
#    passwd='mafol597',
#    db='co302mc_bike_theft')
#cursor = mydb.cursor()
#
#csv_data = csv.reader(file('cycling.csv'))
#for row in csv_data:
#
#	cursor.execute("INSERT INTO cycling(Borough, Work_2001, Bike_2001, Percentage_2001, Work_2011, Bike_2011, Percentage_2011, Percentage_change) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", row)
#
##close the connection to the database.
#mydb.commit()
#cursor.close()
#print "Done"