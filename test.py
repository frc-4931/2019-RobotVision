import cv2
import numpy as np
import math
from time import time
import vision_proccessing as vs

window_name = "Test Window"

camera = cv2.VideoCapture(1)

file_camera = "cameraSettings.json"
file_vision = "visionSettings.json"

json_camera = vs.read_from_file(file_camera)
json_vision = vs.read_from_file(file_vision)

cam_set = vs.CameraSettings(**json_camera)
vs_set = vs.VisionSettings(**json_vision)


def open_camera_config(cam):
    cv2.namedWindow(window_name)

    def cSet(key, start=0.0, scale=0.01):
        def ret(val):
            val = val * scale + start
            cam.set(key, val)
            print(val)
        return ret

    def vsSet(arr, el):
        def ret(val):
            arr[el] = val
        return ret

    start, scale = 0, 0.01
    cv2.createTrackbar("BRIGHTNESS", window_name, int(cam_set.brightness / scale), 100, cSet(cv2.CAP_PROP_BRIGHTNESS))

    start, scale = 0, 1
    cv2.createTrackbar("AUTO_WB", window_name, int((cam_set.auto_wb - start) / scale), 1, cSet(cv2.CAP_PROP_AUTO_WB, start, scale))

    start, scale = 2000, 20
    cv2.createTrackbar("WB_TEMPERATURE", window_name, int((cam_set.wb_temperature - start) / scale), 100, cSet(cv2.CAP_PROP_WB_TEMPERATURE, start, scale))

    start, scale = 0, 0.01
    cv2.createTrackbar("SATURATION", window_name, int((cam_set.saturation - start) / scale), 100, cSet(cv2.CAP_PROP_SATURATION))

    start, scale = 0.25, 0.5
    cv2.createTrackbar("AUTO_EXPOSURE", window_name, int(cam_set.auto_exposure), 1, cSet(cv2.CAP_PROP_AUTO_EXPOSURE, start, scale))

    start, scale = 0, 1
    cv2.createTrackbar("EXPOSURE", window_name, int((cam_set.exposure - start) / scale), 1, cSet(cv2.CAP_PROP_EXPOSURE))

    start, scale = 0, 0.01
    cv2.createTrackbar("CONTRAST", window_name, int((cam_set.contrast - start) / scale), 100, cSet(cv2.CAP_PROP_CONTRAST))

    cv2.createTrackbar("HUE OPEN", window_name, int(vs_set.hue[0]), 255, vsSet(vs_set.hue, 0))
    cv2.createTrackbar("HUE CLOSE", window_name, int(vs_set.hue[1]), 255, vsSet(vs_set.hue, 1))
    cv2.createTrackbar("SAT OPEN", window_name, int(vs_set.sat[0]), 255, vsSet(vs_set.sat, 0))
    cv2.createTrackbar("SAT CLOSE", window_name, int(vs_set.sat[1]), 255, vsSet(vs_set.sat, 1))
    cv2.createTrackbar("VAL OPEN", window_name, int(vs_set.val[0]), 255, vsSet(vs_set.val, 0))
    cv2.createTrackbar("VAL CLOSE", window_name, int(vs_set.val[1]), 255, vsSet(vs_set.val, 1))

    def reset_all_values(val, val1):
        global vs_set, cam_set
        vs_set = vs.VisionSettings()
        cam_set = vs.CameraSettings()

        start, scale = 0, 0.01
        cv2.setTrackbarPos("BRIGHTNESS", window_name, int(cam_set.brightness / scale))
        start, scale = 0, 1
        cv2.setTrackbarPos("AUTO_WB", window_name, int((cam_set.auto_wb - start) / scale))
        start, scale = 2000, 20
        cv2.setTrackbarPos("WB_TEMPERATURE", window_name, int((cam_set.wb_temperature - start) / scale))
        start, scale = 0, 0.01
        cv2.setTrackbarPos("SATURATION", window_name, int((cam_set.saturation - start) / scale))
        start, scale = 0.25, 0.5
        cv2.setTrackbarPos("AUTO_EXPOSURE", window_name, int((cam_set.auto_exposure - start) / scale))
        start, scale = 0, 1
        cv2.setTrackbarPos("EXPOSURE", window_name, int(cam_set.exposure))
        start, scale = 0, 0.01
        cv2.setTrackbarPos("CONTRAST", window_name, int((cam_set.contrast - start) / scale))

        cv2.setTrackbarPos("HUE OPEN", window_name, int(vs_set.hue[0]))
        cv2.setTrackbarPos("HUE CLOSE", window_name, int(vs_set.hue[1]))
        cv2.setTrackbarPos("SAT OPEN", window_name, int(vs_set.sat[0]))
        cv2.setTrackbarPos("SAT CLOSE", window_name, int(vs_set.sat[1]))
        cv2.setTrackbarPos("VAL OPEN", window_name, int(vs_set.val[0]))
        cv2.setTrackbarPos("VAL CLOSE", window_name, int(vs_set.val[1]))

        vs.camera_config(camera, cam_set)

        print("-- Reset --")

    def print_all_fields(val, val1):
        print("\n-------------------- EXPORT --------------------\n")
        print("CAP_PROP_FRAME_HEIGHT: {}".format(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        print("CAP_PROP_FRAME_WIDTH: {}".format(cam.get(cv2.CAP_PROP_FRAME_WIDTH)))
        print()
        print("CAP_PROP_BRIGHTNESS: {}".format(cam.get(cv2.CAP_PROP_BRIGHTNESS)))
        print("CAP_PROP_AUTO_WB: {}".format(cam.get(cv2.CAP_PROP_AUTO_WB)))
        print("CAP_PROP_WB_TEMPERATURE: {}".format(cam.get(cv2.CAP_PROP_WB_TEMPERATURE)))
        print("CAP_PROP_SATURATION: {}".format(cam.get(cv2.CAP_PROP_SATURATION)))
        print("CAP_PROP_AUTO_EXPOSURE: {}".format(cam.get(cv2.CAP_PROP_AUTO_EXPOSURE)))
        print("CAP_PROP_EXPOSURE: {}".format(cam.get(cv2.CAP_PROP_EXPOSURE)))
        print("CAP_PROP_CONTRAST: {}".format(cam.get(cv2.CAP_PROP_CONTRAST)))
        print("CAP_PROP_FPS: {}".format(cam.get(cv2.CAP_PROP_FPS)))
        print()
        print("HUE OPEN: {}".format(vs_set.hue[0]))
        print("HUE CLOSE: {}".format(vs_set.hue[1]))
        print("SAT OPEN: {}".format(vs_set.sat[0]))
        print("SAT CLOSE: {}".format(vs_set.sat[1]))
        print("VAL OPEN: {}".format(vs_set.val[0]))
        print("VAL CLOSE: {}".format(vs_set.val[1]))
        print("\n-------------------- END --------------------\n")

    def save_all_fields(val, val1):
        # cam_set.brightness = cam.get(cv2.CAP_PROP_BRIGHTNESS)
        # cam_set.auto_wb = cam.get(cv2.CAP_PROP_AUTO_WB)
        # cam_set.wb_temperature = cam.get(cv2.CAP_PROP_WB_TEMPERATURE)
        # cam_set.saturation = cam.get(cv2.CAP_PROP_SATURATION)
        # cam_set.auto_exposure = cam.get(cv2.CAP_PROP_AUTO_EXPOSURE)
        # cam_set.exposure = cam.get(cv2.CAP_PROP_EXPOSURE)
        # cam_set.contrast = cam.get(cv2.CAP_PROP_CONTRAST)
        # cam_set.fps = cam.get(cv2.CAP_PROP_FPS)

        start, scale = 0, 0.01
        cam_set.brightness = cv2.getTrackbarPos("BRIGHTNESS", window_name) * scale
        start, scale = 0, 1
        cam_set.auto_wb = (cv2.getTrackbarPos("AUTO_WB", window_name) * scale) + start
        start, scale = 2000, 20
        cam_set.wb_temperature = (cv2.getTrackbarPos("WB_TEMPERATURE", window_name) * scale) + start
        start, scale = 0, 0.01
        cam_set.saturation = (cv2.getTrackbarPos("SATURATION", window_name) * scale) + start
        start, scale = 0.25, 0.5
        cam_set.auto_exposure = (cv2.getTrackbarPos("AUTO_EXPOSURE", window_name) * scale) + start
        start, scale = 0, 1
        cam_set.exposure = (cv2.getTrackbarPos("EXPOSURE", window_name) * scale) + start
        start, scale = 0, 0.01
        cam_set.contrast = (cv2.getTrackbarPos("CONTRAST", window_name) * scale) + start

        vs.write_to_file(file_camera, cam_set.get_json())
        vs.write_to_file(file_vision, vs_set.get_json())

        print("-- Saved --")

    cv2.createButton("Export", print_all_fields)
    cv2.createButton("Save", save_all_fields)
    cv2.createButton("Reset", reset_all_values)

    vs.camera_config(camera, cam_set)


def draw_contours(frame, contours):
    cv2.drawContours(frame, contours, -1, (255, 255, 0))
    return contours


def show_webcam():
    last_time = time()
    while True:
        ret_val, img = camera.read()

        cont = vs.process_frame(img, vs_set)
        draw_contours(img, cont)
        dist, offset = vs.offset_calculate(img, cont, vs_set)

        # Add distance onto image
        if len(cont) == 2:
            M0 = cv2.moments(cont[0])
            M1 = cv2.moments(cont[1])

            if M0['m00'] != 0 and M1['m00'] != 0:
                line = [[0, 0], [0, 0]]

                line[0][0] = int(M0['m10'] / M0['m00'])
                line[0][1] = int(M0['m01'] / M0['m00'])

                line[1][0] = int(M1['m10'] / M1['m00'])
                line[1][1] = int(M1['m01'] / M1['m00'])

                center = vs.get_center(line)
                string = "{:.2f} feet away - {:.2f} feet {}".format(dist, abs(offset), "right" if offset < 0 else "left")
                string_size = cv2.getTextSize(string, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                text_location = int(center[0] - string_size[0] / 2), int(center[1] + string_size[1]/ 2)

                cv2.putText(img, string, text_location, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        cur_time = time()
        delta_time = cur_time - last_time
        last_time = cur_time

        cv2.putText(img, "{:.2f}".format(1 / delta_time), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Camera Only", img)

        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()


def proccess_nowindow():
    last_time = time()
    while True:
        ret_val, img = camera.read()

        cont = vs.process_frame(img, vs_set)
        dist, offset = vs.offset_calculate(img, cont, vs_set)

        # print("Distance: {}, Offset: {}".format(dist, offset))

        cur_time = time()
        delta_time = cur_time - last_time
        last_time = cur_time

        print(1 / delta_time)


def setup_camera():
    open_camera_config(camera)
    vs.camera_config(camera, cam_set)
    show_webcam()


def test_on_frame():
    img = cv2.imread("images/my webcam_screenshot_13.01.2019.png")
    cont = vs.process_frame(img, vs_set)
    draw_contours(img, cont)
    vs.offset_calculate(img, cont, vs_set)
    cv2.imshow("Frame", img)
    while True:
        if cv2.waitKey(1) == 27:
            break


if __name__ == "__main__":
    setup_camera()
