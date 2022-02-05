from cv2 import add
import serial
from time import sleep
from datetime import datetime

class MKS910:
    def __init__(self, port, baudrate=9600, address=254):
        self.port = port
        self.baudrate = baudrate 
        self.address = address

    def open(self):
        self.ser = serial.Serial(self.port, self.baudrate, timeout=1)

    def close(self):
        self.ser.close()

    def __writeCommand__(self, command):

        self.ser.write(f"@{self.address}{command};FF".encode())
        result = self._readline()

        if b'NAK' in result:
            raise ValueError("Command not recognized")

        return result

    def _readline(self):
        eol = b';FF'
        leneol = len(eol)
        line = bytearray()
        while True:
            c = self.ser.read(1)
            if c:
                line += c
                if line[-leneol:] == eol:
                    break
            else:
                break
        return bytes(line)

    def identifyOn(self):
        return self.__writeCommand__("TST!ON")

    def identifyOff(self):
        return self.__writeCommand__("TST!OFF")

    def read(self, PR=4):
        # reads the pressure from the sensor 
        # PR = 1 MicroPirani 
        # PR = 2 Piezo
        # PR = 3 MicroPirani + Piezo (smoothed)
        # PR = 4 PR3 high resolution
        # PR = 5 differential pressure (for leak detection)

        result = self.__writeCommand__(f"PR{PR}").decode()
        # print(result)
        result = result[7:-3]

        # print(float(result))
        return float(result)
    


if __name__ == "__main__":
    mks = MKS910("COM3");
    mks.open()
    mks.identifyOn()
    now = datetime.now()
    for i in range(100):
        print(f"{datetime.now()-now} - {mks.read()}")
        now = datetime.now()
    mks.identifyOff()
    mks.close()

