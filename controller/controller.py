#!/usr/bin/python3
import os
import sys
from Devices import ClearPathMotorSD
from Devices import LoadSensor
from Devices import Switch
from Devices import SwitchCallback
import tkinter as tk
from tkinter import Tk as ThemedTk
from tkinter import ttk
from ttkthemes import ThemedTk, THEMES
from ttkwidgets import ScaleEntry
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import messagebox
from PIL import Image
import time
import json
from pynput.keyboard import Key, Controller

class LimitHandler(SwitchCallback):
    def __init__(self, fn):
        SwitchCallback.__init__(self)
        self.callbackFunc = fn
    def run(self):
        self.callbackFunc()

class Settings():
    def __init__(self, path):
        self.Path = path
        if(os.path.isfile(self.Path)):
            with open(self.Path) as json_data_file:
                self.settings = json.load(json_data_file)
        else:
            self.settings = {
            "acceleration" : "2500",
            "maxDistance" : "800",
            "stepsPer100MM" : "1000",
            "Speed" : "2000",
            "homeSpeed" : "10",
            "targetZero" : "600",
            "targetPen" : "6.35",
            "retract" : "100",
            "retractSpeed" : "1000"
            }
            self.save()
        self.settings["homed"] = "false"

    def save(self):
            with open(self.Path, 'w') as outfile:
                json.dump(self.settings, outfile)
    
    def getValue(self, key):
        val = self.settings[key]
        if(key == "homed"):
            return val == "true"
        else:
            return float(val)

    def setValue(self, key, value):
        if(key == "homed"):
            if(value == True):
                self.settings["homed"] == "true"
            else:
                self.settings["homed"] == "false"
        else:
            self.settings[key] = str(value)
    


class Machine():
    def __init__(self, motor, sensor):
        self.Motor = motor
        self.Sensor = sensor
    def Stop(self):
        "stopping things"
        self.Motor.stopMove()
        self.Sensor.stopRead()

class MainWindow(ThemedTk):
    def __init__(self, settings):
        ThemedTk.__init__(self, themebg=True)
        self.settings = settings
        self.set_theme("black")
        self.setStyles()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.title("Sword Bot 5000")

        self.tabs = ttk.Notebook(self)
        self.vcmd = (self.register(self._checkNumberOnly), '%d', '%P')
        
        self.loadTestFrame()
        self.loadConfigFrame()
        self.tabs.add(self.configFrame, text='Configuration')
        self.tabs.add(self.testingFrame, text='Testing')

        self.tabs.grid(row=0,column=0, sticky="nsew")

        self.geometry("780x460")
        self.grid_propagate(0)

    def loadTestFrame(self):
        self.testingFrame = ttk.Frame(self.tabs, width = 780, height = 400)
        self.testingFrame.columnconfigure(1, weight=1)
        self.testingFrame.columnconfigure(0, weight=0)
        self.testingFrame.rowconfigure(0, weight=0)
        self.testingFrame.grid(row=0,column=0, sticky="nsew")
        self.runLabel = ttk.Label(self.testingFrame, text="Run Program:", width="20", anchor=tk.E )
        self.runBtn = ttk.Button(self.testingFrame, text="Stab")
        self.runLabel.grid(row=0, column=0,sticky="e")
        self.runBtn.grid(row=0, column=1,sticky="w")

    def _checkNumberOnly(self, action, value_if_allowed):
        if action != '1':
           return True
        try:
            return value_if_allowed.isnumeric()
        except ValueError:
           return False

    def setCurrentFocusElement(self, element):
        self.currentVar = element
        print("focus set")

    def numPadCallback(self, key):
        val = self.currentVar.get()
        if(key == "bs"):
            if len(val) > 0:
                val = val[:-1]
        elif key == "." :
            if(not key in val):
                val = val + str(key)
        else:
            val = val + str(key)
        self.currentVar.set(val)
    
    def loadConfigFrame(self):

        self.configFrame = ttk.Frame(self.tabs, width = 780, height = 400)
        self.configFrame.columnconfigure(1, weight=1)
        self.configFrame.columnconfigure(0, weight=0)
        self.configFrame.rowconfigure(0, weight=0)
        self.configFrame.grid(row=0,column=0, sticky="nsew")
        self.titleLabel = ttk.Label(self.configFrame, text="The Swordbot Configurations",  anchor=tk.CENTER)
        self.titleLabel.grid(row=0, column=0, columnspan=3)

        self.stepsLabel = ttk.Label(self.configFrame, text="Steps Per 100mm",  anchor=tk.E)
        self.stepsLabel.grid(row=1, column=0,sticky="e")
        self.stepsVar = tk.StringVar()
        self.stepsVar.set(self.settings.getValue("stepsPer100MM"))
        self.stepsEntry = ttk.Entry(self.configFrame, width=35, validate='key', validatecommand=self.vcmd, textvariable=self.stepsVar)
        self.stepsEntry.grid(row=1, column=1,sticky="w")
        self.stepsEntry.bind('<FocusIn>', lambda event: self.setCurrentFocusElement(self.stepsVar))

        self.accelLabel = ttk.Label(self.configFrame, text="Acceleration(mm/s^2)",  anchor=tk.E)
        self.accelLabel.grid(row=2, column=0,sticky="e")
        self.accelVar = tk.StringVar()
        self.accelVar.set(self.settings.getValue("acceleration"))
        self.accelEntry = ttk.Entry(self.configFrame, width=35, validate='key', validatecommand=self.vcmd, textvariable=self.accelVar)
        self.accelEntry.grid(row=2, column=1,sticky="w")
        self.accelEntry.bind('<FocusIn>', lambda event: self.setCurrentFocusElement(self.accelVar))

        self.limitLabel = ttk.Label(self.configFrame, text="Thrust Limit(mm)",  anchor=tk.E)
        self.limitLabel.grid(row=3, column=0,sticky="e")
        self.limitVar = tk.StringVar()
        self.limitVar.set(self.settings.getValue("maxDistance"))
        self.limitEntry = ttk.Entry(self.configFrame, width=35, validate='key', validatecommand=self.vcmd, textvariable=self.limitVar)
        self.limitEntry.grid(row=3, column=1,sticky="w")
        self.limitEntry.bind('<FocusIn>', lambda event: self.setCurrentFocusElement(self.limitVar))

        self.thrustSpeedLabel = ttk.Label(self.configFrame, text="Thrust Speed(mm/s)",  anchor=tk.E)
        self.thrustSpeedLabel.grid(row=4, column=0,sticky="e")
        self.thrustSpeedVar = tk.StringVar()
        self.thrustSpeedVar.set(self.settings.getValue("Speed"))
        self.thrustSpeedEntry = ttk.Entry(self.configFrame, width=35, validate='key', validatecommand=self.vcmd, textvariable=self.thrustSpeedVar)
        self.thrustSpeedEntry.grid(row=4, column=1,sticky="w")
        self.thrustSpeedEntry.bind('<FocusIn>', lambda event: self.setCurrentFocusElement(self.thrustSpeedVar))

        self.homeSpeedLabel = ttk.Label(self.configFrame, text="Home Speed(mm/s)",  anchor=tk.E)
        self.homeSpeedLabel.grid(row=5, column=0,sticky="e")
        self.homeSpeedVar = tk.StringVar()
        self.homeSpeedVar.set(self.settings.getValue("homeSpeed"))
        self.homeSpeedEntry = ttk.Entry(self.configFrame, width=35, validate='key', validatecommand=self.vcmd, textvariable=self.homeSpeedVar)
        self.homeSpeedEntry.grid(row=5, column=1,sticky="w")
        self.homeSpeedEntry.bind('<FocusIn>', lambda event: self.setCurrentFocusElement(self.homeSpeedVar))

        self.surfaceLabel = ttk.Label(self.configFrame, text="Target Surface(mm)",  anchor=tk.E)
        self.surfaceLabel.grid(row=6, column=0,sticky="e")
        self.surfaceVar = tk.StringVar()
        self.surfaceVar.set(self.settings.getValue("targetZero"))
        self.surfaceEntry = ttk.Entry(self.configFrame, width=35, validate='key', validatecommand=self.vcmd, textvariable=self.surfaceVar)
        self.surfaceEntry.grid(row=6, column=1,sticky="w")
        self.surfaceEntry.bind('<FocusIn>', lambda event: self.setCurrentFocusElement(self.surfaceVar))

        self.penLabel = ttk.Label(self.configFrame, text="Target Penetration(mm)",  anchor=tk.E)
        self.penLabel.grid(row=7, column=0,sticky="e")
        self.penVar = tk.StringVar()
        self.penVar.set(self.settings.getValue("targetPen"))
        self.penEntry = ttk.Entry(self.configFrame, width=35, validate='key', validatecommand=self.vcmd, textvariable=self.penVar)
        self.penEntry.grid(row=7, column=1,sticky="w")
        self.penEntry.bind('<FocusIn>', lambda event: self.setCurrentFocusElement(self.penVar))

        self.retractLabel = ttk.Label(self.configFrame, text="Retraction (mm)",  anchor=tk.E)
        self.retractLabel.grid(row=8, column=0,sticky="e")
        self.retractVar = tk.StringVar()
        self.retractVar.set(self.settings.getValue("retract"))
        self.retractEntry = ttk.Entry(self.configFrame, width=35, validate='key', validatecommand=self.vcmd, textvariable=self.retractVar)
        self.retractEntry.grid(row=8, column=1,sticky="w")
        self.retractEntry.bind('<FocusIn>', lambda event: self.setCurrentFocusElement(self.retractVar))

        self.retractSpeedLabel = ttk.Label(self.configFrame, text="Retraction Speed(mm/s)",  anchor=tk.E)
        self.retractSpeedLabel.grid(row=9, column=0,sticky="e")
        self.retractSpeedVar = tk.StringVar()
        self.retractSpeedVar.set(self.settings.getValue("retractSpeed"))
        self.retractSpeedEntry = ttk.Entry(self.configFrame, width=35, validate='key', validatecommand=self.vcmd, textvariable=self.retractSpeedVar)
        self.retractSpeedEntry.grid(row=9, column=1,sticky="w")
        self.retractSpeedEntry.bind('<FocusIn>', lambda event: self.setCurrentFocusElement(self.retractSpeedVar))

        self.saveSettingsBtn = ttk.Button(self.configFrame, text="Save Config",command=self.saveConfig)
        self.saveSettingsBtn.grid(row=10, column=0, columnspan=3, sticky="nsew")

        self.numPadFrame = ttk.Frame(self.configFrame)
        self.numPadFrame.grid(row=1, column=3, rowspan=9, sticky="nsew")
        
        self.num7Btn = ttk.Button(self.numPadFrame, text="7",command=lambda: self.numPadCallback(7))
        self.num7Btn.grid(row=0, column=0, sticky="nsew")
        self.num8Btn = ttk.Button(self.numPadFrame, text="8",command=lambda: self.numPadCallback(8))
        self.num8Btn.grid(row=0, column=1, sticky="nsew")
        self.num9Btn = ttk.Button(self.numPadFrame, text="9",command=lambda: self.numPadCallback(9))
        self.num9Btn.grid(row=0, column=2, sticky="nsew")

        self.num4Btn = ttk.Button(self.numPadFrame, text="4",command=lambda: self.numPadCallback(4))
        self.num4Btn.grid(row=1, column=0, sticky="nsew")
        self.num5Btn = ttk.Button(self.numPadFrame, text="5",command=lambda: self.numPadCallback(5))
        self.num5Btn.grid(row=1, column=1, sticky="nsew")
        self.num6Btn = ttk.Button(self.numPadFrame, text="6",command=lambda: self.numPadCallback(6))
        self.num6Btn.grid(row=1, column=2, sticky="nsew")

        self.num1Btn = ttk.Button(self.numPadFrame, text="1",command=lambda: self.numPadCallback(1))
        self.num1Btn.grid(row=2, column=0, sticky="nsew")
        self.num2Btn = ttk.Button(self.numPadFrame, text="2",command=lambda: self.numPadCallback(2))
        self.num2Btn.grid(row=2, column=1, sticky="nsew")
        self.num3Btn = ttk.Button(self.numPadFrame, text="3",command=lambda: self.numPadCallback(3))
        self.num3Btn.grid(row=2, column=2, sticky="nsew")

        self.num0Btn = ttk.Button(self.numPadFrame, text="0",command=lambda: self.numPadCallback(0))
        self.num0Btn.grid(row=3, column=1, sticky="nsew")

        self.numPointBtn = ttk.Button(self.numPadFrame, text=".",command=lambda: self.numPadCallback("."))
        self.numPointBtn.grid(row=4, column=0, sticky="nsew")
        self.numBSBtn = ttk.Button(self.numPadFrame, text="Back Space",command=lambda: self.numPadCallback("bs"))
        self.numBSBtn.grid(row=4, column=1, columnspan=2, sticky="nsew")

    
    def saveConfig(self):
        self.settings.setValue("retractSpeed",self.retractSpeedVar.get())
        self.settings.setValue("retract",self.retractVar.get())
        self.settings.setValue("targetPen",self.penVar.get())
        self.settings.setValue("targetZero",self.surfaceVar.get())
        self.settings.setValue("homeSpeed",self.homeSpeedVar.get())
        self.settings.setValue("Speed",self.thrustSpeedVar.get())
        self.settings.setValue("maxDistance",self.limitVar.get())
        self.settings.setValue("acceleration",self.accelVar.get())
        self.settings.setValue("stepsPer100MM",self.stepsVar.get())
        self.settings.save()
        messagebox.showinfo("Notification", "Configurations Saved")

    def setStyles(self):
        style = ttk.Style(self)
        style.configure('TButton',
                        padding=20,
                        )

##Events
def doStab():
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
    load.startRead(15000,1)
    x.moveInMM(1000,2500)
    while not x.commandDone():
        time.sleep(.01)
    m.Stop()
    x.disable()
    count = load.CurrentRead
    print("reads done:" + str(count))
    filenametime = time.time()
     
    f = open("test"+str(filenametime)+".txt", "a")
    for x in range(0, count):
        f.write(str(load.ReadingAt(x)*5.0/0x7fffff) + "," + str(load.TimeOfReading(x)) + '\n')
    f.close()
    

if __name__ == '__main__':
    settings = Settings("./config.json")
    window = MainWindow(settings)
    window.runBtn.config(command=doStab)
    window.mainloop()
