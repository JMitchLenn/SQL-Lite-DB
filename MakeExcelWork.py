import pandas as pd
import sqlite3
filePath = 'C:\\Users\\Joe\\Documents\\HackathonDB\\testJML0923.xlsx'
conn = sqlite3.connect('C:\\Users\\Joe\\Documents\\HackathonDB\\participants.db')
writer = pd.ExcelWriter(filePath,engine='xlsxwriter')
df = pd.read_sql("SELECT * FROM master", conn)
df.head()
df.to_excel(writer, sheet_name='outit', index=False)
print("Excel Saved")
writer.save()
