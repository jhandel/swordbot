%module Devices 
%{ 
    /* Every thing in this file is being copied in  
     wrapper file. We include the C header file necessary 
     to compile the interface */
    #include "./../ClearPathMotorSD/ClearPathMotorSD.h" 
    #include "./../LoadSensor/LoadSensor.h" 

%}
 
%include "./../ClearPathMotorSD/ClearPathMotorSD.h" 
%include "./../LoadSensor/LoadSensor.h" 
%include "stdint.i"