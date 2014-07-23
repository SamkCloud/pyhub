#!/bin/python  
from sys import argv
from datetime import datetime,timedelta

ansiTimeStart = datetime(1601,1,1)

lastLogon = timedelta(seconds= int(argv[1]) / 10000000)

print (ansiTimeStart+lastLogon)
