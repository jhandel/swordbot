import tkinter as tk
from tkinter import Tk as ThemedTk
from tkinter import ttk
from ttkthemes import ThemedTk, THEMES
from ttkwidgets import ScaleEntry
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import messagebox
from PIL import Image
import threading
import time

class CalibrationFrame(ttk.Frame):
    def __init__(self,master,settings, machine):
        self.settings = settings
        self.machine = machine
        self.master = master
        ttk.Frame.__init__(self, master, width = 780, height = 400)
        self.columnconfigure(0, weight=1)
        self.currentCalibration = self.settings.getValue("calibration")
        self.currentTear = self.settings.getValue("tear")
        self.currentRaw = 0
        self.currentMeasurement = tk.StringVar(master, "Measured : {:10.4f}".format(0) + " g")
        self.currentLocationLbl  = ttk.Label(self, textvariable=self.currentMeasurement, font=('Helvetica', 17),  anchor=tk.CENTER)
        self.currentLocationLbl.grid(row=0,column=0, columnspan=3, sticky="nsew")

        self.CurrentRawMeasurement = tk.StringVar(master, "Raw : {:10.4f}".format(0) + " g")
        self.currentRawLocationLbl  = ttk.Label(self, textvariable=self.CurrentRawMeasurement, font=('Helvetica', 17),  anchor=tk.CENTER)
        self.currentRawLocationLbl.grid(row=2,column=0, columnspan=3, sticky="nsew")
        self.isActive = False

        self.TearBtn = ttk.Button(self, text="Tear",command=self.tear)
        self.TearBtn.grid(row=3, column=0, columnspan=3, sticky="nsew")

        self.isRunningCal = False
        self.vcmd = (self.register(self._checkNumberOnly), '%d', '%P')

        self.calibrationRunLabel = ttk.Label(self, text="Calibration weight",  anchor=tk.E)
        self.calibrationRunLabel.grid(row=4, column=0,sticky="e")
        self.calibrationRunVar = tk.StringVar()
        self.calibrationRunVar.set(0)
        self.calibrationRunEntry = ttk.Entry(self, width=35, font=('Helvetica', 16),validate='key', validatecommand=self.vcmd, textvariable=self.calibrationRunVar)
        self.calibrationRunEntry.grid(row=4, column=1,sticky="w")
        self.calibrationRunEntry.bind('<FocusIn>', lambda event: self.setCurrentFocusElement(self.calibrationRunEntry, self.calibrationRunVar))

        self.calibrate500btn = ttk.Button(self, text="Run Calibration",command=self.calibrate)
        self.calibrate500btn.grid(row=5, column=0,  columnspan=3, sticky="nsew")
        self.calibrate500btn.configure(state='disable')

    def _checkNumberOnly(self, action, value_if_allowed):
        if action != '1':
           return True
        try:
            return value_if_allowed.replace('.','',1).isdigit()
        except ValueError:
           return False

    def setCurrentFocusElement(self, element, valvar):
        element.select_range(0, len(valvar.get()))
        self.currentVar = valvar

    def calibrate(self):
        calculated = (self.currentRaw - self.currentTear)
        raw = 0
        self.isRunningCal = True
        time.sleep(.1)
        self.machine.startSensor()
        time.sleep(1)
        self.machine.stopSensor()
        self.isRunningCal = False
        results = self.machine.getRawReadings()
        count = len(results[1])
        for i in range(0, count):
            raw = raw + (results[1][i] - self.currentTear)
        calibrated = raw/count
        messagebox.showinfo("Notification", "measured value = {:d} for {}g".format(int(calibrated), self.calibrationRunVar.get()))
        f = open("calibration.csv", "a")
        f.write("{},{}\r\n".format(self.calibrationRunVar.get(),int(calibrated)))
        f.close()
        

    def tear(self):
        raw = 0
        self.isRunningCal = True
        time.sleep(.1)
        self.machine.startSensor()
        time.sleep(1)
        self.machine.stopSensor()
        self.isRunningCal = False
        results = self.machine.getRawReadings()
        count = len(results[1])
        for i in range(0, count):
            raw = raw + results[1][i]
        self.currentTear = int(raw/count)
        self.settings.setValue("tear",self.currentTear)
        self.calibrate500btn.configure(state='normal')

    def runCheckLoop(self):
        while (self.isActive):
            if(not self.isRunningCal):
                self.currentRaw  = self.machine.takeSingleMeasurement() 
                calculated = (self.currentRaw - self.currentTear) * self.currentCalibration
                self.CurrentRawMeasurement.set ("Raw: {0:d}".format(int(self.currentRaw - self.currentTear)) + " steps")
                self.currentMeasurement.set ("Measured : {:10.1f}".format(calculated) + " g")
                self.currentLocationLbl.update()
                time.sleep(.1)

    def syncTab(self,active):
        if(active):
            self.isActive = True
            self.isRunningCal = False
            x = threading.Thread(target=lambda: self.runCheckLoop())
            x.start()
        else:
            self.isActive = False
            self.isRunningCal = False

    def disable(self):
        self.isActive = False
        time.sleep(.2)
    
    def setCalibration(self):
        self.settings.setValue("calibration", "1")
        self.settings.save()
        messagebox.showinfo("Notification", "Configurations Saved")
