import datetime
from MKS910 import MKS910
import sys
import os
from datetime import datetime
from time import sleep

f = open("log.csv", "w")
trans = MKS910("COM3")
trans.open()
try:
    while True:
        f.write(f"{datetime.now()},{trans.read()}\n")
        sleep(0.2)
except KeyboardInterrupt:
    f.close()
    trans.close()
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)