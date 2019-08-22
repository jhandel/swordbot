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
from ui.mainwindow import MainWindow


class MainApp():
    def __init__(self):
        self.settings = Settings("./config.json")
        self.machine = Machine(self.settings)
        self.window = MainWindow(self.settings, self.machine)
        self.window.testingFrame.runBtn.config(command= self.doStab)
        self.window.configFrame.homeBtn.config(command= self.homeMachine)

    def __del__(self):
        self.machine.disable()

    def runUI(self):
        self.window.mainloop()

    def doStab(self):
        print("I stabbed")
    
    def homeMachine(self):
        top = tk.Toplevel(self.window)
        frame = ttk.Frame(top)
        frame.pack()
        myLabel = ttk.Label(frame, text='Homing Machine')
        myLabel.pack()
        myText = tk.StringVar()
        myText.set("0 mm")
        myEntryBox = ttk.Entry(frame, state="disable", textvariable=myText)
        myEntryBox.pack()
        top.pack_slaves()
        homed = False
        self.machine.watchSwitch(self.machine.stopMove)
        self.machine.moveTo(-1000,int(self.settings.getValue("homeSpeed")))
        while(not homed):
            top.update()
            time.sleep(.1)
            location = "{:10.4f}".format(self.machine.Motor.AxisLocation()) + " mm"
            print(location)
            myText.set(location)
            homed = self.machine.Motor.commandDone()
            print(homed)
        top.destroy()
        self.machine.stopSwitch()
        self.machine.Motor.PulseLocation = 0
        self.settings.setValue("Homed","true")
        self.window.configFrame.syncSettings()

if __name__ == '__main__':
    app = MainApp()
    app.runUI()