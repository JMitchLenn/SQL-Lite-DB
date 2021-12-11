# import necessary libraries
import pandas as pd
import os
import glob
import numpy as np

# use glob to get all the csv files
# in the folder
path = os.getcwd()
subdir = "\\rawdata"
path2 = path + subdir
type(path)
type(path2)

csv_files = glob.glob(os.path.join(path2,"*.xlsx"))
csv_files

### Search all Subdirectories
import os
from glob import glob
PATH = path2
EXT = "*.xlsx"
all_csv_files = [file
                 for path, subdir, files in os.walk(PATH)
                 for file in glob(os.path.join(path, EXT))]
print(all_csv_files)

li = []
# loop over the list of csv files
for f in all_csv_files:
    # read the csv file
    df = pd.read_excel(f)
    # print the location and filename
    print('Location:', f, "RecordCT: ", len(f))
    print('File Name:', f.split("\\")[-1])
    df['source'] = f
    df['from_yr'] = df['source'].str[54:63]
#    df['asofDate'] =
    li.append(df)

#, ignore_index=True
frame = pd.concat(li, axis=0)
frame['RowNum'] = np.arange(frame.shape[0])
print('N = ', len(frame))

frame.count()

# size of each group
print(frame.groupby('source').size())

frame.describe()
ch=frame.notnull()

## Count NAs in each column
frame.isna().sum()

#Compute a mask with isna, then group and find the sum:
#https://stackoverflow.com/questions/53947196/groupby-class-and-count-missing-values-in-features
countbygroup = frame.drop('source', 1).isna().groupby(frame.source, sort=False).sum()

# return the transpose
result = countbygroup.transpose()

frame.dtypes
#convert every column to strings
frame = frame.astype(dtype={'Event Name': 'string',
                            'First Name': 'string',
                            'Last Name': 'string',
                            'Email': 'string',
                            'Home Address 1': 'string',
                            'Home Address 2': 'string',
                            'Home City': 'string',
                            'Home State': 'string',
                            'Home Country': 'string',
                            'Home Zip': 'string',
                            'Age': 'string',
                            'Random Hacks of Kindness Junior Alum': 'string',
                            'Name of School ' : 'string',
                            'source': 'string',
                            'from_yr': 'string',
                            'Gender': 'string',
                            'How did you hear about the event?': 'string',
                            'Grade': 'string',
                            'School, Company or Organization': 'string',
                            })
frame.dtypes

df = frame
### clean up#df['new column name'] = df['column name'].apply(lambda x: 'value if condition is met' if x condition else 'value if condition is not met')
#https://medium.com/swlh/python-equivalent-of-common-sas-statements-and-functions-530869084da
# Creating new column that contains 0 for missing in Col_A and 1 otherwise
#df['clean_school']=df['School, Company or Organization'].apply(lambda x: df["School, Company or Organization"] if pd.notnull(x) else 's_notblank')
#Col 1 = where you want the values replaced
#Col 2 = where you want to take the values from
#df["School, Company or Organization"].fillna(df["Name of School "], inplace=True)

#def age_grp_if(x):
#    if (pd.isnull(x)) :
#        return age_group['School, Company or Organization']
#    else:
#        return 'ItaintNull'

#age_group = df.copy()
#age_group['age_grp_if'] = age_group['Name of School '].apply(age_grp_if)
#age_group.head()

#https://stackoverflow.com/questions/10715519/conditionally-fill-column-values-based-on-another-columns-value-in-pandas
### THis is the easiest way I found using numpy,  Pandas easier if it was a mapping or a recods
df['Clean School'] = np.where(df['School, Company or Organization'].notnull() == True, df['School, Company or Organization'], df['Name of School '])

type(frame)
#https://stackoverflow.com/questions/53947196/groupby-class-and-count-missing-values-in-features
countbygroup = frame.drop('source', 1).isna().groupby(frame.source, sort=False).sum()

#df.to_excel(path +'\HATtest.xlsx', sheet_name='draft', index = False)


#x = len(frame['source'])
#y = frame['source'].str[54:63]
#y

### Pick up here getting the year for the grade

#https://towardsdatascience.com/turn-your-excel-workbook-into-a-sqlite-database-bc6d4fd206aa
##### Original DB Build
import pandas as pd
import sqlite3

EventB = pd.read_excel(
    'C:/Users/Joe/Documents/HackathonDB/EventSource.xlsx',
    sheet_name='eventb', header=0)
EventB.head(10)
#add a date field
EventB['GradeDate'] = '2019-07-01'

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

df.head(10)
## rename all the columns
# Before renaming the columns
print(df.columns)
df.rename(columns={ 'Event Name': 'Event_name',
                    'First Name': 'First_Name',
                    'Last Name': 'Last_Name',

                    'Home Address 1': 'HomeAdd1',
                    'Home Address 2': 'HomeAdd2',
                    'Home City': 'City',
                    'Home State': 'State',
                    'Home Zip': 'Zipcode',
                    'Home Country': 'Country',
                   # 'TEST': 'Age',
                    'Random Hacks of Kindness Junior Alum': 'Alum',
                    'from_yr': 'GradeDate',
                    'How did you hear about the event?': 'HowHear',
                    'Clean School':'School'
                }, inplace=True)
# After renaming the columns
print(df.columns)

df['Grade_Date']
### Create a mapping for age of records to use in the app
# ============== ALTERNATIVE METHODS ==============
## Method A using map
#EventB['GradeDate'] = '2019-07-01'
mapping = {'2014-2015':'2015-01-01',
           '2015-2016':'2016-01-01',
           '2016-2017':'2017-01-01',
           '2017-2018':'2018-01-01',
           '2018-2019':'2019-01-01',
           '2019-2020':'2020-01-01',
           '': 'NuleJUML'}
df['Est_Rec_Dt'] = df['GradeDate'].map(mapping)
type(mapping)
#c.execute("DROP TABLE master2")

c.execute("""
    CREATE TABLE master (
        PersID INTEGER,
        Event_name TEXT,
        First_Name TEXT,
        Last_Name TEXT,
        Email TEXT,
        HomeAdd1 TEXT,
        HomeAdd2 TEXT,
        City TEXT,
        State TEXT,
        Zipcode TEXT,
        Country TEXT,
        Age INTEGER,
        Alum TEXT,
        GradeDate TEXT,
        Gender TEXT,
        HowHear TEXT,
        Grade INTEGER,
        School TEXT,
        Est_Rec_Dt TEXT,
        LASTROLE TEXT,
        PRIMARY KEY(PersID),
        FOREIGN KEY(LASTROLE) REFERENCES ROLES(ROLE)
        );
    """)

#EventB.to_sql('master', db_conn, if_exists='append', index=False)

# Load the big data
print(df.columns)
del df['Name of School ']
del df['source']
del df['School, Company or Organization']
del df['RowNum']

df.to_sql('master', db_conn, if_exists='append', index=False)


db_conn.close()


### Check it
db_conn = sqlite3.connect('C:/Users/Joe/Documents/HackathonDB/participants.db')
c = db_conn.cursor()

pd.read_sql("SELECT * FROM master LIMIT 5", db_conn)
pd.read_sql("SELECT * FROM master2 LIMIT 5", db_conn)


db_conn.close()
