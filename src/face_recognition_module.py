"""
face_recognition_module.py

Safe stub for face recognition used by main.py.

This file intentionally does NOT include any biometric data. It loads a local
encodings.pickle if present (see scripts/generate_encodings.py) and otherwise
returns UNKNOWN_PERSON to avoid leaking sensitive data.
"""
from typing import Optional
import pickle
import os

import face_recognition

from config import FACE_ENCODINGS_FILE, FRAME_SCALE, UNKNOWN_PERSON

# In-memory cache for encodings
_encodings = None
_names = None


def _load_encodings():
    global _encodings, _names
    if _encodings is not None:
        return
    try:
        if not FACE_ENCODINGS_FILE.exists():
            print("[WARNING] Face encodings file not found:", FACE_ENCODINGS_FILE)
            _encodings = []
            _names = []
            return

        with open(FACE_ENCODINGS_FILE, "rb") as f:
            data = pickle.load(f)
            # Expected struct: {"encodings": [...], "names": [...]}
            _encodings = data.get("encodings", [])
            _names = data.get("names", [])
            print(f"[INFO] Loaded {_names and len(_names) or 0} face encodings.")
    except Exception as e:
        print("[WARNING] Failed to load face encodings:", e)
        _encodings = []
        _names = []


def identify_face(rgb_frame) -> Optional[str]:
    """
    Identify a face from an RGB image (numpy array).

    Returns:
      - a person's name (str) if matched
      - UNKNOWN_PERSON if encodings exist but the face did not match
      - None if no face was found in the frame

    Note: This stub avoids returning sensitive data when encodings are absent.
    """
    _load_encodings()

    if not _encodings:
        # No encodings available — do not expose biometric information
        return UNKNOWN_PERSON

    # Resize/speed-up processing consistent with main.py's scale factor
    try:
        small_frame = rgb_frame[::FRAME_SCALE, ::FRAME_SCALE]
    except Exception:
        # Fallback: if slicing fails, use the original frame
        small_frame = rgb_frame

    face_locations = face_recognition.face_locations(small_frame)
    if not face_locations:
        return None

    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    for encoding in face_encodings:
        matches = face_recognition.compare_faces(_encodings, encoding, tolerance=0.5)
        if True in matches:
            first_match_index = matches.index(True)
            return _names[first_match_index]

    return UNKNOWN_PERSON
