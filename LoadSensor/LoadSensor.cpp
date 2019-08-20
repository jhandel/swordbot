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
    startRead(readCount, channel, ADS1256_7500SPS, ADS1256_GAIN_1);
}
void LoadSensor::startRead(long readCount, uint8_t channel, ADS1256_DRATE drate)
{
    startRead(readCount,  channel, drate, ADS1256_GAIN_1);
}
void LoadSensor::startRead(long readCount, uint8_t channel, ADS1256_DRATE drate, ADS1256_GAIN gain)
{

    if(readCount > bufferSize){
        RequestedRead = bufferSize;
    }else{
        RequestedRead = readCount;
    }
    Channel = channel;
    if(Channel>=8){
            return;
    }
    ADS1256_ConfigADC(gain,drate);
    DEV_Delay_ms(10);
    ADS1256_SetChannal(Channel);
    ADS1256_WriteCmd(CMD_SYNC);
    DEV_Delay_us(10);
    ADS1256_WriteCmd(CMD_WAKEUP);
    DEV_Delay_us(10);
    DEV_Digital_Write(DEV_CS_PIN, 0);
    ADS1256_WaitDRDY();
    DEV_Delay_us(8);
    DEV_SPI_WriteByte(CMD_RDATAC);       
    DEV_Delay_us(8);

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

void LoadSensor::processReads(){
    UBYTE buf[3] = {0,0,0};
    CurrentRead = 0;
    auto start = std::chrono::high_resolution_clock::now();
    printf("start reading ...\r\n"); 
    while(CurrentRead < RequestedRead){
        ADS1256_WaitDRDY();
        printf("reading ...\r\n"); 
        auto elapsed = std::chrono::high_resolution_clock::now() - start;
        ReadTimes[CurrentRead] = std::chrono::duration_cast<std::chrono::microseconds>(elapsed).count();
        buf[0] = DEV_SPI_ReadByte();
        DEV_Delay_us(3);
        buf[1] = DEV_SPI_ReadByte();
        DEV_Delay_us(3);
        buf[2] = DEV_SPI_ReadByte();
        //DEV_Delay_us(3);
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
    //ADC[i]*5.0/0x7fffff
}
