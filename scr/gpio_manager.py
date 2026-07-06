"""
gpio_manager.py

Handles the initialization and cleanup of all GPIO peripherals.

Author: Benjamin KPOKA

"""

import threading

import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD

from config import (
    LCD_RS,
    LCD_E,
    LCD_D4,
    LCD_D5,
    LCD_D6,
    LCD_D7,
    LCD_BACKLIGHT,
    LCD_COLUMNS,
    LCD_ROWS,
    IR_SENSOR_PIN,
    SERVO_PIN,
    SERVO_FREQUENCY,
)


class GPIOManager:
    """
    Initialize and manage all Raspberry Pi GPIO peripherals.
    """

    def __init__(self):

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # -----------------------------
        # LCD Backlight
        # -----------------------------
        GPIO.setup(LCD_BACKLIGHT, GPIO.OUT)

        # -----------------------------
        # IR Sensor
        # -----------------------------
        GPIO.setup(IR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # -----------------------------
        # Servo
        # -----------------------------
        GPIO.setup(SERVO_PIN, GPIO.OUT)

        self.servo_pwm = GPIO.PWM(
            SERVO_PIN,
            SERVO_FREQUENCY
        )

        self.servo_pwm.start(0)

        self.servo_lock = threading.Lock()

        # -----------------------------
        # LCD Display
        # -----------------------------
        self.lcd = CharLCD(
            pin_rs=LCD_RS,
            pin_e=LCD_E,
            pins_data=[
                LCD_D4,
                LCD_D5,
                LCD_D6,
                LCD_D7,
            ],
            numbering_mode=GPIO.BCM,
            cols=LCD_COLUMNS,
            rows=LCD_ROWS,
            pin_backlight=LCD_BACKLIGHT,
            auto_linebreaks=True,
        )

    # ====================================================
    # LCD
    # ====================================================

    def clear_lcd(self):
        """Clear LCD display."""
        self.lcd.clear()

    def display_message(self, message):
        """
        Display a message on the LCD.
        """

        self.lcd.clear()
        self.lcd.write_string(message)

    # ====================================================
    # IR SENSOR
    # ====================================================

    def person_detected(self):
        """
        Return True if the IR sensor detects a person.
        """

        return GPIO.input(IR_SENSOR_PIN) == GPIO.LOW

    # ====================================================
    # SERVO
    # ====================================================

    def get_pwm(self):
        """
        Return the PWM object.
        """

        return self.servo_pwm

    def get_servo_lock(self):
        """
        Return the servo lock.
        """

        return self.servo_lock

    # ====================================================
    # CLEANUP
    # ====================================================

    def cleanup(self):
        """
        Release all GPIO resources.
        """

        self.servo_pwm.stop()
        GPIO.cleanup()