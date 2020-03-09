import tkinter as tk
from tkinter import Tk as ThemedTk
from tkinter import ttk
from ttkthemes import ThemedTk, THEMES
from ttkwidgets import ScaleEntry
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import messagebox
from PIL import Image
import time

class JoggingFrame(ttk.Frame):
    def __init__(self,master,settings, machine):
        self.settings = settings
        self.machine = machine
        self.master = master
        self.jogging = False
        ttk.Frame.__init__(self, master, width = 780, height = 400)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(0, weight=0)
        self.rowconfigure(0, weight=0)
        self.grid(row=0,column=0, sticky="nsew")
        self.titleLabel = ttk.Label(self, text="Jog to Target",  anchor=tk.CENTER)
        self.titleLabel.grid(row=0, column=0, columnspan=3)

        self.rapidHomeBtn = ttk.Button(self, text="Rapid Home",command=self.goHome)
        self.rapidHomeBtn.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.stepBtnFrame = ttk.Frame(self)
        self.stepBtnFrame.grid(row=2,column=0, columnspan=3)

        self.stepVar = tk.DoubleVar(master, 100)
        self.jogBtn0 = ttk.Radiobutton(self.stepBtnFrame, text = "0.1 mm", variable = self.stepVar, value = .1).grid(row=0, column=0, sticky="nsew")
        self.jogBtn1 = ttk.Radiobutton(self.stepBtnFrame, text = "1 mm", variable = self.stepVar, value = 1).grid(row=0, column=1, sticky="nsew")
        self.jogBtn2 = ttk.Radiobutton(self.stepBtnFrame, text = "10 mm", variable = self.stepVar, value = 10).grid(row=0, column=2, sticky="nsew")
        self.jogBtn3 = ttk.Radiobutton(self.stepBtnFrame, text = "100 mm", variable = self.stepVar, value = 100).grid(row=0, column=3, sticky="nsew")

        self.negButton = ttk.Button(self, text="<",command=lambda: self.jog(-1))
        self.negButton.grid(row=3, column=0, sticky="nsew")
        self.posButton = ttk.Button(self, text=">",command=lambda: self.jog(1))
        self.posButton.grid(row=3, column=2, sticky="nsew")

        self.locVar = tk.StringVar(master, "{:10.4f}".format(self.machine.Motor.AxisLocation()) + " mm")
        self.currentLocation  = ttk.Label(self, textvariable=self.locVar, font=('Helvetica', 17),  anchor=tk.CENTER)
        self.currentLocation.grid(row=4,column=0, columnspan=3)

        self.setTargetButton = ttk.Button(self, text="Set Target Surface",command=self.setTargetZero)
        self.setTargetButton.grid(row=5, column=0, columnspan=3, sticky="nsew")

    def goHome(self):
        while(self.jogging):
            return
        distance = self.machine.Motor.AxisLocation() * -1
        if (distance != 0):
            self.moveDistance(distance)
        self.jogging = False


    def syncTab(self, active):
        location = "{:10.4f}".format(self.machine.Motor.AxisLocation()) + " mm"
        self.locVar.set(location)
        if(not self.settings.getValue("homed")):
            self.setTargetButton.configure(state='disable')
            self.rapidHomeBtn.configure(state='disable')
        else:
            self.setTargetButton.configure(state='normal')
            self.rapidHomeBtn.configure(state='normal')
    
    def setTargetZero(self):
        self.settings.setValue("targetZero", self.machine.Motor.AxisLocation())
        self.settings.save()
        messagebox.showinfo("Notification", "Configurations Saved")

    def jog(self,dir):
        while(self.jogging):
            return
        self.jogging = True
        distance = dir * self.stepVar.get()
        max = self.settings.getValue("maxDistance")
        currentLoc = self.machine.Motor.AxisLocation()
        if(dir < 0):
            if(distance + currentLoc < 0):
                print("setting new distance")
                distance = currentLoc * -1
        else:
            if(distance + currentLoc > max):
                distance = max - currentLoc
        destination = distance + currentLoc
        if(distance != 0):
            self.moveDistance(distance)
        self.jogging = False

    def moveDistance(self, distance):
        speed = self.settings.getValue("jogSpeed")
        self.machine.moveTo(distance,int(speed))
        finished = False
        while(not finished):
            self.currentLocation.update()
            time.sleep(.1)
            location = "{:10.4f}".format(self.machine.Motor.AxisLocation()) + " mm"
            self.locVar.set(location)
            finished = self.machine.Motor.commandDone()
        self.machine.stopMove()