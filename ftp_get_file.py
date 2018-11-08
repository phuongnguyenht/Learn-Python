### Download file CDR from CPS folder of server VMS

import logging
import datetime
import time
import socket
from datetime import date, timedelta
from ftplib import FTP
import ftplib
import os.path

logging.basicConfig(filename="FTP_cdr_" + str(datetime.date.today()) + ".log", level=logging.INFO)

def main():
    try:
        CDRServerHost = '100.154.140.212'
        CDRUsername = 'user'
        CDRPassword = 'password'
        
        yesterday =  date.today() - timedelta(1)
        yt = yesterday.strftime("%Y%m%d")
        directory = '\\cps\\yesterday.strftime("%Y%m%d")\\'
        Ftp = FTP(CDRServerHost)
        loginResult = Ftp.login(CDRUsername, CDRPassword)
        
        # Check login success or not success
        print (loginResult)
        logging.info(loginResult)
        if loginResult.find("230") >= 0:
            logging.info("login successful")
            print "1"
            Ftp.cwd('cps')
            ### Check list all file in folder cps
            # Ftp.retrlines('LIST')
            ### go to folder and download
            os.chdir("C:\CDR_NEW")
            if not os.path.exists(yesterday.strftime("%Y%m%d")):
                os.mkdir(yesterday.strftime("%Y%m%d"))
            else:
                print "co roi"
                logging.info("Folder %s is exist!", yt)
            os.chdir(yt)
            lpath = os.getcwd()
            #print lpath
            Ftp.cwd(yt)
            files = Ftp.retrlines('LIST')
            filenames = Ftp.nlst()
            #print filenames
            for filename in filenames:
                local_filename = os.path.join(lpath, filename)
                print local_filename
                file = open(local_filename, 'wb')
                Ftp.retrbinary('RETR '+ filename, file.write)
                file.close()

        else:
            print "2"
            time.sleep(120)
            logging.info("login failed, login again")
            loginResult = cdrFtp.login(CDRUsername, CDRPassword)
            logging.info(loginResult)
        
        Ftp.quit()
    except Exception as ex:
        logging.error("program fail: " + str(ex))
main()    
