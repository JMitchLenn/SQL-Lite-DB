#https://towardsdatascience.com/turn-your-excel-workbook-into-a-sqlite-database-bc6d4fd206aa

import pandas as pd
import sqlite3

EventB = pd.read_excel(
    'C:/Users/Joe/Documents/HackathonDB/EventSource.xlsx',
    sheet_name='eventb', header=0)
EventB.head(10)
#add a date field
EventB['GradeDate'] = '2019-01-01'

EventB.head(10)

db_conn = sqlite3.connect('C:/Users/Joe/Documents/HackathonDB/participants.db')
c = db_conn.cursor()

#CREATE TABLE s
# ales (
#    SalesID INTEGER ,
#    OrderID TEXT NOT NULL,
#    ProductID TEXT NOT NULL,
#    Sales REAL,
#    Quantity INTEGER,
#    Discount REAL,
#    Profit REAL,
#    PRIMARY KEY(SalesID),
#    FOREIGN KEY(OrderID) REFERENCES orders(OrderID),
#    FOREIGN KEY(ProductID) REFERENCES products(ProductID)   );

# drop table
c.execute("DROP TABLE master")

print("data dropped successfully")

c.execute("""
    CREATE TABLE master (
        PersID INTEGER,
        Email TEXT,
        First_Name TEXT,
        Last_Name TEXT,
        Grade INTEGER,
        Gender TEXT,
        School TEXT,
        Street TEXT,
        City TEXT,
        State TEXT,
        GradeDate TEXT,
        LASTROLE TEXT,
        PRIMARY KEY(PersID),
        FOREIGN KEY(LASTROLE) REFERENCES ROLES(ROLE)
        );
    """)

EventB.to_sql('master', db_conn, if_exists='append', index=False)

db_conn.close()


### Check it
db_conn = sqlite3.connect('C:/Users/Joe/Documents/HackathonDB/participants.db')
c = db_conn.cursor()

pd.read_sql("SELECT * FROM master LIMIT 5", db_conn)

db_conn.close()

# Forecast Date
#select email,Grade,GradeDate, date('now') as Now, (JULIANDAY('Now') - JULIANDAY(GradeDate))/365 as DeltaYears  from master;