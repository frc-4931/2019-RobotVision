import cv2

camera = cv2.VideoCapture(0)
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
    window_name = "Test Window"

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
    hue = [53.417266187050366, 75.5631399317406]
    sat = [208.67805755395685, 255.0]
    val = [18.34532374100722, 255.0]

    color = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    filtered = cv2.inRange(color, (hue[0], sat[0], val[0]), (hue[1], sat[1], val[1]))

    filtered, contours, hierarchy = cv2.findContours(filtered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    approx = []
    for i in contours:
        eps = 0.05 * cv2.arcLength(i, True)
        apx = cv2.approxPolyDP(i, eps, True)
        approx.append(apx)

    return approx


def draw_contours(frame):
    contours = process_frame(frame)
    cv2.drawContours(frame, contours, -1, (255, 255, 0))
    return contours


def dist(p1, p2):
    return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**(1/2)


def offset_calculate(frame, contours) -> tuple:
    angle, offset, distance = 0, 0, 0

    # If no contours exist return all -1
    if len(contours) == 0:
        return -1, -1, -1

    # Find the center (x, y) of the frame
    height, width, channels = frame.shape
    middle = [width / 2, height / 2]

    # Find the centers of all contours
    centers = []
    if len(contours) > 1:
        for i in contours:
            M = cv2.moments(i)

            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            centers.append(((cx, cy), i))

        # Sort contours by distance to the center (remove all but the first two)
        centers.sort(key=lambda val: dist(val[0], middle))
        centers = centers[:2]

        # Draw line connecting the two contours
        # TODO remove this when moving into main
        cv2.line(frame, centers[0][0], centers[1][0], (255, 0, 0))

    else:
        M = cv2.moments(contours[0])

        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        centers.append(((cx, cy), contours[0]))

    # Calculate skew to find angle

    # Calculate size / distance apart to find distance

    # Calculate distance from center to find [x] offset

    return angle, offset, distance


def show_webcam():
    while True:
        ret_val, img = camera.read()
        # draw_contours(img)
        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()


def setup_camera():
    open_camera_config(camera)
    show_webcam()


def test_on_frame():
    img = cv2.imread("images/my webcam_screenshot_13.01.2019.png")
    cont = draw_contours(img)
    offset_calculate(img, cont)
    cv2.imshow("Frame", img)
    while True:
        if cv2.waitKey(1) == 27:
            break


if __name__ == "__main__":
    test_on_frame()
