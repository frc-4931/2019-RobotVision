from networktables import NetworkTables
from time import sleep, ctime, time
import cv2

camera = cv2.VideoCapture(0)
camera.set(3,640)
camera.set(4,480)

connection_timeout = 120
NT_server = "roborio-4931-frc.local"


def process_frame():
    ret, frame = camera.read()


    return frame


def connected():
    global smartDashboard
    smartDashboard = NetworkTables.getTable("SmartDashboard")
    smartDashboard.putString("Data from py", "Hello World! - From Raspi! Connected on {0:s}".format(ctime()))

    while True:
        frame = process_frame()

        outline = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cv2.waitKey(1)


def show_webcam():
    while True:
        ret_val, img = cam.read()
        cv2.imshow('my webcam', img)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()


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