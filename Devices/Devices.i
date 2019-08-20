%module(directors="1") Devices 
%{ 
    /* Every thing in this file is being copied in  
     wrapper file. We include the C header file necessary 
     to compile the interface */
    #include "./../ClearPathMotorSD/ClearPathMotorSD.h" 
    #include "./../LoadSensor/LoadSensor.h" 
    #include "./../Switch/Switch.h" 

%}
%feature("director") SwitchCallback;

%include "./../ClearPathMotorSD/ClearPathMotorSD.h" 
%include "./../LoadSensor/LoadSensor.h" 
%include "./../Switch/Switch.h" 
%include "stdint.i"