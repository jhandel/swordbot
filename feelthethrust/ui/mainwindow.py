import tkinter as tk
from tkinter import Tk as ThemedTk
from tkinter import ttk
from ttkthemes import ThemedTk, THEMES
from ttkwidgets import ScaleEntry
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import messagebox
from PIL import Image
from ui.testing import TestFrame
from ui.config import ConfigFrame
from ui.jogging import JoggingFrame
from ui.calibration import CalibrationFrame

class MainWindow(ThemedTk):
    def __init__(self, settings, machine):
        ThemedTk.__init__(self)
        self.fullscreen = False
        self.settings = settings
        self.machine = machine
        self.setStyles()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.title("Sword Bot 5000 Feel The Thrust")

        self.tabs = ttk.Notebook(self)

        self.loadTestFrame()
        self.loadConfigFrame()
        self.loadJoggingFrame()
        self.loadCalibrationFrame()
        self.tabs.add(self.configFrame, text='Configuration')
        self.tabs.add(self.calibrationFrame, text='Calibration')
        self.tabs.add(self.joggingFrame, text='Jog Machine')
        self.tabs.add(self.testingFrame, text='Run Tests')
        self.tabs.bind("<<NotebookTabChanged>>", self.tabUpdate)
        self.tabs.grid(row=0,column=0, sticky="nsew")

        self.geometry("780x460")
        self.grid_propagate(0)

    def loadTestFrame(self):
        self.testingFrame = TestFrame(self.tabs, self.settings, self.machine)
    
    def loadConfigFrame(self):
        self.configFrame = ConfigFrame(self.tabs, self.settings, self.machine, self.toggleFullScreen)
    
    def loadJoggingFrame(self):
        self.joggingFrame = JoggingFrame(self.tabs, self.settings, self.machine)

    def loadCalibrationFrame(self):
        self.calibrationFrame = CalibrationFrame(self.tabs, self.settings, self.machine)
    
    def toggleFullScreen(self):
            if(self.fullscreen):
                self.fullscreen = False
                self.attributes('-fullscreen', False)
            else:
                self.fullscreen = True
                self.attributes('-fullscreen', True)

    def tabUpdate(self, event):
        print(self.tabs.index("current"))
        self.configFrame.syncTab(self.tabs.index("current") == 0)
        self.calibrationFrame.syncTab(self.tabs.index("current") == 1)
        self.joggingFrame.syncTab(self.tabs.index("current") == 2)
        self.testingFrame.syncTab(self.tabs.index("current") == 3)
    
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
                    
        style.configure('TRadiobutton',
                        padding=10,
                        font=('Helvetica', 17),
                        anchor=tk.CENTER,
                        relief="flat"
                        )
    def disable(self):
        self.calibrationFrame.disable()
