
#include <stdint.h>
#include <stdio.h>
#include <cstdlib>
#include "Switch.h"
#include "./../bcm2835drv/bcm2835drv.h"
#include <thread>
#include <chrono>
#include <unistd.h>

 void Switch::startMonitor(uint8_t pin, bool edge, long poll, SwitchCallback *cballback){
	 Pin = pin;
	 Edge = edge;
	 Poll = poll;
	 
	 DEV_pin_config(Pin, BCM2835_GPIO_FSEL_INPT);
	 DEV_pin_SetPud(Pin, BCM2835_GPIO_PUD_UP);

	 delete _callback;
	 _callback = 0;
	 _callback = cballback;
	 monitoring = true;
     if(switchMonitor.joinable()) switchMonitor.join();
	 switchMonitor = std::thread([=]() {
	 	printf("thread started\r\n");
        this->monitorPin();
    });
 }
 void Switch::monitorPin(){
	uint8_t lastValue = DEV_Digital_Read(Pin) == 1?0:1;

	while(monitoring){
		uint8_t edgeCheck = Edge?1:0;
		uint8_t currentValue = DEV_Digital_Read(Pin);
		if(currentValue != lastValue && currentValue == edgeCheck){	
			if (_callback) {
				_callback->run();
			}
		}
		lastValue = currentValue;
		std::this_thread::sleep_for(std::chrono::microseconds(Poll));
	}				
	printf("thread completed\r\n");
 }
 void Switch::stopMonitor()
  {
	delete _callback;
	_callback = 0;
    monitoring = false;
    if(switchMonitor.joinable()) switchMonitor.join();
  };