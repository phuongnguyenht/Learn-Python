# -*- coding:utf-8 -*-
import os
import glob
os.chdir("C:\Users\Phuong-Nguyen\Desktop\Mradio")
import pdb

for filename in glob.glob('*.txt'):
    print(filename)
    with open('C:\Users\Phuong-Nguyen\Desktop\mradio_trasau.txt', 'a') as f2:
        with open(filename) as file:
            line = file.readline()
            while line:
                # print(line)
                currentline = line.split(",", 1)
                print currentline[0]
                f2.write(currentline[0] +"\n")
                f2.write(line)
                line = file.readline()

        f2.close()