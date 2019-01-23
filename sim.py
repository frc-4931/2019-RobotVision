from threading import Thread
import numpy as np
import cv2
import math
from time import sleep


ROTATION_SNAP_POINTS = 8
DEGREES_PER_POINT = 360 / ROTATION_SNAP_POINTS

ANGLE_CORRECTION = 0.5
OFFSET_CORRECTION = 0.2
DISTANCE_CORRECTION = 0.2


class Drive(Thread):
    def __init__(self, distance, offset, angle):
        super().__init__()

        self.__distance = distance
        self.__offset = offset
        self.__angle = angle

        self.__y_speed = 0
        self.__x_speed = 0
        self.__rot_speed = 0

        self.running = True

    def run(self):
        while self.running:
            self.__offset += (self.__y_speed / 100000)
            self.__distance -= (self.__x_speed / 100000)
            self.__angle -= (self.__rot_speed / 10000)

    def get_angle(self):
        return self.__angle

    def get_distance(self):
        return self.__distance

    def get_offset(self):
        return self.__offset

    def drive(self, y_speed, x_speed, rot_speed):
        self.__y_speed = min(max(y_speed, -1), 1)
        self.__x_speed = min(max(x_speed, -1), 1)
        self.__rot_speed = min(max(rot_speed, -1), 1)

    def stop_move(self):
        self.drive(0, 0, 0)

    def stop(self):
        self.running = False


def draw_angled_rec(x0, y0, width, height, angle, img):
    _angle = angle * math.pi / 180.0
    b = math.cos(_angle) * 0.5
    a = math.sin(_angle) * 0.5
    pt0 = (int(x0 - a * height - b * width),
           int(y0 + b * height - a * width))
    pt1 = (int(x0 + a * height - b * width),
           int(y0 - b * height - a * width))
    pt2 = (int(2 * x0 - pt0[0]), int(2 * y0 - pt0[1]))
    pt3 = (int(2 * x0 - pt1[0]), int(2 * y0 - pt1[1]))

    cv2.line(img, pt0, pt1, (255, 255, 255), 3)
    cv2.line(img, pt1, pt2, (255, 255, 255), 3)
    cv2.line(img, pt2, pt3, (255, 255, 255), 3)
    cv2.line(img, pt3, pt0, (255, 255, 255), 3)


def calculate(drive: Drive) -> bool:
    curDistance = drive.get_distance()
    curOffset = drive.get_offset()
    curAngle = drive.get_angle()

    targetAngle = round(curAngle / DEGREES_PER_POINT) * DEGREES_PER_POINT
    deltaTarget = targetAngle - curAngle

    trs = 0.4
    deltaTarget = trs * math.copysign(1, deltaTarget) if abs(deltaTarget) < trs else deltaTarget

    angleCorrection = -deltaTarget / (DEGREES_PER_POINT / 2) * ANGLE_CORRECTION
    offsetCorrection = pow(max(1 - abs(angleCorrection), 0), 2) * -curOffset * OFFSET_CORRECTION
    distanceCorrection = pow(max(1 - abs(offsetCorrection), 0), 2) * curDistance * DISTANCE_CORRECTION * 0.1

    if abs(deltaTarget) < 3 and abs(curOffset) < 0.15 and abs(curDistance) < 0.2:
        return True
    else:
        drive.drive(offsetCorrection, distanceCorrection, angleCorrection)
        return False


if __name__ == "__main__":
    drive = Drive(5, 2, 15)
    drive.start()
    width, height = 800, 800
    sizeX, sizeY = 50, 50
    pixels_per_foot = 25

    done = False
    while not done:
        img = np.zeros((width, height, 3), np.uint8)
        p1 = (int(width/2 - 100), 0)
        p2 = (int(width/2 + 100), 10)
        cv2.rectangle(img, p1, p2, (0, 255, 0))

        done = calculate(drive)

        x = int((width / 2) + (drive.get_offset() * pixels_per_foot))
        y = int((drive.get_distance() * pixels_per_foot) + (sizeY / 2))
        angle = drive.get_angle()
        if abs(angle) < 0.2: angle = 0

        draw_angled_rec(x, y, sizeX, sizeY, angle, img)
        cv2.imshow("Image", img)

        if cv2.waitKey(1) == 27:
            break

    drive.stop()

    sleep(5)

    cv2.destroyAllWindows()


if __name__ != "__main__":
    width, height = 800, 800
    sizeX, sizeY = 50, 50
    pixels_per_foot = 25

    img = np.zeros((width, height, 3), np.uint8)

    p1 = (int(width / 2 - 100), 0)
    p2 = (int(width / 2 + 100), 10)
    cv2.rectangle(img, p1, p2, (0, 255, 0))

    x = int((width / 2) + (2 * pixels_per_foot))
    y = int((6 * pixels_per_foot) + (sizeY / 2))
    angle = 20

    draw_angled_rec(x, y, sizeX, sizeY, angle, img)

    cv2.imshow("image", img)

    while True:
        if cv2.waitKey(1) == 27:
            break

