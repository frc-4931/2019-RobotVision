import cv2
import math


hue = [53.417266187050366, 75.5631399317406]
sat = [208.67805755395685, 255.0]
val = [18.34532374100722, 255.0]


def get_center(side):
    return (side[0][0] + side[1][0]) / 2, (side[0][1] + side[1][1]) / 2


def get_center_x(side):
    return (side[0][0] + side[1][0]) / 2


def get_center_y(side):
    return (side[0][1] + side[1][1]) / 2


def dist(p1, p2):
    return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**(1/2)


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

    # cam.set(cv2.CAP_PROP_CONVERT_RGB, 0)
    cam.set(cv2.CAP_PROP_FPS, 30.0)


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
            M = cv2.moments(i)

            cx, cy = -1, -1
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])

            centers.append(((cx, cy), i))

        # Sort contours by distance to the center (remove all but the first two)
        centers.sort(key=lambda val: dist(val[0], middle))
        centers = centers[:2]

    else:
        if len(contours[0]) == 4:
            M = cv2.moments(contours[0])

            cx, cy = -1, -1
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])

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

    elif len(contour_sides) == 1:
        dst_left = dist(contour_sides[0][0][0], contour_sides[0][0][1])
        dst_right = dist(contour_sides[0][1][0], contour_sides[0][1][1])
        dst = (dst_left + dst_right) / 2

        # FIXME remove prints
        # print(dst)
        distance = 2 * 212 / dst
        # print(distance)

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
