### Insert table blacklist

from ftplib import FTP
import pyodbc
import os

#setup db
mtconn = pyodbc.connect(driver='{SQL Server}', server='xxx', database='xxxx', uid='xx', pwd='xxxx')
mtcursor = mtconn.cursor()

#filename ='blacklistfolder1.txt'
#os.chdir('C:\\Documents and Settings\\Administrator\\Desktop\\')

#file = open('C:\\Documents and Settings\\Administrator\\Desktop\\blacklistfolder1.txt', 'r')
file = open('C:\\web\\Crons\\GetFTPfile\\blacklistfolder1.txt', 'r')

file_content = file.readlines()
for row in file_content:
	append = "+84"
	rows = append + row
	print rows
	insert = "INSERT INTO vivas_mt.dbo.blacklist (msisdn) VALUES('{0}')".format(rows)
	print insert
	mtcursor.execute(insert)
mtconn.commit()
