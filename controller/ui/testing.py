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

class TestFrame(ttk.Frame):
    def __init__(self,master, settings, machine):
        self.settings = settings
        self.machine = machine
        self.master = master
        ttk.Frame.__init__(self, master, width = 780, height = 400)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(0, weight=0)
        self.rowconfigure(0, weight=0)
        self.grid(row=0,column=0, sticky="nsew")
        self.runLabel = ttk.Label(self, text="Run Program:", font=('Helvetica', 16) , width="20", anchor=tk.E )
        self.runBtn = ttk.Button(self, text="Stab", command=self.runTest)
        self.runLabel.grid(row=0, column=0,sticky="e")
        self.runBtn.grid(row=0, column=1,sticky="w")
        self.runNumVar = tk.StringVar()
        self.runNumVar.set("Run Number: " + str(int(self.settings.getValue("runNumber"))))
        self.runNumberLabel = ttk.Label(self, textvariable=self.runNumVar, font=('Helvetica', 16), width="20", anchor=tk.E )
        self.runNumberLabel.grid(row=0, column=2,sticky="e")


        self.figure = Figure()
        self.figure.set_figheight(3.7)
        self.figure.set_figwidth(7.8)
        self.axis = self.figure.add_subplot(111)
        self.axis.plot([], [], lw=2)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=4, sticky="nsew")
        self.clearGraphBtn = ttk.Button(self, text="Clear", command=self.clearResults)
        self.clearGraphBtn.grid(row=0, column=3,sticky="e")

    def clearResults(self):
        self.axis.clear()
        self.canvas.draw()
        self.canvas.flush_events()
        self.canvas.draw()

    def syncTab(self, active):
        if(not self.settings.getValue("homed")):
            self.runBtn.configure(state='disable')
        else:
            self.runBtn.configure(state='normal')

    def runTest(self):
        runNum = int(self.settings.getValue("runNumber"))
        runNum = runNum + 1
        self.settings.setValue("runNumber",runNum)
        self.settings.save()


        self.runNumVar.set("Run Number: " + str(runNum))
        self.runNumberLabel.update()
        penetration = self.settings.getValue("targetPen")
        thrustmove = self.settings.getValue("targetZero") + penetration
        if(thrustmove > self.settings.getValue("maxDistance")):
            return #if the thrust move is to far we quit

        distance = self.machine.Motor.AxisLocation() * -1
        if (distance != 0):
            self.moveHome()
        
        thrustspeed = int(self.settings.getValue("Speed"))

        retractmove = ( penetration * 2) * -1

        #start reading
        self.machine.startSensor()
        #thrust at target
        self.machine.moveTo(thrustmove,int(thrustspeed))
        finished = False
        while(not finished):
            time.sleep(.001)
            finished = self.machine.Motor.commandDone()
        time.sleep(.25)
        self.machine.stopSensor()
        results = self.machine.getReadings()
        self.axis.plot(results[0], results[2], lw=2)
        self.canvas.draw()
        self.canvas.flush_events()
        self.canvas.draw()
        
        self.moveHome()

        filenametime = time.time()
        acceleration = int(self.settings.getValue("acceleration"))
        f = open("run-measurements-" + str(runNum) + ".csv", "a")
        f.write('run,speed,distance,penetration,acceleration\r\n')
        f.write(str(runNum)+ ','+ str(thrustspeed) +','+ str(thrustmove) +','+ str(penetration) +','+ str(acceleration) +'\r\n')
        f.write('\r\n')
        f.write('\r\n')
        f.write('\r\n')
        f.write('microsecond,rawmeasurement,calcmeasurement\r\n')
        count = len(results[0])
        for i in range(0, count):
            f.write(str(results[0][i]) + "," + str(results[1][i]) + "," + str(results[2][i]) +'\r\n')
        f.close()
        f = open("run-movement-log-" + str(runNum) + ".csv", "a")
        f.write('run,speed,distance,penetration,acceleration\r\n')
        f.write(str(runNum)+ ','+ str(thrustspeed) +','+ str(thrustmove) +','+ str(penetration) +','+ str(acceleration) +'\r\n')
        f.write('\r\n')
        f.write('\r\n')
        f.write('\r\n')
        f.write('microsecond,location\r\n')
        count = len(results[0])
        for i in range(0, count):
            f.write(str(results[3][i]) + "," + str(results[4][i]) + '\r\n')
        f.close()


    def moveHome(self):
        homed = False
        self.machine.watchSwitch(self.machine.stopMove)
        self.machine.moveTo(self.settings.getValue("maxDistance") *-1,int(self.settings.getValue("homeSpeed")))
        while(not homed):
            time.sleep(.1)
            homed = self.machine.Motor.commandDone()
        self.machine.stopSwitch()
        self.machine.Motor.PulseLocation = 0
        self.settings.setValue("homed",True)