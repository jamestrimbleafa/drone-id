import argparse
from gpiozero import Button

# Initialize buttons
bit0 = Button(pin=22, pull_up=False)
bit1 = Button(pin=27, pull_up=False)
bit2 = Button(pin=17, pull_up=False)
sw0 = Button(pin=5, pull_up=False)

# Calculate drone ID
id = 0
id = id + 4 if bit2.is_pressed else id
id = id + 2 if bit1.is_pressed else id
id = id + 1 if bit0.is_pressed else id

# Read switch state
sw = 1 if sw0.is_pressed else 0

# Set up argument parser
parser = argparse.ArgumentParser(description='Drone ID and Switch Status')
parser.add_argument('--value', action='store_true', help='Only print the Drone ID')

# Parse command-line arguments
args = parser.parse_args()

# Print output based on the presence of the --value flag
if args.value:
    print(id)  # Only print the ID when --value is specified
else:
    print("Drone ID: ", id)
    print("Switch: ", sw)