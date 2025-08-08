import cv2
img = cv2.imread(r"image.jpg")
if img is None:
    print("Image not found or failed to load.")
    exit()
scale_percent = 50
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
img = resized_img
cv2.rectangle(img, (50, 50), (350, 350), (0, 0, 255), 1)
cv2.putText(img, "mylogo", (60, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.imshow('logo', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
