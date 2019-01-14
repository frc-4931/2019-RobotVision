from networktables import NetworkTables
from time import sleep, ctime, time
import cv2
import numpy as np
from grip import GripPipeline

camera = cv2.VideoCapture(0)
camera.set(3,640)
camera.set(4,480)

connection_timeout = 120
NT_server = "roborio-4931-frc.local"

gp = GripPipeline()


def process_frame(frame):
    gp.process(frame)
    contour = gp.find_contours_output

    approx = []
    for i in contour:
        eps = 0.05 * cv2.arcLength(i, True)
        apx = cv2.approxPolyDP(i, eps, True)
        approx.append(apx)

    return approx


def connected():
    global smartDashboard
    smartDashboard = NetworkTables.getTable("SmartDashboard")
    smartDashboard.putString("Data from py", "Hello World! - From Raspi! Connected on {0:s}".format(ctime()))

    while True:
        ret, frame = camera.read()
        outline = process_frame(frame)

        # Calculate position to target

        # Send position to RoboRIO through SmartDashboard

        cv2.waitKey(1)


if __name__ == "__main__":
    NetworkTables.initialize(server=NT_server)
    connecting = True
    isConnected = False
    start_time = time()

    print("Connecting")
    while connecting:
        if NetworkTables.isConnected():
            connecting = False
            isConnected = True

        elif time() - start_time >= connection_timeout:
            connecting = False
            isConnected = False

    if isConnected:
        print("Connection to {:s} successful!".format(NT_server))
        connected()
    else:
        print("Failed to connect! Exiting...")