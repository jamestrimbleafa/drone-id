drone-id:
	@echo "Compiling drone-id"
	gcc -o drone-id ./drone-id.c 

clean:
	@echo "Removing drone-id"
	rm -f ./drone-id
