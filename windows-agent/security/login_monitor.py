import time
import win32evtlog

from camera.camera_capture import capture_photo
from network.notifier import send_telegram_message, send_telegram_photo


SERVER = "localhost"
LOG_TYPE = "Security"

LOGIN_EVENTS = {
    4624: "Successful login",
    4625: "Failed login",
}


def get_latest_events():
    handle = win32evtlog.OpenEventLog(SERVER, LOG_TYPE)

    flags = (
        win32evtlog.EVENTLOG_BACKWARDS_READ
        | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    )

    events = win32evtlog.ReadEventLog(handle, flags, 0)

    win32evtlog.CloseEventLog(handle)

    return events


def monitor_login_events():
    print("Device Sentinel - Continuous Login Monitor")
    print("Monitoring Windows Security events...")
    print("Press Ctrl+C to stop.")

    last_event_time = None

    while True:
        try:
            events = get_latest_events()

            for event in events:
                event_id = event.EventID & 0xFFFF

                if event_id in LOGIN_EVENTS:
                    event_time = event.TimeGenerated

                    if last_event_time is None or event_time > last_event_time:
                        event_name = LOGIN_EVENTS[event_id]

                        print(
                            f"{event_name} | "
                            f"Event ID: {event_id} | "
                            f"Time: {event_time}"
                        )

                        # Capture a photo
                        photo_path = capture_photo()

                        # Create Telegram alert
                        message = (
                            f"🚨 Device Sentinel Alert\n\n"
                            f"Event: {event_name}\n"
                            f"Event ID: {event_id}\n"
                            f"Time: {event_time}"
                        )

                        # Send text alert
                        send_telegram_message(message)

                        # Send captured photo
                        if photo_path:
                            print(f"Login photo saved: {photo_path}")

                            send_telegram_photo(
                                photo_path,
                                caption=message
                            )

                        last_event_time = event_time

            time.sleep(3)

        except KeyboardInterrupt:
            print("\nDevice Sentinel stopped.")
            break

        except Exception as error:
            print(f"Monitoring error: {error}")
            time.sleep(5)


if __name__ == "__main__":
    monitor_login_events()