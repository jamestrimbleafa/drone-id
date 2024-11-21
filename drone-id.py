from gpiozero import Button

bit0 = Button(pin=22,pull_up=False)
bit1 = Button(pin=27,pull_up=False)
bit2 = Button(pin=17,pull_up=False)
sw = Button(pin=5,pull_up=False)

id = 0
id = id + 4 if bit2.is_pressed else id
id = id + 2 if bit1.is_pressed else id
id = id + 1 if bit0.is_pressed else id

print("Drone ID: ",id)

was_pressed = 0
while True:
  if sw.is_pressed:
    if (was_pressed == 0 and sw.is_pressed == 1):
      print("Pressed")
    was_pressed = 1
  else:
    was_pressed = 0
