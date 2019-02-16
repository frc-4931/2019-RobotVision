#!/usr/bin/env bash
# Place a file with name "ssh" onto the root of SD card. File can be empty.
#
# SSH pi@raspberrypi.local -> Configure with raspi-config:
# hostname -> "vision"
# `shutdown -r now`
#
# SSH pi@vision.local -> Run this file on the pi:
# `sh install.sh`

sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libgtk2.0-dev libgtk-3-dev
sudo apt-get install libatlas-base-dev gfortran

sudo apt-get install python3
sudo apt-get install python3-pip
sudo python3 -m pip install --upgrade pip
sudo python3 -m pip install opencv-python-headless