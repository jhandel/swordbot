import tkinter as tk
from tkinter import Tk as ThemedTk
from tkinter import ttk
from ttkthemes import ThemedTk, THEMES
from ttkwidgets import ScaleEntry
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import messagebox
from PIL import Image
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
from tkinter.scrolledtext import ScrolledText
from tkinter import END

class TestFrame(ttk.Frame):
    def __init__(self,master, settings, machine):
        self.settings = settings
        self.machine = machine
        self.master = master
        ttk.Frame.__init__(self, master, width = 780, height = 400)
        self.rowconfigure(0, weight=0)
        self.grid(row=0,column=0, sticky="nsew")
        self.runBtnShirt = ttk.Button(self, text="Shirt (6N)", command=self.runShirtTest)
        self.runBtnShirt.grid(row=0, column=1,sticky="w")
        self.runBtnSilk = ttk.Button(self, text="Silk (47N)", command=self.runSilkTest)
        self.runBtnSilk.grid(row=0, column=2,sticky="w")
        self.runBtnLeather = ttk.Button(self, text="Leather (55N)", command=self.runLeatherTest)
        self.runBtnLeather.grid(row=0, column=3,sticky="w")
        self.runBtnLinen = ttk.Button(self, text="Linen (62N)", command=self.runLinenTest)
        self.runBtnLinen.grid(row=0, column=4,sticky="w")

        self.runBtnTarget = ttk.Button(self, text="Target", command=self.runTargetTest)
        self.runBtnTarget.grid(row=0, column=5,sticky="w")

        self.log = ScrolledText(self)
        self.log.grid(row=1, column=0, columnspan=6, sticky="nsew")

    def syncTab(self, active):
        print("testing")

    def runShirtTest(self):
        self.runTest(6)
    def runSilkTest(self):
        self.runTest(47)
    def runLeatherTest(self):
        self.runTest(55)
    def runLinenTest(self):
        self.runTest(62)
    def runTargetTest(self):
        self.runTest(self.settings.getValue("targetForce"))
    def runTest(self,targetForce):
        self.moveHome()
        penetration = self.settings.getValue("targetPen")
        thrustmove = self.settings.getValue("targetZero") + penetration
        baselineForce = self.settings.getValue("baselineForce")

        totalTargetForce = targetForce + baselineForce

        totalTargetForceSteps = self.settings.getRawForceSteps(totalTargetForce)

        if(thrustmove > self.settings.getValue("maxDistance")):
            return #if the thrust move is to far we quit

        distance = self.machine.Motor.AxisLocation() * -1
        if (distance != 0):
            self.moveHome()
        
        thrustspeed = int(self.settings.getValue("Speed"))

        retractmove = ( penetration * 2) * -1

        self.machine.moveTo(thrustmove,int(thrustspeed))


        #thrust at target
        print(totalTargetForceSteps)
        self.machine.moveTo(thrustmove,int(thrustspeed))
        finished = False
        time.sleep(.099)
        while(not finished):
            force = self.machine.takeSingleMeasurement() 
            if(force >= totalTargetForceSteps):
                self.machine.stopMove()
                self.log.insert(END,"{}".format(force)+'\n')
                calculated = self.settings.getMeasurement(force)
                self.log.insert(END,"{}".format(calculated)+'\n')
            finished = self.machine.Motor.commandDone()

        self.machine.moveTo(retractmove,int(thrustspeed))
        finished = False
        while(not finished):
            time.sleep(.001)
            finished = self.machine.Motor.commandDone()
        time.sleep(.25)
        self.moveHome()

    def moveHome(self):
        homed = False
        self.machine.watchSwitch(self.machine.stopMove)
        self.machine.moveTo(self.settings.getValue("maxDistance") *-1,int(self.settings.getValue("homeSpeed")))
        while(not homed):
            time.sleep(.1)
            homed = self.machine.Motor.commandDone()
        self.machine.stopSwitch()
        self.machine.moveTo(5,int(self.settings.getValue("homeSpeed")))
        homed = False
        while(not homed):
            time.sleep(.1)
            homed = self.machine.Motor.commandDone()
        self.machine.Motor.PulseLocation = 0
        self.settings.setValue("homed",True)