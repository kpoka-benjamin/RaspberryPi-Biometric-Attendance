"""
main.py

Entry point of the RaspberryPi-Biometric-Attendance project.

Author: Benjamin KPOKA
License: MIT
"""

import threading
import time
import cv2
import RPi.GPIO as GPIO

from config import (
    init_gpio,
    IR_SENSOR_PIN,
)

from airtable_service import send_attendance
from lcd_controller import (
    display_message,
    clear_display,
)

from servo_controller import (
    rotate_servo,
    stop_servo,
)

from fingerprint_module import get_fingerprint
from face_recognition_module import identify_face

# Lock to prevent threads from writing to the LCD or driving the servo at the same time
hardware_lock = threading.Lock()

# ============================================================================
# Facial Recognition Thread
# ============================================================================

def facial_recognition_thread():
    """
    Continuously performs facial recognition when the IR sensor is triggered.
    """
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("[ERROR] Camera not detected.")
        return

    scale_factor = 2

    try:
        while True:
            if GPIO.input(IR_SENSOR_PIN) == GPIO.LOW:
                success, frame = camera.read()

                if not success:
                    time.sleep(0.1)
                    continue

                resized = cv2.resize(
                    frame,
                    (0, 0),
                    fx=1 / scale_factor,
                    fy=1 / scale_factor
                )

                rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
                person = identify_face(rgb)

                # Acquire lock before interacting with hardware/API to avoid thread conflicts
                if person and person != "Unknown":
                    with hardware_lock:
                        print(f"[INFO] Face recognized: {person}")
                        display_message(f"Welcome {person}")
                        rotate_servo()
                        send_attendance(person)
                        time.sleep(2)
                        display_message("Waiting...")

                elif person == "Unknown":
                    with hardware_lock:
                        print("[INFO] Unknown face detected.")
                        display_message("Unknown Face")
                        time.sleep(2)
                        display_message("Waiting...")

            time.sleep(0.3)
    finally:
        camera.release()
        print("[INFO] Camera released.")


# ============================================================================
# Fingerprint Recognition Thread
# ============================================================================

def fingerprint_recognition_thread():
    """
    Continuously performs fingerprint recognition when the IR sensor is triggered.
    """
    while True:
        if GPIO.input(IR_SENSOR_PIN) == GPIO.LOW:
            
            # Use lock only during the active checking and acting phase
            with hardware_lock:
                display_message("Place Finger")
                person = get_fingerprint()

                if person:
                    print(f"[INFO] Fingerprint recognized: {person}")
                    display_message("Access Granted")
                    rotate_servo()
                    send_attendance(person)
                else:
                    print("[INFO] Unknown fingerprint.")
                    display_message("Access Denied")

                time.sleep(3)
                display_message("Waiting...")

        time.sleep(0.3)


# ============================================================================
# Main Application
# ============================================================================

def main():
    """
    Start the biometric attendance system.
    """
    print("=" * 60)
    print(" Raspberry Pi Biometric Attendance System")
    print("=" * 60)

    init_gpio()
    display_message("Initializing...")
    print("[INFO] GPIO initialized.")

    facial_thread = threading.Thread(
        target=facial_recognition_thread,
        daemon=True
    )

    fingerprint_thread = threading.Thread(
        target=fingerprint_recognition_thread,
        daemon=True
    )

    facial_thread.start()
    fingerprint_thread.start()

    print("[INFO] Recognition services started.")
    display_message("Waiting...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Manual shutdown requested.")
    finally:
        stop_servo()
        GPIO.cleanup()
        clear_display()
        print("[INFO] GPIO cleaned.")
        print("[INFO] System stopped successfully.")


# ============================================================================
# Program Entry
# ============================================================================

if __name__ == "__main__":
    main()