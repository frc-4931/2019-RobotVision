import cv2

window_name = "Test Window"

cv2.namedWindow(window_name)

camera = cv2.VideoCapture(1)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

camera.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)  # [0, 1] ~1/2 - 142
camera.set(cv2.CAP_PROP_AUTO_WB, .25)
camera.set(cv2.CAP_PROP_WB_TEMPERATURE, 3184)  # [?] ~1/8 - 3184
camera.set(cv2.CAP_PROP_SATURATION, 0.60)  # [0, 1] ~2/3 - 128
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
camera.set(cv2.CAP_PROP_EXPOSURE, 0)  # [0, 1] ~1/4 - -9
camera.set(cv2.CAP_PROP_CONTRAST, 0.5)  # [0, 1] ~2/3 - 7

print("CAP_PROP_BRIGHTNESS: {}".format(camera.get(cv2.CAP_PROP_BRIGHTNESS)))
print("CAP_PROP_AUTO_WB: {}".format(camera.get(cv2.CAP_PROP_AUTO_WB)))
print("CAP_PROP_WB_TEMPERATURE: {}".format(camera.get(cv2.CAP_PROP_WB_TEMPERATURE)))
print("CAP_PROP_SATURATION: {}".format(camera.get(cv2.CAP_PROP_SATURATION)))
print("CAP_PROP_AUTO_EXPOSURE: {}".format(camera.get(cv2.CAP_PROP_AUTO_EXPOSURE)))
print("CAP_PROP_EXPOSURE: {}".format(camera.get(cv2.CAP_PROP_EXPOSURE)))
print("CAP_PROP_CONTRAST: {}".format(camera.get(cv2.CAP_PROP_CONTRAST)))

def cSet(key, start=0.0, scale=0.01):
    def ret(val):
        val = val * scale + start
        camera.set(key, val)
        print(val)
    return ret

cv2.createTrackbar("CAP_PROP_BRIGHTNESS", window_name, 50, 100, cSet(cv2.CAP_PROP_BRIGHTNESS))
cv2.createTrackbar("CAP_PROP_AUTO_WB", window_name, 0, 1, cSet(cv2.CAP_PROP_AUTO_WB, 0, 1))
cv2.createTrackbar("CAP_PROP_WB_TEMPERATURE", window_name, 0, 100, cSet(cv2.CAP_PROP_WB_TEMPERATURE, 2000, 20))
cv2.createTrackbar("CAP_PROP_SATURATION", window_name, 60, 100, cSet(cv2.CAP_PROP_SATURATION))
cv2.createTrackbar("CAP_PROP_AUTO_EXPOSURE", window_name, 0, 1, cSet(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25, 0.5))
cv2.createTrackbar("CAP_PROP_EXPOSURE", window_name, 0, 100, cSet(cv2.CAP_PROP_EXPOSURE))
cv2.createTrackbar("CAP_PROP_CONTRAST", window_name, 50, 100, cSet(cv2.CAP_PROP_CONTRAST))


def show_webcam():
    while True:
        ret_val, img = camera.read()
        cv2.imshow('my webcam', img)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()


if __name__ == "__main__":
    show_webcam()