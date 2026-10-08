import cv2

print("Starting camera test...")

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Could not access the camera.")
    exit()

print("Camera connected!")
print("Press SPACE to capture a photo.")
print("Press ESC to exit.")

while True:
    success, frame = camera.read()

    if not success:
        print("ERROR: Could not read camera frame.")
        break

    cv2.imshow("Device Sentinel - Camera Test", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == 32:
        cv2.imwrite("camera_test.jpg", frame)
        print("Photo captured: camera_test.jpg")
        break

    if key == 27:
        print("Camera test cancelled.")
        break

camera.release()
cv2.destroyAllWindows()