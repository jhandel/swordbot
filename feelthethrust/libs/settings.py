import os
import sys
import time
import json

class Settings():
    def __init__(self, path, calibration):
        self.Path = path
        self.CalPath = calibration
        if(os.path.isfile(self.Path) and os.path.isfile(self.CalPath)):
            with open(self.Path) as json_data_file:
                self.settings = json.load(json_data_file)
            with open(self.CalPath) as json_calibration_data:
                self.calibration = json.load(json_calibration_data)["measurement"]
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
            "retractSpeed" : "1000",
            "fullScreen":"false",
            "tear":"229000",
            "calibration":"14",
            "targetForce":"0",
            "baselineForce":"0"
            }
            self.save()
        self.settings["homed"] = "false"
        self.settings["CommandedLocation"] = "-1"

    def save(self):
            with open(self.Path, 'w') as outfile:
                json.dump(self.settings, outfile)
    
    def getValue(self, key):
        val = self.settings[key]
        if(key == "homed"):
            return val == "true"
        elif (key == "fullScreen"):
            return val == "true"
        else:
            return float(val)

    def getMeasurement(self,rawValue):
        print(rawValue)
        count = len(self.calibration)
        print(count)
        returnval = 0
        for x in range(1, count):
            measurePool = self.calibration[x]
            if(measurePool[1] > rawValue):
                measureSteps = measurePool[3]
                returnvalStart = self.calibration[x-1][0]
                remainingSteps = rawValue - self.calibration[x-1][1]
                remainingMeasure = remainingSteps/measureSteps
                returnval = returnvalStart + remainingMeasure
                break
        return returnval

    def getRawForceSteps(self,measurement):
        count = len(self.calibration)
        returnval = self.calibration[1]
        for x in range(1, count):
            measurePool = self.calibration[x]
            if(measurePool[0] > measurement):
                measureSteps = measurePool[3]
                startingSteps = self.calibration[x-1][1]
                remainingmeasurement = measurement - self.calibration[x-1][0]
                remainingsteps = remainingmeasurement*measureSteps
                returnval = startingSteps + remainingsteps
                break
        return returnval


    def setValue(self, key, value):
        if(key == "homed"):
            if(value == True):
                self.settings["homed"] = "true"
            else:
                self.settings["homed"] = "false"
        else:
            self.settings[key] = str(value)