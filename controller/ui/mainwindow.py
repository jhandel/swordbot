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

class MainWindow(ThemedTk):
    def __init__(self, settings, machine):
        ThemedTk.__init__(self, themebg=True)
        #self.attributes('-fullscreen', True)
        self.settings = settings
        self.machine = machine
        self.set_theme("black")
        self.setStyles()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.title("Sword Bot 5000")

        self.tabs = ttk.Notebook(self)

        self.loadTestFrame()
        self.loadConfigFrame()
        self.loadJoggingFrame()
        self.tabs.add(self.configFrame, text='Configuration')
        self.tabs.add(self.joggingFrame, text='Jog Machine')
        self.tabs.add(self.testingFrame, text='Run Tests')
        self.tabs.bind("<<NotebookTabChanged>>", self.tabUpdate)
        self.tabs.grid(row=0,column=0, sticky="nsew")

        self.geometry("780x460")
        self.grid_propagate(0)

    def loadTestFrame(self):
        self.testingFrame = TestFrame(self.tabs, self.settings, self.machine)
    
    def loadConfigFrame(self):
        self.configFrame = ConfigFrame(self.tabs, self.settings, self.machine)
    
    def loadJoggingFrame(self):
        self.joggingFrame = JoggingFrame(self.tabs, self.settings, self.machine)

    def tabUpdate(self, event):
        self.configFrame.syncTab()
        self.joggingFrame.syncTab()
        self.testingFrame.syncTab()
    
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