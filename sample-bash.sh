#!/bin/bash
device=eth0
echo $PATH
echo "This is an example of using drone-id.  It will read the drone's ID from the GPIO pins then set the IP address to 192.168.1.100+ID.  SUDO rights are required to set the IP."
id=$(/usr/local/bin/drone-id --value)
echo "This is drone #$id"
ip=$((100+$id))
echo "Setting $device IP to 192.168.1.$ip"
sudo ifconfig $device 192.168.1.$ip
ifconfig $device

