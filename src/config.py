"""
config.py

Central configuration file for the RaspberryPi-Biometric-Attendance project.

Author: Benjamin KPOKA

"""

import os
from pathlib import Path

# ============================================================================
# Project Directories
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODELS_DIR = BASE_DIR / "models"
IMAGES_DIR = BASE_DIR / "images"

FACE_ENCODINGS_FILE = MODELS_DIR / "encodings.pickle"
FINGERPRINT_MAP_FILE = MODELS_DIR / "fingerprint_ids.pkl"

# ============================================================================
# Airtable Configuration
# ============================================================================

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "Attendance")

AIRTABLE_URL = (
    f"https://api.airtable.com/v0/"
    f"{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
)

HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json",
}

# ============================================================================
# Camera Configuration
# ============================================================================

CAMERA_INDEX = 0
FRAME_SCALE = 2

# ============================================================================
# Fingerprint Sensor Configuration
# ============================================================================

FINGERPRINT_SERIAL_PORT = "/dev/ttyS0"
FINGERPRINT_BAUDRATE = 57600
FINGERPRINT_TIMEOUT = 1

# ============================================================================
# Servo Configuration
# ============================================================================

SERVO_PIN = 17
SERVO_FREQUENCY = 50

SERVO_OPEN_ANGLE = 180
SERVO_CLOSED_ANGLE = 0

SERVO_OPEN_DELAY = 3.5
SERVO_CLOSE_DELAY = 3.5

# ============================================================================
# LCD Configuration
# ============================================================================

LCD_RS = 25
LCD_E = 24

LCD_D4 = 12
LCD_D5 = 13
LCD_D6 = 19
LCD_D7 = 26

LCD_BACKLIGHT = 21

LCD_COLUMNS = 16
LCD_ROWS = 2

# ============================================================================
# Infrared Sensor
# ============================================================================

IR_SENSOR_PIN = 27

# ============================================================================
# Timing Configuration
# ============================================================================

MAIN_LOOP_DELAY = 2
THREAD_DELAY = 0.3
LCD_MESSAGE_DELAY = 2

# ============================================================================
# Default Messages
# ============================================================================

MSG_INITIALIZING = "Initializing..."
MSG_WAITING = "Waiting..."
MSG_PLACE_FINGER = "Place Finger"
MSG_UNKNOWN_FACE = "Unknown Face"
MSG_ACCESS_GRANTED = "Access Granted"
MSG_ACCESS_DENIED = "Access Denied"

# ============================================================================
# Face Recognition
# ============================================================================

UNKNOWN_PERSON = "Unknown"

# ============================================================================
# Project Information
# ============================================================================

PROJECT_NAME = "RaspberryPi-Biometric-Attendance"
AUTHOR = "Benjamin KPOKA"
