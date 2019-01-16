import cv2
import numpy as np
import math
from time import time

window_name = "Test Window"

hue = [53.417266187050366, 75.5631399317406]
sat = [208.67805755395685, 255.0]
val = [18.34532374100722, 255.0]

camera = cv2.VideoCapture(1)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)


def camera_config(cam):
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)  # [0, 1] ~1/2 - 142
    cam.set(cv2.CAP_PROP_AUTO_WB, .25)
    cam.set(cv2.CAP_PROP_WB_TEMPERATURE, 3184)  # [?] ~1/8 - 3184
    cam.set(cv2.CAP_PROP_SATURATION, 0.60)  # [0, 1] ~2/3 - 128
    cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    cam.set(cv2.CAP_PROP_EXPOSURE, 0)  # [0, 1] ~1/4 - -9
    cam.set(cv2.CAP_PROP_CONTRAST, 0.5)  # [0, 1] ~2/3 - 7


def open_camera_config(cam):
    cv2.namedWindow(window_name)

    camera_config(cam)

    print("CAP_PROP_BRIGHTNESS: {}".format(cam.get(cv2.CAP_PROP_BRIGHTNESS)))
    print("CAP_PROP_AUTO_WB: {}".format(cam.get(cv2.CAP_PROP_AUTO_WB)))
    print("CAP_PROP_WB_TEMPERATURE: {}".format(cam.get(cv2.CAP_PROP_WB_TEMPERATURE)))
    print("CAP_PROP_SATURATION: {}".format(cam.get(cv2.CAP_PROP_SATURATION)))
    print("CAP_PROP_AUTO_EXPOSURE: {}".format(cam.get(cv2.CAP_PROP_AUTO_EXPOSURE)))
    print("CAP_PROP_EXPOSURE: {}".format(cam.get(cv2.CAP_PROP_EXPOSURE)))
    print("CAP_PROP_CONTRAST: {}".format(cam.get(cv2.CAP_PROP_CONTRAST)))

    def cSet(key, start=0.0, scale=0.01):
        def ret(val):
            val = val * scale + start
            cam.set(key, val)
            print(val)
        return ret

    cv2.createTrackbar("BRIGHTNESS", window_name, 50, 100, cSet(cv2.CAP_PROP_BRIGHTNESS))
    cv2.createTrackbar("AUTO_WB", window_name, 0, 1, cSet(cv2.CAP_PROP_AUTO_WB, 0, 1))
    cv2.createTrackbar("WB_TEMPERATURE", window_name, 0, 100, cSet(cv2.CAP_PROP_WB_TEMPERATURE, 2000, 20))
    cv2.createTrackbar("SATURATION", window_name, 60, 100, cSet(cv2.CAP_PROP_SATURATION))
    cv2.createTrackbar("AUTO_EXPOSURE", window_name, 0, 1, cSet(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25, 0.5))
    cv2.createTrackbar("EXPOSURE", window_name, 0, 100, cSet(cv2.CAP_PROP_EXPOSURE))
    cv2.createTrackbar("CONTRAST", window_name, 50, 100, cSet(cv2.CAP_PROP_CONTRAST))


def process_frame(frame):
    color = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    filtered = cv2.inRange(color, (hue[0], sat[0], val[0]), (hue[1], sat[1], val[1]))

    filtered, contours, hierarchy = cv2.findContours(filtered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    approx = []
    for i in contours:
        eps = 0.05 * cv2.arcLength(i, True)
        apx = cv2.approxPolyDP(i, eps, True)

        if cv2.contourArea(apx) < 200:  # TODO contour threshold
            continue

        if len(apx) != 4:
            continue

        approx.append(apx)

    return approx


def draw_contours(frame, contours):
    cv2.drawContours(frame, contours, -1, (255, 255, 0))
    return contours


def get_center(side):
    return (side[0][0] + side[1][0]) / 2, (side[0][1] + side[1][1]) / 2


def get_center_x(side):
    return (side[0][0] + side[1][0]) / 2


def get_center_y(side):
    return (side[0][1] + side[1][1]) / 2


def dist(p1, p2):
    return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**(1/2)


def offset_calculate(frame, contours) -> tuple:
    offset, distance = 0, 0

    # If no contours exist return all -1
    if len(contours) == 0:
        return -1, -1

    # Find the center (x, y) of the frame
    height, width, channels = frame.shape
    middle = [width / 2, height / 2]

    # Find the centers of all contours
    centers = []
    if len(contours) > 1:
        for i in contours:
            if len(i) != 4:
                continue

            M = cv2.moments(i)

            cx, cy = -1, -1
            try:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
            except ZeroDivisionError:
                pass

            centers.append(((cx, cy), i))

        # Sort contours by distance to the center (remove all but the first two)
        centers.sort(key=lambda val: dist(val[0], middle))
        centers = centers[:2]

        # Draw line connecting the two contours
        # TODO remove this when moving into main
        if len(centers) >= 2:
            cv2.line(frame, centers[0][0], centers[1][0], (255, 0, 0))

    else:
        if len(contours[0]) == 4:
            M = cv2.moments(contours[0])

            cx, cy = -1, -1
            try:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
            except ZeroDivisionError:
                pass

            centers.append(((cx, cy), contours[0]))

    # creates sides array and sorts them to the order (l/r, l/r, t/b, t/b)
    contour_sides = []
    for i in range(len(centers)):
        sides = list()

        # sets sides 0-3 and sorts them by longest side length
        sides.append([centers[i][1][0][0], centers[i][1][1][0]])
        sides.append([centers[i][1][1][0], centers[i][1][2][0]])
        sides.append([centers[i][1][2][0], centers[i][1][3][0]])
        sides.append([centers[i][1][3][0], centers[i][1][0][0]])
        sides.sort(key=lambda sd: dist(*sd), reverse=True)

        # Swaps 0-1 and/or 2-3 to make 0-1 = l-r and 2-3 = t-b
        if get_center_x(sides[0]) > get_center_x(sides[1]):
            tmp = sides[0]
            sides[0] = sides[1]
            sides[1] = tmp

        if get_center_y(sides[2]) > get_center_y(sides[3]):
            tmp = sides[2]
            sides[2] = sides[3]
            sides[3] = tmp

        contour_sides.append(sides)

    # Calculate skew to find angle
    # Not being used in current model

    # Calculate size / distance apart to find distance
    if len(centers) == 2:
        dst = dist(centers[0][0], centers[1][0])
        distance = 2 * 510 / dst

    # Calculate distance from center to find [x] offset
    feet_at_dst = distance * math.sqrt(3)
    pixels_to_feet = feet_at_dst / 1280

    center = None

    if len(centers) == 2:
        cx = centers[0][0][0], centers[1][0][0]
        cy = centers[0][0][1], centers[1][0][1]

        center = (cx[0] + cx[1]) / 2, (cy[0] + cy[1]) / 2

    # If one: get slope if slope > 0 target is on the left side, aka +.35 ft to get center
    elif len(contour_sides) == 1:
        left_side = contour_sides[0][0]
        slope = (left_side[0][1] - left_side[1][1]) / (left_side[0][0] - left_side[1][0])
        delta = 0.35 if slope > 0 else -0.35
        center = centers[0][0][0] + delta, centers[0][0][1]

    offset = (dist(center, middle) * pixels_to_feet) - (pixels_to_feet / 2)

    return distance, offset


def show_webcam():
    last_time = time()
    while True:
        ret_val, img = camera.read()

        cont = process_frame(img)
        draw_contours(img, cont)
        dist, offset = offset_calculate(img, cont)

        # print("Distance: {}, Offset: {}".format(dist, offset))

        cv2.imshow(window_name, img)

        cur_time = time()
        delta_time = cur_time - last_time
        last_time = cur_time

        print(1 / delta_time)

        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()


def setup_camera():
    open_camera_config(camera)
    show_webcam()


def test_on_frame():
    img = cv2.imread("images/my webcam_screenshot_13.01.2019.png")
    cont = process_frame(img)
    draw_contours(img, cont)
    offset_calculate(img, cont)
    cv2.imshow("Frame", img)
    while True:
        if cv2.waitKey(1) == 27:
            break


if __name__ == "__main__":
    open_camera_config(camera)
    show_webcam()
