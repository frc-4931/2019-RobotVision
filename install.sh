#!/usr/bin/env bash

# Password is `raspberry`
#
# Place a file with name "ssh" onto the root of the pi's SD card.
# `touch /run/media/USER/DRIVE/ssh`
#
# SSH pi@raspberrypi.local -> Configure with raspi-config:
# Network Options -> hostname -> "vision" -> Reboot Yes
#
# From this point on you can follow these instructions or run the automated setup.sh script
#
# Run this file on the pi:
# `ssh pi@vision.local` -> `mkdir vision` -> `exit`
# `scp 2019-Vision/* pi@vision.local:vision`
# `ssh pi@vision.local` -> `sh install.sh`
#
# Add vision to pi's boot:
#  `sudo nano /etc/rc.local` -> Add line before `exit 0`: `sudo sh /home/pi/vision/run.sh &`

yes | sudo apt-get update
yes | sudo apt-get upgrade
sudo rpi-update

yes | sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
yes | sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
yes | sudo apt-get install libxvidcore-dev libx264-dev
yes | sudo apt-get install libgtk2.0-dev libgtk-3-dev
yes | sudo apt-get install libatlas-base-dev gfortran
yes | sudo apt-get install libilmbase-dev libopenexr-dev libgstreamer1.0-dev

yes | sudo apt-get install python3
yes | sudo apt-get install python3-pip

sudo python3 -m pip install --trusted-host www.piwheels.org opencv-python-headless
sudo python3 -m pip install pyfrc