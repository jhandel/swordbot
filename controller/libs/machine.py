
from libs.Devices import ClearPathMotorSD
from libs.Devices import LoadSensor
from libs.Devices import Switch
from libs.Devices import SwitchCallback
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
        self.Settings.settingsUpdated = lambda: self.updateSettings()
        self.updateSettings()

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

    def stopMove(self):
        self.Motor.stopMove()

    def stopSwitch(self):
        self.Switch.stopMonitor()

    def stopSensor(self):
        self.Sensor.stopRead()
    
    def enable(self):
        self.Motor.enable()
    
    def disable(self):
        self.Motor.disable()

    