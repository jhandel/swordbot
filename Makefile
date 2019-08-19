CC = g++

DEBUG = -g -O0 -Wall
CFLAGS += $(DEBUG) 

STEPGENLIB = -lbcm2835 -lm -pthread

PYTHONCFLAGS = -I/usr/include/python3.5m -I/usr/include/python3.5m  -Wno-unused-result -Wsign-compare -g -fdebug-prefix-map=/build/python3.5-6waWnr/python3.5-3.5.3=. -fstack-protector-strong -Wformat -Werror=format-security  -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes
PYTHONLDLAGS = -L/usr/lib/python3.5/config-3.5m-arm-linux-gnueabihf -L/usr/lib -lpython3.5m -lpthread -ldl  -lutil -lm  -Xlinker -export-dynamic -Wl,-O1 -Wl,-Bsymbolic-functions


./controller/_Devices.so:./bin/ClearPathMotorSD.o ./bin/Devices.o ./bin/LoadSensor.o ./bin/ADS1256.o ./bin/bcm2835drv.o
	$(CC) -shared ./bin/ClearPathMotorSD.o ./bin/Devices.o  ./bin/LoadSensor.o ./bin/ADS1256.o ./bin/bcm2835drv.o -o ./bin/_Devices.so  $(PYTHONLDLAGS) -Wl,--whole-archive  $(STEPGENLIB) -Wl,--no-whole-archive
	cp ./bin/_Devices.so ./controller/_Devices.so
	cp ./Devices/Devices.py ./controller/Devices.py

./bin/Devices.o : ./Devices/Devices_wrap.cxx
	$(CC) $(CFLAGS) -O2 -c -fPIC  $<  -o $@  $(STEPGENLIB) $(PYTHONCFLAGS)

./bin/ClearPathMotorSD.o : ./ClearPathMotorSD/ClearPathMotorSD.cpp
	$(CC) $(CFLAGS) -c -fPIC $<  -o $@  $(STEPGENLIB)

./bin/LoadSensor.o : ./LoadSensor/LoadSensor.cpp
	$(CC) $(CFLAGS) -c -fPIC $<  -o $@  $(STEPGENLIB)

./bin/ADS1256.o : ./LoadSensor/ADS1256.c
	$(CC) $(CFLAGS) -c -fPIC $<  -o $@  $(STEPGENLIB)

./bin/bcm2835drv.o : ./bcm2835drv/bcm2835drv.c
	$(CC) $(CFLAGS) -c -fPIC $<  -o $@  $(STEPGENLIB)

clean :
	rm -f ./bin/*.o
	rm -f ./bin/*.so