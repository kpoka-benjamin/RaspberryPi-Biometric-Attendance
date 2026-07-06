"""
airtable_service.py

Send attendance records to Airtable.

Author: Benjamin KPOKA

"""

import requests
from datetime import datetime

from config import (
    AIRTABLE_URL,
    HEADERS,
)


class AirtableService:
    """
    Airtable communication service.
    """

    @staticmethod
    def send_attendance(person_name):
        """
        Send attendance data to Airtable.
        """

        timestamp = datetime.now().isoformat()

        payload = {
            "fields": {
                "Name": person_name,
                "Time": timestamp
            }
        }

        try:

            response = requests.post(
                AIRTABLE_URL,
                headers=HEADERS,
                json=payload
            )

            if response.status_code in (200, 201):

                print(
                    f"[INFO] Attendance recorded: "
                    f"{person_name} ({timestamp})"
                )

            else:

                print(
                    f"[ERROR] Airtable returned "
                    f"{response.status_code}"
                )

                print(response.text)

        except Exception as error:

            print(
                f"[ERROR] Unable to connect to Airtable:"
            )

            print(error)