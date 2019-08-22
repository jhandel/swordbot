import tkinter as tk
from tkinter import Tk as ThemedTk
from tkinter import ttk
from ttkthemes import ThemedTk, THEMES
from ttkwidgets import ScaleEntry
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import messagebox
from PIL import Image

class TestFrame(ttk.Frame):
    def __init__(self,master):
        self.master = master
        ttk.Frame.__init__(self, master, width = 780, height = 400)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(0, weight=0)
        self.rowconfigure(0, weight=0)
        self.grid(row=0,column=0, sticky="nsew")
        self.runLabel = ttk.Label(self, text="Run Program:", width="20", anchor=tk.E )
        self.runBtn = ttk.Button(self, text="Stab")
        self.runLabel.grid(row=0, column=0,sticky="e")
        self.runBtn.grid(row=0, column=1,sticky="w")

