from networktables import NetworkTables
from time import sleep, ctime, time
import cv2
import vision_proccessing as vision


camera = cv2.VideoCapture(0)

connection_timeout = 120
NT_server = "roborio-4931-frc.local"

camera_settings = vision.CameraSettings()
vision_settings = vision.VisionSettings()

# Pi located at pi@vision.local -pass raspberry


def connected():
    global smartDashboard
    smartDashboard = NetworkTables.getTable("SmartDashboard")
    smartDashboard.putString("Data from PiPy", "Connected on {0:s}".format(ctime()))

    while True:
        # Get the current frame from camera
        ret, frame = camera.read()

        # Calculate outlines of objects
        contours = vision.process_frame(frame, vision_settings)

        # Calculate position to target
        distance, offset = vision.offset_calculate(frame, contours, vision_settings)

        # Send position to RoboRIO through SmartDashboard
        smartDashboard.putNumber("Vision Distance", distance)
        smartDashboard.putNumber("Vision Offset", offset)

        print(distance, offset)
        cv2.waitKey(1)


if __name__ == "__main__":
    NetworkTables.initialize(server=NT_server)
    connecting = True
    isConnected = False
    start_time = time()

    # Configure the camera
    vision.camera_config(camera, camera_settings)

    print("Vision: Connecting to {:s}".format(NT_server))
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
        print("Failed to connect to {:s}! Exiting...".format(NT_server))
