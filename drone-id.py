from gpiozero import Button

bit0 = Button(pin=22,pull_up=False)
bit1 = Button(pin=27,pull_up=False)
bit2 = Button(pin=17,pull_up=False)
sw = Button(pin=5,pull_up=False)

id2 = bit2.is_pressed ? 4 : 0
id1 = bit1.is_pressed ? 2 : 0
id0 = bit0.is_pressed ? 1 : 0
id = id2+id1+id0

print("Drone ID: ",id)

while True:
  if sw.is_pressed:
    print("Pressed")
