CC = g++

DEBUG = -g -O0 -Wall
CFLAGS += $(DEBUG) 

STEPGENLIB = -lbcm2835 -lm -pthread

PYTHONCFLAGS = -I/usr/include/python3.5m -I/usr/include/python3.5m  -Wno-unused-result -Wsign-compare -g -fdebug-prefix-map=/build/python3.5-6waWnr/python3.5-3.5.3=. -fstack-protector-strong -Wformat -Werror=format-security  -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes
PYTHONLDLAGS = -L/usr/lib/python3.5/config-3.5m-arm-linux-gnueabihf -L/usr/lib -lpython3.5m -lpthread -ldl  -lutil -lm  -Xlinker -export-dynamic -Wl,-O1 -Wl,-Bsymbolic-functions
 
./bin/libLoadSensor.so:./bin/LoadSensor.o ./bin/LoadSensor_wrap.o ./bin/ADS1256.o ./bin/bcm2835drv.o
	$(CC) -shared ./bin/LoadSensor.o ./bin/LoadSensor_wrap.o ./bin/bcm2835drv.o ./bin/ADS1256.o  -o ./bin/libLoadSensor.so  $(PYTHONLDLAGS) -Wl,--whole-archive  $(STEPGENLIB) -Wl,--no-whole-archive
	rm -f ./bin/LoadSensor.o 
	rm -f ./bin/LoadSensor_wrap.o
	rm -f ./bin/bcm2835drv.o
	rm -f ./bin/ADS1256.o

./bin/LoadSensor_wrap.o : ./LoadSensor/LoadSensor_wrap.cxx
	$(CC) $(CFLAGS) -O2 -c -fPIC  $<  -o $@  $(STEPGENLIB) $(PYTHONCFLAGS)

./bin/LoadSensor.o : ./LoadSensor/LoadSensor.cpp
	$(CC) $(CFLAGS) -c -fPIC $<  -o $@  $(STEPGENLIB)

./bin/ADS1256.o : ./LoadSensor/ADS1256.c
	$(CC) $(CFLAGS) -c -fPIC $<  -o $@  $(STEPGENLIB)

./bin/bcm2835drv.o : ./LoadSensor/bcm2835drv.c
	$(CC) $(CFLAGS) -c -fPIC $<  -o $@  $(STEPGENLIB)


	
clean :
	rm bin/*.* 