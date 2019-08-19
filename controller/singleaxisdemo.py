#!/usr/bin/python3
from Devices import ClearPathMotorSD
from Devices import LoadSensor
import time

def main():
    x = ClearPathMotorSD()
    time.sleep(.25)
    load = LoadSensor()
    x.attach(24,25,23)
    x.setMaxVelInMM(5000)
    x.setAccelInMM(4615)
    x.setDeccelInMM(4615)
    x.stepsPer100mm(1000)
    x.disable()
    time.sleep(.5)
    x.enable()

    load.startRead(15000,1)
    x.moveInMM(10000,2500)
    while not x.commandDone():
       time.sleep(.01)
    #time.sleep(1)
    x.stopMove()
    load.stopRead()
    x.disable()
    count = load.CurrentRead
    print("reads done:" + str(count))
    filenametime = time.time()
     
    f = open("test"+str(filenametime)+".txt", "a")
    for x in range(0, count):
        f.write(str(load.ReadingAt(x)*5.0/0x7fffff) + "," + str(load.TimeOfReading(x)) + '\n')
    f.close()


if __name__ == '__main__':
        main()