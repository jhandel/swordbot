/*
  ClearPathMotorSD.h - Library for interfacing with Clearpath motors using an Arduino- Version 1
  Teknic 2017 Brendan Flosenzier

  This library is free software; you can redistribute it and/or
  modify it.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
*/

/* 
 A ClearPathMotorSD is activated by creating an instance of the ClearPathMotorSD class.

  There can several instances of ClearPathMotorSD however each must be attached to different pins.

  This class is used in conjuntion with the ClearPathStepGen class which manages and sends step pulses to each motor.
  
  Note: Each attached motor must have its direction/B pin connected to one of pins 8-13 on an arduino UNO (PORTB) 
  in order to work with the ClearPathStepGen object.  Other devices can be connected to pins 8-13 as well.
  If you are using another Arduino besides the UNO, the ClearPathStepGen must be modifyed to use a different port.

  The functions for a ClearPathMotorSD are:

   ClearPathMotorSD - default constructor for initializing the motor
   
   attach() - Attachs pins to this motor, and declares them as input/outputs

   stopMove()  - Interupts the current move, the motor may abruptly stop

   move() - sets the maximum veloctiy

   disable() - disables the motor

   enable() - enables the motor

   getCommandedPosition() - Returns the absolute cmomanded position where the position on enable=0

   readHLFB() - Returns the value of the motor's HLFB Pin

   setMaxVel() - sets the maximum veloctiy

   setMaxAccel() - sets the acceleration

   commandDone() - returns wheter or not there is a valid current command
   
 */
#ifndef ClearPathMotorSD_h
#define ClearPathMotorSD_h
#include <bcm2835.h>
#include <stdint.h>
#include <stdio.h>
#include <iostream>
#include <thread> 
#include "./../bcm2835drv/bcm2835drv.h"

class ClearPathMotorSD
{
  public:
  ClearPathMotorSD(): motorActivity(){
    moveStateX=3;
    PinA=0;
    PinB=0;
    PinE=0;
    PinH=0;
    Enabled=false;
    VelLimitQx=0;					
    AccLimitSteps=0;
    AccLimitMM=0;
    DeccLimitSteps=0;
    DeccLimitMM=0;			
    _TX=0;					
    _Ta=0;				
    _Td=0;				
    _Ts=0;
    _Vp=0;			
    CommandX=0;
    AbsPosition=0;
    StepsPer100mm = 10000;
    PulseLocation=0;
    DirForwardPinLevel = 1;
  }
  ~ClearPathMotorSD(){
    CommandX = 0;
    if(motorActivity.joinable()) motorActivity.join();
    DEV_ModuleExit();
  }
  void attach(uint8_t, int, int, int);
  void attach(uint8_t, int, int, int, int);
  bool moveInMM(long, int);
  void enable();
  long getCommandedPosition();
  bool readHLFB();
  void stopMove();
  void stepsPer100mm(double);
  void setMaxVelInMM(long); 
  void setAccelInMM(long);
  void setDeccelInMM(long);
  bool commandDone();
  void disable();
  double AxisLocation();
  

  
  uint8_t PinA;
  uint8_t PinB;
  uint8_t PinE;
  uint8_t PinH;
  bool Enabled; 
  int moveStateX;
  volatile long AbsPosition;
  long PulseLocation;
  uint8_t DirForwardPinLevel;


  private:
  void processMovement();
  volatile long CommandX;
  bool _direction;
  uint8_t _BurstX;
  std::thread motorActivity;

// All of the position, velocity and acceleration parameters are signed and in Q24.8,
// with all arithmetic performed in fixed point.

 int32_t VelLimitQx;					// Velocity limit
 double AccLimitSteps;					// Acceleration limit
 double DeccLimitSteps;					// Acceleration limit
 int32_t AccLimitMM;					// Acceleration limit
 int32_t DeccLimitMM;					// Acceleration limit
 double StepsPer100mm;
 float _TX;   //current time
 float _Ta;					// acceloration time
 float _Td;				// decelleration time
 float _Ts;        // Time at steady state
 float _Vp;				// pulses at steady state
 int pulseWidth;


};
#endif