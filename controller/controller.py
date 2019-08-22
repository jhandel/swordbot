#!/usr/bin/python3
import os
import sys
import time
import json
from libs.Devices import ClearPathMotorSD
from libs.Devices import LoadSensor
from libs.Devices import Switch
from libs.Devices import SwitchCallback
import tkinter as tk
from tkinter import Tk as ThemedTk
from tkinter import ttk
from ttkthemes import ThemedTk, THEMES
from ttkwidgets import ScaleEntry
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import messagebox
from PIL import Image
from libs.settings import Settings
from libs.machine import LimitHandler
from libs.machine import Machine

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

    def setCurrentFocusElement(self, element, valvar):
        element.select_range(0, len(valvar.get()))
        self.currentVar = valvar

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
        self.stepsEntry = ttk.Entry(self.configFrame, width=35, font=('Helvetica', 17), validate='key', validatecommand=self.vcmd, textvariable=self.stepsVar)
        self.stepsEntry.grid(row=1, column=1,sticky="w")
        self.stepsEntry.bind('<FocusIn>', lambda event: self.setCurrentFocusElement(self.stepsEntry, self.stepsVar))

        self.accelLabel = ttk.Label(self.configFrame, text="Acceleration(mm/s^2)",  anchor=tk.E)
        self.accelLabel.grid(row=2, column=0,sticky="e")
        self.accelVar = tk.StringVar()
        self.accelVar.set(self.settings.getValue("acceleration"))
        self.accelEntry = ttk.Entry(self.configFrame, width=35, font=('Helvetica', 17), validate='key', validatecommand=self.vcmd, textvariable=self.accelVar)
        self.accelEntry.grid(row=2, column=1,sticky="w")
        self.accelEntry.bind('<FocusIn>', lambda event: self.setCurrentFocusElement(self.accelEntry, self.accelVar))

        self.limitLabel = ttk.Label(self.configFrame, text="Thrust Limit(mm)",  anchor=tk.E)
        self.limitLabel.grid(row=3, column=0,sticky="e")
        self.limitVar = tk.StringVar()
        self.limitVar.set(self.settings.getValue("maxDistance"))
        self.limitEntry = ttk.Entry(self.configFrame, width=35, font=('Helvetica', 17), validate='key', validatecommand=self.vcmd, textvariable=self.limitVar)
        self.limitEntry.grid(row=3, column=1,sticky="w")
        self.limitEntry.bind('<FocusIn>', lambda event: self.setCurrentFocusElement(self.limitEntry, self.limitVar))

        self.thrustSpeedLabel = ttk.Label(self.configFrame, text="Thrust Speed(mm/s)",  anchor=tk.E)
        self.thrustSpeedLabel.grid(row=4, column=0,sticky="e")
        self.thrustSpeedVar = tk.StringVar()
        self.thrustSpeedVar.set(self.settings.getValue("Speed"))
        self.thrustSpeedEntry = ttk.Entry(self.configFrame, width=35, font=('Helvetica', 17), validate='key', validatecommand=self.vcmd, textvariable=self.thrustSpeedVar)
        self.thrustSpeedEntry.grid(row=4, column=1,sticky="w")
        self.thrustSpeedEntry.bind('<FocusIn>', lambda event: self.setCurrentFocusElement(self.thrustSpeedEntry, self.thrustSpeedVar))

        self.homeSpeedLabel = ttk.Label(self.configFrame, text="Home Speed(mm/s)",  anchor=tk.E)
        self.homeSpeedLabel.grid(row=5, column=0,sticky="e")
        self.homeSpeedVar = tk.StringVar()
        self.homeSpeedVar.set(self.settings.getValue("homeSpeed"))
        self.homeSpeedEntry = ttk.Entry(self.configFrame, width=35, font=('Helvetica', 17),validate='key', validatecommand=self.vcmd, textvariable=self.homeSpeedVar)
        self.homeSpeedEntry.grid(row=5, column=1,sticky="w")
        self.homeSpeedEntry.bind('<FocusIn>', lambda event: self.setCurrentFocusElement(self.homeSpeedEntry, self.homeSpeedVar))

        self.surfaceLabel = ttk.Label(self.configFrame, text="Target Surface(mm)",  anchor=tk.E)
        self.surfaceLabel.grid(row=6, column=0,sticky="e")
        self.surfaceVar = tk.StringVar()
        self.surfaceVar.set(self.settings.getValue("targetZero"))
        self.surfaceEntry = ttk.Entry(self.configFrame, width=35, font=('Helvetica', 17),validate='key', validatecommand=self.vcmd, textvariable=self.surfaceVar)
        self.surfaceEntry.grid(row=6, column=1,sticky="w")
        self.surfaceEntry.bind('<FocusIn>', lambda event: self.setCurrentFocusElement(self.surfaceEntry, self.surfaceVar))

        self.penLabel = ttk.Label(self.configFrame, text="Target Penetration(mm)",  anchor=tk.E)
        self.penLabel.grid(row=7, column=0,sticky="e")
        self.penVar = tk.StringVar()
        self.penVar.set(self.settings.getValue("targetPen"))
        self.penEntry = ttk.Entry(self.configFrame, width=35, font=('Helvetica', 17),validate='key', validatecommand=self.vcmd, textvariable=self.penVar)
        self.penEntry.grid(row=7, column=1,sticky="w")
        self.penEntry.bind('<FocusIn>', lambda event: self.setCurrentFocusElement(self.penEntry, self.penVar))

        self.retractLabel = ttk.Label(self.configFrame, text="Retraction (mm)",  anchor=tk.E)
        self.retractLabel.grid(row=8, column=0,sticky="e")
        self.retractVar = tk.StringVar()
        self.retractVar.set(self.settings.getValue("retract"))
        self.retractEntry = ttk.Entry(self.configFrame, width=35, font=('Helvetica', 17),validate='key', validatecommand=self.vcmd, textvariable=self.retractVar)
        self.retractEntry.grid(row=8, column=1,sticky="w")
        self.retractEntry.bind('<FocusIn>', lambda event: self.setCurrentFocusElement(self.retractEntry, self.retractVar))

        self.retractSpeedLabel = ttk.Label(self.configFrame, text="Retraction Speed(mm/s)",  anchor=tk.E)
        self.retractSpeedLabel.grid(row=9, column=0,sticky="e")
        self.retractSpeedVar = tk.StringVar()
        self.retractSpeedVar.set(self.settings.getValue("retractSpeed"))
        self.retractSpeedEntry = ttk.Entry(self.configFrame, width=35, font=('Helvetica', 17),validate='key', validatecommand=self.vcmd, textvariable=self.retractSpeedVar)
        self.retractSpeedEntry.grid(row=9, column=1,sticky="w")
        self.retractSpeedEntry.bind('<FocusIn>', lambda event: self.setCurrentFocusElement(self.retractSpeedEntry, self.retractSpeedVar))

        self.saveSettingsBtn = ttk.Button(self.configFrame, text="Save Config",command=self.saveConfig)
        self.saveSettingsBtn.grid(row=10, column=0, columnspan=2, sticky="nsew")

        self.homeBtn = ttk.Button(self.configFrame, text="Home Machine",command=self.saveConfig)
        self.homeBtn.grid(row=10, column=3, sticky="nsew")

        self.numPadFrame = ttk.Frame(self.configFrame)
        self.numPadFrame.grid(row=1, column=3, rowspan=8, sticky="nsew")
        
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
                        padding=10,
                        font=('Helvetica', 17),
                        anchor=tk.CENTER
                        )
        style.configure('TEntry',
                        padding=5,
                        )

##Events


class MainApp():
    def __init__(self):
        self.settings = Settings("./config.json")
        self.machine = Machine(self.settings)
        self.window = MainWindow(self.settings)
        self.window.runBtn.config(command= self.doStab)
        self.window.homeBtn.config(command= self.homeMachine)

    def __del__(self):
        self.machine.disable()

    def runUI(self):
        self.window.mainloop()

    def doStab(self):
        print("I stabbed")
    
    def homeMachine(self):
        popup = tk.Toplevel()
        ttk.Label(popup, text="Homing Machine").grid(row=0,column=0)
        progress = 0
        progress_var = tk.StringVar()
        progress_var.set("0 mm")
        progress_bar = ttk.Label(popup, textvariable=progress_var).grid(row=0,column=0)
        popup.pack_slaves()
        homed = False
        self.machine.watchSwitch(self.machine.stopMove)
        print("start moving")
        self.machine.moveTo(1000,100)
        while(not homed):
            popup.update()
            time.sleep(.01)
            
            location = "{:10.4f}".format(self.machine.Motor.AxisLocation()) + " mm"
            print(location)
            progress_var.set(location)
            homed = self.machine.Motor.commandDone()
        return 0
        self.machine.Motor.PulseLocation = 0
        self.settings.setValue("Homed","true")
        self.machine.stopSwitch()
        popup.destroy()


if __name__ == '__main__':
    app = MainApp()
    app.runUI()