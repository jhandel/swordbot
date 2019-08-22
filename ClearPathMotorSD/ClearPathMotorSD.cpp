/*
  ClearPathMotorSD.h - Library for interfacing with Clearpath-SD motors using an Arduino- Version 1
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
#include <stdint.h>
#include <stdio.h>
#include <cstdlib>
#include "ClearPathMotorSD.h"
#include "./../bcm2835drv/bcm2835drv.h"
#include <thread>
#include <chrono>
#include <math.h>


/*		
	This is the three pin attach function.  
	It asociates the 1st number, as this motors Direction Pin,
	the 2nd number with the Step Pin,
	and the 3rd number with the Enable Pin
*/
void ClearPathMotorSD::attach(uint8_t fowardDirectionLevel, int APin, int BPin, int EPin)
{
	DEV_ModuleInit();
	PinA=APin;
	PinB=BPin;
	PinE=EPin;
	PinH=0;
	DirForwardPinLevel = fowardDirectionLevel;
	DEV_pin_config(PinA, BCM2835_GPIO_FSEL_OUTP);
	DEV_pin_config(PinB, BCM2835_GPIO_FSEL_OUTP);
	DEV_pin_config(EPin, BCM2835_GPIO_FSEL_OUTP);
}

/*		
	This is the four pin attach function.  
	It asociates the 1st number, as this motors Direction Pin,
	the 2nd number with the Step Pin,
	the 3rd number with the Enable Pin,
	and the 4th number as the HLFB Pin
*/
void ClearPathMotorSD::attach(uint8_t fowardDirectionLevel, int APin, int BPin, int EPin, int HPin)
{
	DEV_ModuleInit();
	PinA=APin;
	PinB=BPin;
	PinE=EPin;
	PinH=HPin;
	DirForwardPinLevel = fowardDirectionLevel;
	DEV_pin_config(PinA, BCM2835_GPIO_FSEL_OUTP);
	DEV_pin_config(PinB, BCM2835_GPIO_FSEL_OUTP);
	DEV_pin_config(EPin, BCM2835_GPIO_FSEL_OUTP);
	DEV_pin_config(PinH, BCM2835_GPIO_FSEL_INPT);
}

/*		
	This function clears the current move, and puts the motor in a
	move idle state, without disabling it, or clearing the position.

	This may cause an abrupt stop.
*/
void ClearPathMotorSD::stopMove()
{
    _TX=0;					
    _Ta=0;				
    _Td=0;				
    _Ts=0;
    _Vp=0;
	_BurstX=0;
	moveStateX = 3;
	CommandX=0;
	if(motorActivity.joinable()){
		motorActivity.join();
	}
}

/*		
	This function commands a directional move
	The move cannot be longer than 2,000,000 counts
	If there is a current move, it will NOT be overwritten

	The function will return true if the move was accepted
*/
bool ClearPathMotorSD::moveInMM(double dist, int speed)
{
	stopMove();
	_TX=1;
	std::cout << "Steps/1mm:" <<(StepsPer100mm/100) << std::endl;
	CommandX = (fabs(dist) * (StepsPer100mm/100));
	std::cout << "Command:" <<CommandX << std::endl;
	_Vp= (speed * (StepsPer100mm/100));		
	std::cout << "Speed:"<< _Vp << std::endl;			
    _Ta= (_Vp/AccLimitSteps);	
	std::cout << "Accell Time:"<< _Ta << std::endl;				
    _Td= (_Vp/DeccLimitSteps);		
	std::cout << "Decel Time:"<< _Td << std::endl;			
    _Ts= ((float)CommandX/(_Vp/1000000)); //- 0.5*(_Ta + _Td);
	std::cout << "Const Speed Time:"<< _Ts << std::endl;

	if(dist<0)
	{
		if(PinA!=0)
		{
			if (DirForwardPinLevel == LOW)
				DEV_Digital_Write(PinA,HIGH);
			else
				DEV_Digital_Write(PinA,LOW);
			_direction=true;
		}
	}
	else
	{
		if(PinA!=0)
		{
			if (DirForwardPinLevel == LOW)
				DEV_Digital_Write(PinA,LOW);
			else
				DEV_Digital_Write(PinA,HIGH);
			_direction=false;
		}
	}
	motorActivity = std::thread([=]() {
        this->processMovement();
    });
	return true;
}

void ClearPathMotorSD::processMovement(){
	
	while(CommandX > 0){
		int pw = 10000;
		//std::cout << "current time:"<< _TX << std::endl;
		//std::cout << "Standard velocity" << _Ta + _Ts << std::endl;
		if (_TX < _Ta){
			pw = ((_TX * _Ta));
			//std::cout << "accel speed:"<< pw << std::endl;
		}else if(_TX > _Ta && _TX < _Ta + _Ts){
			//std::cout << "constant speed:"<< _Vp << std::endl;	
			pw = (1000000/_Vp);
			//std::cout << "constant speed:"<< pw << std::endl;
		}else{
			pw = abs(((1000000/_Vp)) - ((_TX * _Td) * 1000000));
			//std::cout << "decel speed:"<< pw << std::endl;
		}
		DEV_Digital_Write(PinB,HIGH);
		DEV_Delay_us(2);
		DEV_Digital_Write(PinB,LOW);
		DEV_Delay_us(pw - 2);
		_TX = _TX + (pw);
		CommandX --;
		if(!_direction)
		{
			PulseLocation++;
		}else{
			PulseLocation--;
		}
	}
}

double ClearPathMotorSD::AxisLocation(){
	double location = (double)PulseLocation/StepsPer100mm * 100;
	double specificLoc = floor(location*10000)/10000;
	return specificLoc;
}

/*		

*/
void ClearPathMotorSD::setMaxVelInMM(long velMax)
{
	VelLimitQx = velMax;
}
/*		

*/
void ClearPathMotorSD::setAccelInMM(long accel)
{
	AccLimitMM = accel;
    AccLimitSteps=(AccLimitMM * (StepsPer100mm/100));

}

void ClearPathMotorSD::stepsPer100mm(double steps){

	StepsPer100mm = steps;
	AccLimitSteps=(AccLimitMM * (StepsPer100mm/100));
	DeccLimitSteps = (DeccLimitMM * (StepsPer100mm/100));
}

void ClearPathMotorSD::setDeccelInMM(long deccel)
{
    DeccLimitMM = deccel;
	DeccLimitSteps = (DeccLimitMM * (StepsPer100mm/100));

}


/*		
	This function returns the absolute commanded position
*/
long ClearPathMotorSD::getCommandedPosition()
{
	return AbsPosition;
}

/*		
	This function returns true if there is no current command
	It returns false if there is a current command
*/
bool ClearPathMotorSD::commandDone()
{
	if(CommandX <= 0) {
		if(motorActivity.joinable()){
			motorActivity.join();
		}
		return true;
	}else{
		return false;
	}
		
}


/*		
	This function returns the value of the HLFB Pin
*/
bool ClearPathMotorSD::readHLFB()
{
	if(PinH!=0)
		return !DEV_Digital_Read(PinH);
	else
		return false;
}

/*		
	This function enables the motor
*/
void ClearPathMotorSD::enable()
{

	if(PinE!=0)
		DEV_Digital_Write(PinE,HIGH);
	AbsPosition=0;
	Enabled=true;
}

/*		
	This function returns zeros out the current command, and digitally writes the enable pin LOW
	If the motor was not attached with an enable pin, then it just zeros the command
*/
void ClearPathMotorSD::disable()
{

	if(PinE!=0)
		DEV_Digital_Write(PinE,LOW);
	Enabled=false;
    _TX=0;					
    _Ta=0;				
    _Td=0;				
    _Ts=0;
    _Vp=0;
	_BurstX=0;
	moveStateX = 3;
	CommandX=0;
	if(motorActivity.joinable()){
		motorActivity.join();
	}
}
