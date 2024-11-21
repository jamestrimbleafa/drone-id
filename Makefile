drone-id:
	@echo "Compiling drone-id"
	gcc drone-id.c -lgpiod -o drone-id

clean:
	@echo "Removing drone-id"
	rm -f ./drone-id

configure:
	@echo "Installing gpiod and C libraries"
	sudo apt install gpiod libgpiod-dev
	@echo "Installing python gpio zero package"
	pip install gpiozero
