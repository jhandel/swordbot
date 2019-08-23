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

    def __del__(self):
        self.machine.disable()
        self.window.disable()

    def runUI(self):
        self.window.mainloop()

if __name__ == '__main__':
    app = MainApp()
    app.runUI()