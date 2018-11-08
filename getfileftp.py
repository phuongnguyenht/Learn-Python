### Download file blacklist from VMS

import logging
import datetime
from ftplib import FTP
import time
import os.path

FORMAT = "%(asctime)-15s %(message)s"
logging.basicConfig(filename="ftp" + str(datetime.date.today()) + ".log", level=logging.INFO, format=FORMAT)

#logging.info("Begin login FTP download file")
def main():
    try:
        CDRServerHost = 'x.x.x.x'
        CDRUsername = 'user'
        CDRPassword = 'pass'
        filename = 'blacklistfolder1.txt'
        pwd = ""
        logging.info("start to connect to FTP server...")
        Ftp = FTP(CDRServerHost)
        loginResult = Ftp.login(CDRUsername, CDRPassword)
        print(loginResult)
        if loginResult.find("203") >=0:
            logging.info("Login successfult")
        else:
            time.sleep(120)
            logging.info("Login Failed, login again")
            loginResult = Ftp.login(CDRUsername, CDRPassword)
            logging.info(loginResult)
        if os.path.isfile(filename):
            os.remove(filename)
            print("remove file before download")
        else:
            Ftp.retrbinary("RETR " + filename, open(filename, 'wb').write)
            print("Download success")
        Ftp.quit()
    except Exception as ex:
        logging.error("program fail: " + str(ex))
main()
