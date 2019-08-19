#ifndef LoadSensor_h
#define LoadSensor_h
#include <bcm2835.h>
#include <stdint.h>
#include <stdio.h>
#include <iostream>
#include <thread> 
#include <chrono>
#include "ADS1256.h"

class LoadSensor
{
    public:
        LoadSensor(): loadSensorThread(){
            DateRate = ADS1256_7500SPS;
            Gain = ADS1256_GAIN_1;
            RequestedRead = 0;
            CurrentRead = 0;
            Channel = 1;
            DEV_ModuleInit();
            ADS1256_init();
        }
        ~LoadSensor(){
            RequestedRead = 0;
            if(loadSensorThread.joinable()) loadSensorThread.join();
            DEV_ModuleExit();
        }

        void startRead(long,uint8_t);
        void startRead(long,uint8_t,ADS1256_DRATE);
        void startRead(long,uint8_t,ADS1256_DRATE, ADS1256_GAIN);
        bool currentlyReading();
        void stopRead();
        void clearData();
        uint32_t ReadingAt(long);
        long TimeOfReading(long);
        uint8_t Channel;
        volatile long CurrentRead;
        long RequestedRead;
        ADS1256_DRATE DateRate;
        ADS1256_GAIN Gain;
        
    private:
        std::thread loadSensorThread;
        long bufferSize = 100000;
        void processReads();
        uint32_t Reads[100000];
        long ReadTimes[100000];
};
#endif