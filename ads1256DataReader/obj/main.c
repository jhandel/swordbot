#include <stdlib.h>     //exit()
#include <signal.h>     //signal()
#include <time.h>
#include "ADS1256.h"
#include "stdio.h"
#include <time.h>
#include <string.h>
#include <sys/timeb.h>
void  Handler(int signo)
{
    //System Exit
    printf("\r\nEND                  \r\n");
    DEV_ModuleExit();

    exit(0);
}

double timespec_to_double(struct timespec ts)
{
	return ((double)(ts.tv_sec) + ((double)(ts.tv_nsec) / 1000000000));
}

int main(void)
{


    double readsPerSec, start_t, end_t, total_t, total, max, min;
    int count = 1000000;
    UDOUBLE ADC[count],i;
    int reads;
    reads = 0;
    total_t = 0;
    total = 0;
    max = 0;
    min = 200;
    printf("demo\r\n");
    DEV_ModuleInit();
    struct timespec now;
    // Exception handling:ctrl + c
    signal(SIGINT, Handler);

    if(ADS1256_init() == 1){
        printf("\r\nEND                  \r\n");
        DEV_ModuleExit();
        exit(0);
    }
    ADS1256_ConfigADC(ADS1256_GAIN_1,ADS1256_7500SPS);
    //ADS1256_WriteCmd(CMD_SELFCAL);
    //ADS1256_SetMode(0);

    clock_gettime(CLOCK_REALTIME, &now);
    start_t = timespec_to_double(now);
    FILE *fp;
    char name[50];
        
    snprintf(name, 50, "test%f.txt", start_t);
    fp = fopen(name, "w+");
        //fprintf(fp, "This is testing for fprintf...\n");
        //fputs("This is testing for fputs...\n", fp);
        

    printf("Start Reading \n");
    ADS1256_GetContinousSingle(ADC,1,count);
    clock_gettime(CLOCK_REALTIME, &now);
    end_t = timespec_to_double(now);
    printf("Stop Reading \n");
    reads = count;
    for(i = 0; i < count; i++){
        
        total = total + ADC[i]*5.0/0x7fffff;
        fprintf(fp, "%f\r\n", ADC[i]*5.0/0x7fffff  );
        if(max  < ADC[i]*5.0/0x7fffff){
            max = ADC[i]*5.0/0x7fffff;
        }
        if(min > ADC[i]*5.0/0x7fffff){
            min = ADC[i]*5.0/0x7fffff;
        }
    }
    total = total/count;

    
    total_t += (double)(end_t - start_t);
    readsPerSec = reads/total_t;
    
    printf("Average Voltage: %f v\n", total  );
    printf("Min Voltage: %f v\n", min  );
    printf("Max Voltage: %f v\n", max  );
    printf("Total time taken by CPU: %f\n", total_t  );
    printf("Reads: %i\n", reads  );
    printf("Reads Per Second: %f\n", readsPerSec  );
    fclose(fp);
    printf("Exiting of the program...\n");
    return 0;
}
