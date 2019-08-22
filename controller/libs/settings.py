import os
import sys
import time
import json

class Settings():
    def __init__(self, path):
        self.Path = path
        self.settingsUpdated = lambda: print("saved")
        if(os.path.isfile(self.Path)):
            with open(self.Path) as json_data_file:
                self.settings = json.load(json_data_file)
        else:
            self.settings = {
            "acceleration" : "2500",
            "maxDistance" : "800",
            "stepsPer100MM" : "1000",
            "Speed" : "2000",
            "jogSpeed" : "200",
            "homeSpeed" : "10",
            "targetZero" : "600",
            "targetPen" : "6.35",
            "retract" : "100",
            "retractSpeed" : "1000"
            }
            self.save()
        self.settings["homed"] = "false"
        self.settings["CommandedLocation"] = "-1"

    def save(self):
            with open(self.Path, 'w') as outfile:
                json.dump(self.settings, outfile)
            self.settingsUpdated()
    
    def getValue(self, key):
        val = self.settings[key]
        if(key == "homed"):
            return val == "true"
        else:
            return float(val)

    def setValue(self, key, value):
        if(key == "homed"):
            if(value == True):
                self.settings["homed"] == "true"
            else:
                self.settings["homed"] == "false"
        else:
            self.settings[key] = str(value)