import cv2

cam = cv2.VideoCapture("rtsp://admin:admin123@172.22.61.80:554")
while True:
    _, frame = cam.read()

    cv2.imshow("frame", frame)
#     print(frame.shape)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    elif key == ord("c"):
        cv2.imwrite("capture.jpg", frame)

cam.release()
cv2.destroyAllWindows()