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

        self.calibrate500btn = ttk.Button(self, text="Calibrate 500g",command=self.calibrate)
        self.calibrate500btn.grid(row=3, column=0, sticky="nsew")

        self.TearBtn = ttk.Button(self, text="Tear",command=self.tear)
        self.TearBtn.grid(row=3, column=3, sticky="nsew")
        
    def calibrate(self):
        calculated = (self.currentRaw - self.currentTear)
        print(calculated)
        self.currentCalibration = 500/calculated
        print(self.currentCalibration)
        self.settings.setValue("calibration", self.currentCalibration)
        self.settings.save()
        messagebox.showinfo("Notification", "Configurations Saved")
    
    def tear(self):
        raw = self.currentRaw
        self.currentTear = raw
        self.settings.setValue("tear",raw)

    def runCheckLoop(self):
        while (self.isActive):

            self.currentRaw  = self.machine.takeSingleMeasurement() 
            calculated = (self.currentRaw - self.currentTear) * self.currentCalibration
            self.CurrentRawMeasurement.set ("Raw: {0:d}".format(int(self.currentRaw - self.currentTear)) + " steps")
            self.currentMeasurement.set ("Measured : {:10.1f}".format(calculated) + " g")
            self.currentLocationLbl.update()
            time.sleep(.1)

    def syncTab(self,active):
        if(active):
            self.isActive = True
            x = threading.Thread(target=lambda: self.runCheckLoop())
            x.start()
        else:
            self.isActive = False

    def disable(self):
        self.isActive = False
        time.sleep(.2)
    
    def setCalibration(self):
        self.settings.setValue("calibration", "1")
        self.settings.save()
        messagebox.showinfo("Notification", "Configurations Saved")
