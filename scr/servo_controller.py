"""
servo_controller.py

Servo motor controller.

Author: Benjamin KPOKA

"""

import time

from config import (
    SERVO_OPEN_ANGLE,
    SERVO_CLOSED_ANGLE,
    SERVO_OPEN_DELAY,
    SERVO_CLOSE_DELAY,
)


class ServoController:
    """
    Controls the servo motor.
    """

    def __init__(self, pwm, lock):
        self.pwm = pwm
        self.lock = lock

    @staticmethod
    def angle_to_duty(angle):
        """
        Convert servo angle into PWM duty cycle.
        """
        return 2.5 + (angle / 180.0) * 10

    def open_door(self):
        """
        Open then close the door.
        """

        with self.lock:

            self.pwm.ChangeDutyCycle(
                self.angle_to_duty(SERVO_OPEN_ANGLE)
            )

            time.sleep(SERVO_OPEN_DELAY)

            self.pwm.ChangeDutyCycle(
                self.angle_to_duty(SERVO_CLOSED_ANGLE)
            )

            time.sleep(SERVO_CLOSE_DELAY)

            self.pwm.ChangeDutyCycle(0)