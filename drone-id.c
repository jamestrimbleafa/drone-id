#include <stdio.h>
#include <stdlib.h>
#include <linux/gpio.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>


#define BIT2 17 // Physical pin 11 / GPIO17 (GPIO_GEN0)
#define BIT1 27 // Physical pin 13 / GPIO27 (GPIO_GEN2)
#define BIT0 22 // Physical pin 15 / GPIO22 (GPIO_GEN3)

#define DEV_NAME "/dev/gpiochip0"

int main(int argc, char* argv[]) {
	int id = -1;

	// Initialize GPIO
	
	int fd, ret;
	fd = open(DEV_NAME, O_RDONLY);
	if (fd < 0) {
		printf("Unable to open %s: %s\n", DEV_NAME, strerror(errno));
		return 0;
	}


	struct gpiohandle_request rq;
	struct gpiohandle_data data;

	rq.lineoffsets[0] = BIT0;
	rq.lineoffsets[1] = BIT1;
	rq.lineoffsets[2] = BIT2;
	rq.flags = GPIOHANDLE_REQUEST_INPUT;
	rq.lines = 3;
	ret = ioctl(fd, GPIO_GET_LINEHANDLE_IOCTL, &rq);

	close(fd);

	// Setup each GPIO pin as input with a pulldown resistor.  This way the pin will read zero/false when grounded or not connected, and one/true when connected to 3.3V
	
	if (ret == -1) {
		printf("Unable to get line handle from ioctl: %s",strerror(errno));
		return 0;
	}
	ret = ioctl(rq.fd, GPIOHANDLE_GET_LINE_VALUES_IOCTL, &data);
	if (ret == -1) {
		printf("Unable to get line handle from ioctl: %s", strerror(errno));
	} else {	
		//printf("17: %d, 27: %d, 22: %d\n",data.values[0], data.values[1], data.values[2]);
		
		id = 0;
		id += (4*data.values[2]);
		id += (2*data.values[1]);
		id += (1*data.values[0]);
	}
	close(rq.fd);

	// Output the done id if successful or -1 if there was an error
	if (argc > 1 && strcmp(argv[1],"--value")==0) {
		printf("%d",id);
	} else {
		printf("Drone ID: %d\n",id);
	}

	// Terminate
	return 0;
}

