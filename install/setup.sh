#!/usr/bin/env bash

# Note: You need sshpass installed to run this script
#
# Note: This file needs to be run from the project root directory

# The following must be done before you can ssh into a brand new raspberry pi:
# Place a file with name "ssh" onto the root of the pi's SD card.
# `touch /run/media/USER/DRIVE/ssh`

# Change hostname to vision
sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@vision.local 'sudo raspi-config nonint do_change_hostname vision; sudo shutdown -r now'

echo "Sleeping while we wait for the pi to reboot..."
sleep 30

# Make directory for vision
sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@vision.local 'mkdir vision'

# SCP all the need files over to the raspberry pi
sshpass -p 'raspberry' scp -o StrictHostKeyChecking=no main.py pi@vision.local:vision/
sshpass -p 'raspberry' scp -o StrictHostKeyChecking=no vision_proccessing.py pi@vision.local:vision/
sshpass -p 'raspberry' scp -o StrictHostKeyChecking=no cameraSettigs.json pi@vision.local:vision/
sshpass -p 'raspberry' scp -o StrictHostKeyChecking=no visionSettings.json pi@vision.local:vision/
sshpass -p 'raspberry' scp -o StrictHostKeyChecking=no install.sh pi@vision.local:vision/
sshpass -p 'raspberry' scp -o StrictHostKeyChecking=no run.sh pi@vision.local:vision/

# Run the install script to install all the necessary libraries
sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@vision.local 'sudo sh vision/install.sh'

# SCP the pre-made rc.local script
sshpass -p 'raspberry' scp -o StrictHostKeyChecking=no install/rc.local pi@vision.local:/etc/rc.local

# Make new rc.local script executable
sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@vision.local 'sudo chmod +x /etc/rc.local'

# Restart the raspberry pi for the changes to take effect
sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no 'sudo shutdown -r now'