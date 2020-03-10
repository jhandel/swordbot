#include <bcm2835.h>
#include <stdint.h>
#include <stdio.h>
#include <iostream>
#include <thread> 
#include <chrono>
#include "ADS1256.h"
#include "../bcm2835drv/bcm2835drv.h"
#include "LoadSensor.h"


void LoadSensor::startRead(long readCount, uint8_t channel)
{

    if(readCount > bufferSize){
        RequestedRead = bufferSize;
    }else{
        RequestedRead = readCount;
    }

    Channel = channel;

    if(ScanMode == 0){// 0  Single-ended input  8 channel1 Differential input  4 channe 
        if(Channel>=8){
            return;
        }
        ADS1256_SetChannal(Channel);
    }
    else{
        if(Channel>=4){
            return;
        }
        ADS1256_SetDiffChannal(Channel);
        printf("differental reading\r\n");
    }
    ADS1256_WriteCmd(CMD_SYNC);
    DEV_Delay_us(10);
    ADS1256_WriteCmd(CMD_WAKEUP);
    DEV_Delay_us(10);
    ADS1256_WaitDRDY();
    
    DEV_Digital_Write(DEV_CS_PIN, 0);
    DEV_Delay_us(8);
    DEV_SPI_WriteByte(CMD_RDATAC);       

    loadSensorThread = std::thread([=]() {
        this->processReads();
    });

}

bool LoadSensor::currentlyReading()
{
    if(CurrentRead < RequestedRead)
		return true;
	else
		return false;
}
void LoadSensor::stopRead(){
    RequestedRead = 0;
    if(loadSensorThread.joinable()) loadSensorThread.join();
}
void LoadSensor::clearData()
{
    std::fill_n(Reads, bufferSize, 0);
    std::fill_n(ReadTimes, bufferSize, 0);
}

uint32_t LoadSensor::ReadingAt(long index)
{
    if(index < bufferSize){
        return Reads[index];
    }
    return 0;
}
long LoadSensor::TimeOfReading(long index)
{
    if(index < bufferSize){
        return ReadTimes[index];
    }
    return 0;
}

uint32_t LoadSensor::singleMeasurement(uint8_t channel){
    return ADS1256_GetChannalValue(channel);
}

void LoadSensor::setGainAndRate(ADS1256_DRATE drate, ADS1256_GAIN gain){
    ADS1256_ConfigADC(gain,drate);
    ADS1256_WriteCmd(CMD_SELFCAL);
    DEV_Delay_ms(200);
}

void LoadSensor::processReads(){
    UBYTE buf[3] = {0,0,0};
    CurrentRead = 0;
    auto start = std::chrono::high_resolution_clock::now();
    while(CurrentRead < RequestedRead){
        ADS1256_WaitDRDY();
        DEV_Delay_us(7);
        auto elapsed = std::chrono::high_resolution_clock::now() - start;
        ReadTimes[CurrentRead] = std::chrono::duration_cast<std::chrono::microseconds>(elapsed).count();
        buf[0] = DEV_SPI_ReadByte();
        DEV_Delay_us(3);
        buf[1] = DEV_SPI_ReadByte();
        DEV_Delay_us(3);
        buf[2] = DEV_SPI_ReadByte();
        UDOUBLE read = ((UDOUBLE)buf[0] << 16) & 0x00FF0000;
        read |= ((UDOUBLE)buf[1] << 8);  /* Pay attention to It is wrong   read |= (buf[1] << 8) */
        read |= buf[2];
        if (read & 0x800000)
            read |= 0xFF000000;
        Reads[CurrentRead] = read;
        CurrentRead++;
        while(DEV_Digital_Read(DEV_DRDY_PIN) == 0);// you have to wait for the bit to rise or you can double read
    }
    DEV_SPI_WriteByte(CMD_SDATAC);
    DEV_Digital_Write(DEV_CS_PIN, 1);
}


void LoadSensor::startMonitor(uint8_t channel, double target, LoadSensorCallback *cballback){
	 delete _callback;
	 _callback = 0;
	 _callback = cballback;
	 monitoring = true;
     targetForce = target;
     Channel = channel;

    if(ScanMode == 0){// 0  Single-ended input  8 channel1 Differential input  4 channe 
        if(Channel>=8){
            return;
        }
        ADS1256_SetChannal(Channel);
    }
    else{
        if(Channel>=4){
            return;
        }
        ADS1256_SetDiffChannal(Channel);
        printf("differental reading\r\n");
    }
    ADS1256_WriteCmd(CMD_SYNC);
    DEV_Delay_us(10);
    ADS1256_WriteCmd(CMD_WAKEUP);
    DEV_Delay_us(10);
    ADS1256_WaitDRDY();
    
    DEV_Digital_Write(DEV_CS_PIN, 0);
    DEV_Delay_us(8);
    DEV_SPI_WriteByte(CMD_RDATAC);       


     if(loadSensorThread.joinable()) loadSensorThread.join();
	 loadSensorThread = std::thread([=]() {
	 	printf("thread started\r\n");
        this->monitorForce();
    });
 }
 void LoadSensor::monitorForce(){
    UBYTE buf[3] = {0,0,0};
    CurrentRead = 0;
    while(monitoring){
        ADS1256_WaitDRDY();
        DEV_Delay_us(7);
        buf[0] = DEV_SPI_ReadByte();
        DEV_Delay_us(3);
        buf[1] = DEV_SPI_ReadByte();
        DEV_Delay_us(3);
        buf[2] = DEV_SPI_ReadByte();
        UDOUBLE read = ((UDOUBLE)buf[0] << 16) & 0x00FF0000;
        read |= ((UDOUBLE)buf[1] << 8);  /* Pay attention to It is wrong   read |= (buf[1] << 8) */
        read |= buf[2];
        if (read & 0x800000)
            read |= 0xFF000000;
        if(read >= targetForce){	
			if (_callback) {
				_callback->run();
			}
		}
        while(DEV_Digital_Read(DEV_DRDY_PIN) == 0);// you have to wait for the bit to rise or you can double read
    }
    DEV_SPI_WriteByte(CMD_SDATAC);
    DEV_Digital_Write(DEV_CS_PIN, 1);			
	printf("thread completed\r\n");
 }
 void LoadSensor::stopMonitor()
  {
	delete _callback;
	_callback = 0;
    monitoring = false;
    if(loadSensorThread.joinable()) loadSensorThread.join();
  };

void LoadSensor::SetMode(uint8_t mode){
    ADS1256_SetMode(mode);
    ScanMode = mode;
}
