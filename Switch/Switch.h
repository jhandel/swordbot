
#ifndef Switch_h
#define Switch_h
#include <bcm2835.h>
#include <stdint.h>
#include <stdio.h>
#include <iostream>
#include <thread> 
#include "./../bcm2835drv/bcm2835drv.h"

class SwitchCallback {
  public:
	  virtual ~SwitchCallback() { }
	  virtual void run() { std::cout << "Callback::run()" << std::endl; }
};

class Switch
{
  public:
  Switch():_callback(0), switchMonitor(){
    DEV_ModuleInit();
    monitoring = false;
    Edge = false;
  }
  ~Switch(){
    stopMonitor();
    if(switchMonitor.joinable()) switchMonitor.join();
    DEV_ModuleExit();
    Edge = false;
  }
  void startMonitor(uint8_t pin, bool edge, long poll, SwitchCallback *cballback);
  void stopMonitor();
  uint8_t Pin;
  bool Edge;
  long Poll;

  private:
	  SwitchCallback *_callback;
    std::thread switchMonitor;
    bool monitoring;
    void monitorPin();
};
#endif