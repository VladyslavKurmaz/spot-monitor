# import cv2
#
# cam = cv2.VideoCapture(0)
#
# while True:
#    _, frame = cam.read()
#
#    cv2.imshow("frame", frame)
#    print(frame.shape)
#    key = cv2.waitKey(1)
#    if key == ord("q"):
#        break
#    elif key == ord("c"):
#        cv2.imwrite("capture.jpg", frame)
#
# cam.release()
# cv2.destroyAllWindows()
from hikvision import *

def load_config(name):
    f = open(name, 'r')
    lines = f.readlines()
    f.close()
    return ''.join(lines)


hik = Hikvision()
hik.put_config(load_config('config.yaml'))