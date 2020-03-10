#ifndef LoadSensor_h
#define LoadSensor_h
#include <bcm2835.h>
#include <stdint.h>
#include <stdio.h>
#include <iostream>
#include <thread> 
#include <chrono>
#include "ADS1256.h"

class LoadSensorCallback {
  public:
	  virtual ~LoadSensorCallback() { }
	  virtual void run() { std::cout << "Callback::run()" << std::endl; }
};

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
            DEV_Delay_ms(200);
            ADS1256_init();
            
        }
        ~LoadSensor(){
            printf("closing channel");
            RequestedRead = 0;
            if(loadSensorThread.joinable()) loadSensorThread.join();
            DEV_ModuleExit();
        }

        void startMonitor(uint8_t channel, double target, LoadSensorCallback *cballback);
        void stopMonitor();

        void setGainAndRate(ADS1256_DRATE, ADS1256_GAIN);
        void startRead(long,uint8_t);
        uint32_t singleMeasurement(uint8_t);
        bool currentlyReading();
        void stopRead();
        void clearData();
        uint32_t ReadingAt(long);
        long TimeOfReading(long);
        uint8_t Channel;
        volatile long CurrentRead;
        long RequestedRead;
        void SetMode(uint8_t);
        ADS1256_DRATE DateRate;
        ADS1256_GAIN Gain;
        
    private:
        LoadSensorCallback *_callback;
        std::thread loadSensorThread;
        long bufferSize = 100000;
        void processReads();
        uint32_t Reads[100000];
        long ReadTimes[100000];
        uint8_t ScanMode = 0;
        bool monitoring;
        double targetForce;
        void monitorForce();
};
#endif