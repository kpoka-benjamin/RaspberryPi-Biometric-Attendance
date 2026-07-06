"""
fingerprint_module.py

Fingerprint recognition module.

Author: Benjamin KPOKA

"""

import pickle
import serial
import time

import adafruit_fingerprint

from config import (
    FINGERPRINT_SERIAL_PORT,
    FINGERPRINT_BAUDRATE,
    FINGERPRINT_TIMEOUT,
    FINGERPRINT_MAP_FILE,
)


class FingerprintRecognition:
    """
    Handles fingerprint sensor initialization
    and fingerprint authentication.
    """

    def __init__(self):

        self.sensor = None
        self.fingerprint_map = {}

        self._load_fingerprint_database()
        self._initialize_sensor()

    # =====================================================
    # Initialization
    # =====================================================

    def _initialize_sensor(self):
        """
        Initialize the fingerprint sensor.
        """

        try:

            uart = serial.Serial(
                FINGERPRINT_SERIAL_PORT,
                baudrate=FINGERPRINT_BAUDRATE,
                timeout=FINGERPRINT_TIMEOUT
            )

            self.sensor = adafruit_fingerprint.Adafruit_Fingerprint(
                uart
            )

            print("[INFO] Fingerprint sensor initialized.")

        except Exception as error:

            print(
                "[ERROR] Unable to initialize fingerprint sensor."
            )

            print(error)

            self.sensor = None

    def _load_fingerprint_database(self):
        """
        Load fingerprint ID to user mapping.
        """

        try:

            with open(FINGERPRINT_MAP_FILE, "rb") as file:

                self.fingerprint_map = pickle.load(file)

            print("[INFO] Fingerprint database loaded.")

        except Exception as error:

            print(
                "[WARNING] No fingerprint database found."
            )

            print(error)

            self.fingerprint_map = {}

    # =====================================================
    # Authentication
    # =====================================================

    def authenticate(self):
        """
        Authenticate a fingerprint.

        Returns
        -------
        str | None

            Person name if recognized,
            otherwise None.
        """

        if self.sensor is None:

            return None

        print("[INFO] Waiting for fingerprint...")

        attempts = 0

        while (
            self.sensor.get_image()
            != adafruit_fingerprint.OK
        ):

            time.sleep(0.1)

            attempts += 1

            if attempts >= 50:

                print(
                    "[INFO] Fingerprint timeout."
                )

                return None

        if (
            self.sensor.image_2_tz(1)
            != adafruit_fingerprint.OK
        ):

            print(
                "[ERROR] Unable to convert fingerprint."
            )

            return None

        if (
            self.sensor.finger_search()
            != adafruit_fingerprint.OK
        ):

            print(
                "[INFO] Unknown fingerprint."
            )

            return None

        finger_id = self.sensor.finger_id

        person = self.fingerprint_map.get(
            finger_id,
            f"ID_{finger_id}"
        )

        print(
            f"[INFO] Fingerprint recognized: {person}"
        )

        return person

    # =====================================================
    # Utility
    # =====================================================

    def is_available(self):
        """
        Check whether the sensor is available.
        """

        return self.sensor is not None