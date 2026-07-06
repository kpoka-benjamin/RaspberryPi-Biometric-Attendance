"""
lcd_controller.py

Controls the 16x2 LCD display.

Author: Benjamin KPOKA
"""

import time

from config import LCD_MESSAGE_DELAY


class LCDController:
    """
    LCD display controller.
    """

    def __init__(self, lcd):
        self.lcd = lcd

    def clear(self):
        """Clear the LCD."""
        self.lcd.clear()

    def display(self, message):
        """
        Display a message.
        """
        self.lcd.clear()
        self.lcd.write_string(message)

    def display_temporary(self, message, duration=LCD_MESSAGE_DELAY):
        """
        Display a message temporarily.
        """
        self.display(message)
        time.sleep(duration)
        self.clear()

    def waiting(self):
        self.display("Waiting...")

    def initializing(self):
        self.display("Initializing...")

    def place_finger(self):
        self.display("Place Finger")

    def access_granted(self):
        self.display("Access Granted")

    def access_denied(self):
        self.display("Access Denied")

    def unknown_face(self):
        self.display("Unknown Face")