#include <gpiod.h>
#include <error.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

struct gpiod_chip *chip;
struct gpiod_line_request_config config;
struct gpiod_line_bulk lines;

int
main(int argc, char *argv[])
{
  unsigned int offsets[4] = {22, 27, 17, 5};

  int values[4] = {-1, -1, -1, -1};
  int err;

  chip = gpiod_chip_open("/dev/gpiochip0");
  if(!chip)
  {
    perror("gpiod_chip_open");
    goto cleanup;
  }

  err = gpiod_chip_get_lines(chip, offsets, 4, &lines);
  if(err)
  {
    perror("gpiod_chip_get_lines");
    goto cleanup;
  }

  memset(&config, 0, sizeof(config));
  config.consumer = "drone-id";
  config.request_type = GPIOD_LINE_REQUEST_DIRECTION_INPUT;
  config.flags = 0; // GPIOD_LINE_REQUEST_FLAG_BIAS_PULL_DOWN; or GPIOD_LINE_REQUEST_FLAG_ACTIVE_LOW; may be required

  err = gpiod_line_request_bulk(&lines, &config, values);
  if(err)
  {
    perror("gpiod_line_request_bulk");
    goto cleanup;
  }

  err = gpiod_line_get_value_bulk(&lines, values);
  if(err)
  {
    perror("gpiod_line_get_value_bulk");
    goto cleanup;
  }

  int id = values[2]*4 + values[1]*2 + values[0];
  int sw = values[3];

  if (argc > 1 && strcmp(argv[1],"--value")==0) {
		printf("%d",id);
	} else {
		printf("Drone ID: %d\n",id);
		printf("Switch: %d\n", sw);
  }  

cleanup:
  gpiod_line_release_bulk(&lines);
  gpiod_chip_close(chip);

  return EXIT_SUCCESS;
}
