"""
scripts/generate_encodings.py

Generate models/encodings.pickle from a directory of labeled images.

Usage:
  - Create images/known/<PersonName>/image1.jpg ...
  - Run: python scripts/generate_encodings.py

This script writes models/encodings.pickle (already ignored by .gitignore) and
must NOT be committed with biometric data.
"""
import os
import pickle
import face_recognition

KNOWN_DIR = "images/known"
OUT_FILE = "models/encodings.pickle"

os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)

encodings = []
names = []

if not os.path.isdir(KNOWN_DIR):
    print(f"Known images directory not found: {KNOWN_DIR}")
    print("Create images/known/<PersonName>/ and add photos before running this script.")
    raise SystemExit(1)

for person in sorted(os.listdir(KNOWN_DIR)):
    person_dir = os.path.join(KNOWN_DIR, person)
    if not os.path.isdir(person_dir):
        continue
    for fname in sorted(os.listdir(person_dir)):
        path = os.path.join(person_dir, fname)
        if not os.path.isfile(path):
            continue
        try:
            image = face_recognition.load_image_file(path)
            face_enc = face_recognition.face_encodings(image)
            if face_enc:
                encodings.append(face_enc[0])
                names.append(person)
                print(f"Encoded {path} -> {person}")
            else:
                print(f"No face found in {path}")
        except Exception as e:
            print("Failed to process", path, e)

with open(OUT_FILE, "wb") as f:
    pickle.dump({"encodings": encodings, "names": names}, f)

print("Saved encodings to", OUT_FILE)
print("Reminder: do NOT commit models/encodings.pickle to version control.")
