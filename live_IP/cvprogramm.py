import cv2
cap = cv2.VideoCapture(r"5614724-hd_720_1280_30fps.mp4")
if not cap.isOpened():
    print("[ERROR] Could not open video source.")
    exit()
custom_width = 600
custom_height = 400
while True:
    ret, frame = cap.read()
    if not ret:
        print("[INFO] Can't receive frame (stream end?). Exiting ...")
        break
    resized_frame = cv2.resize(frame, (custom_width, custom_height), interpolation=cv2.INTER_AREA)
    cv2.imshow("Highway", resized_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()