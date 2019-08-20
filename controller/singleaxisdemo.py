#!/usr/bin/python3
from Devices import ClearPathMotorSD
from Devices import LoadSensor
from Devices import Switch
from Devices import SwitchCallback
import time

class LimitHandler(SwitchCallback):
    def __init__(self, fn):
        SwitchCallback.__init__(self)
        self.callbackFunc = fn
    def run(self):
        self.callbackFunc()


class Machine():
    def __init__(self, motor, sensor):
        self.Motor = motor
        self.Sensor = sensor
    def Stop(self):
        "stopping things"
        self.Motor.stopMove()
        self.Sensor.stopRead()


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
    m = Machine(x,load)
    limit = Switch()
    limitCallback = LimitHandler(m.Stop).__disown__()
    limit.startMonitor(21,False,100000,limitCallback)
    load.startRead(15000,1)
    x.moveInMM(10000,2500)
    #while not x.commandDone():
    time.sleep(1)
    m.Stop()
    time.sleep(1)
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
    limit.stopMonitor()


if __name__ == '__main__':
        main()