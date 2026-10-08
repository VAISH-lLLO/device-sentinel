import cv2
from datetime import datetime
from pathlib import Path


def capture_photo():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("ERROR: Could not access the camera.")
        return None

    success, frame = camera.read()
    camera.release()

    if not success:
        print("ERROR: Could not capture camera frame.")
        return None

    # Create photos folder
    photos_folder = Path("photos")
    photos_folder.mkdir(exist_ok=True)

    # Create timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    photo_path = photos_folder / f"login_{timestamp}.jpg"

    cv2.imwrite(str(photo_path), frame)

    print(f"Photo captured: {photo_path}")

    return photo_path


if __name__ == "__main__":
    capture_photo()