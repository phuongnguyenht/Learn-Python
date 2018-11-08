#! /usr/bin/python
import ftplib
from ftplib import FTP
import os.path
import sys,os

SERVER = '10.3.3.234'
USER = 'ftp'
PASS = 'ftp'
PORT = 21
filename = "send.txt"
filepath = "C:\\Users\\My-Computer\\Desktop\\" + filename
ftp = FTP()
ftp.connect(SERVER, PORT)
print (ftp.getwelcome())
def main():
    try:
        print ("Logging in...")
        ftp.login(USER, PASS)
        print("Login successful")

        if os.path.isfile(filepath):
            ftp.storlines("STOR " + filename, open(filepath, 'r'))
            # transfer the file
            print('Uploading ' + filename + '...')
            print "Upload " + filename + " finished."
            ftp.quit()
        else:
            print filename + ' does not exist'
    except:
        print ("Failed to login")
main()
# delete file after put file to server
# os.remove(filepath)