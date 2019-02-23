from networktables import NetworkTables
from time import sleep, ctime, time
import cv2
import vision_proccessing as vision
import argparse

connection_timeout = 120
NT_server = "roborio-4931-frc.local"

# Pi located at pi@vision.local -pass raspberry


def connected(vs_settings, cam: cv2.VideoCapture):
    global smartDashboard
    smartDashboard = NetworkTables.getTable("SmartDashboard")
    smartDashboard.putString("Data from PiPy", "Connected on {0:s}".format(ctime()))

    while True:
        # Get the current frame from camera
        ret, frame = cam.read()

        # Calculate outlines of objects
        contours = vision.process_frame(frame, vs_settings)

        # Calculate position to target
        distance, offset, sight = vision.offset_calculate(frame, contours, vs_settings)

        # Send position to RoboRIO through SmartDashboard
        smartDashboard.putNumber("Vision Distance", distance)
        smartDashboard.putNumber("Vision Offset", offset)
        smartDashboard.putBoolean("Vision Sight", sight)

        print(distance, offset, sight)
        cv2.waitKey(1)


def run_local(vs_settings, cam):
    while True:
        # Get the current frame from camera
        ret, frame = cam.read()

        # Calculate outlines of objects
        contours = vision.process_frame(frame, vs_settings)

        # Calculate position to target
        distance, offset, sight = vision.offset_calculate(frame, contours, vs_settings)

        print(distance, offset, sight)
        cv2.waitKey(1)


if __name__ == "__main__":
    file_camera = "/home/pi/vision/cameraSettings.json"
    file_vision = "/home/pi/vision/visionSettings.json"

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--relative", action="store_true", help="Sets paths to be relative to execution path."
                                                                      "\nUse this when running on a computer")
    parser.add_argument("-l", "--local", action="store_true", help="Sets the program to not try to connect to the "
                                                                   "RoboRIO.\nUseful for test on a local machine.")
    parser.add_argument("-c", "--camera", type=int, default=0, help="Sets the which camera to use.")
    args = parser.parse_args()

    if args.relative:
        file_camera = "cameraSettings.json"
        file_vision = "visionSettings.json"

    camera = cv2.VideoCapture(args.camera)

    json_camera = vision.read_from_file(file_camera)
    json_vision = vision.read_from_file(file_vision)

    camera_settings = vision.CameraSettings(**json_camera)
    vision_settings = vision.VisionSettings(**json_vision)

    NetworkTables.initialize(server=NT_server)
    connecting = True
    isConnected = False
    start_time = time()

    # Configure the camera
    vision.camera_config(camera, camera_settings)

    if args.local:
        run_local(vision_settings, camera)

    else:
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
            connected(vision_settings, camera)
        else:
            print("Failed to connect to {:s}! Exiting...".format(NT_server))
