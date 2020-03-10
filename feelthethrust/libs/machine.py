from libs.Devices import ClearPathMotorSD
from libs.Devices import LoadSensor
from libs.Devices import Switch
from libs.Devices import SwitchCallback
import libs.Devices as cspace
from libs.settings import Settings
import time

class LimitHandler(SwitchCallback):
    def __init__(self, fn):
        SwitchCallback.__init__(self)
        self.callbackFunc = fn
    def run(self):
        self.callbackFunc()

class Machine():
    def __init__(self, settings):
        motor = ClearPathMotorSD()
        sensor = LoadSensor()
        switch = Switch()
        motor.attach(0,24,25,23)
        motor.enable()
        self.Motor = motor
        self.Sensor = sensor
        self.Switch = switch
        self.Settings = settings
        self.updateSettings()
        self.Sensor.setGainAndRate(cspace.ADS1256_2000SPS, cspace.ADS1256_GAIN_1)
        self.setSignalMode("single")

    def updateSettings(self):
        self.Motor.setMaxVelInMM(int(self.Settings.getValue("Speed")) * 2)
        self.Motor.setAccelInMM(int(self.Settings.getValue("acceleration")))
        self.Motor.setDeccelInMM(int(self.Settings.getValue("acceleration")))
        self.Motor.stepsPer100mm(self.Settings.getValue("stepsPer100MM"))
    
    def moveTo(self, mm, speed):
        self.Motor.moveInMM(mm,speed)

    def watchSwitch(self, action):
        switchCallback = LimitHandler(action).__disown__()
        self.Switch.startMonitor(21,False,100,switchCallback)

    def watchForce(self, action, target):
        loadSensorCallback = LimitHandler(action).__disown__()
        self.Sensor.startMonitor(0,target,loadSensorCallback)

    def stopMove(self):
        self.Motor.stopMove()

    def stopSwitch(self):
        self.Switch.stopMonitor()
    
    def stopForceWatch(self):
        self.Sensor.stopMonitor()
    
    def startSensor(self):
        self.Sensor.startRead(100000,0)

    def stopSensor(self):
        self.Sensor.stopRead()

    def takeSingleMeasurement(self):
        val = self.Sensor.singleMeasurement(0)
        return val
    
    def setSignalMode(self,mode):
        if (mode == "differential"):
            self.Sensor.SetMode(1)
        else:
            self.Sensor.SetMode(0)

    def getRawReadings(self):
        count = self.Sensor.CurrentRead
        results = [[],[]]
        for x in range(1, count):
            results[0].append(self.Sensor.TimeOfReading(x))
            results[1].append((self.Sensor.ReadingAt(x)))
        return results

    def getMovementReadings(self):
        count = self.Motor.GetLoggedPulseCount()
        results = [[],[]]
        for x in range(1, count):
            results[0].append(self.Motor.TimeOfLocation(x))
            results[1].append(self.Motor.LocationAt(x))
        return results

    def getForceReadings(self):
        count = self.Sensor.CurrentRead
        tear = self.Settings.getValue("tear")
        results = [[],[]]
        for x in range(1, count):
            results[0].append(self.Sensor.TimeOfReading(x))
            results[1].append((self.Sensor.ReadingAt(x) - tear))
        return results
    
    def enable(self):
        self.Motor.enable()
    
    def disable(self):
        self.Motor.disable()
        del self.Motor
        del self.Sensor
        del self.Switch

    