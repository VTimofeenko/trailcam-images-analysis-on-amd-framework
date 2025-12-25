"""Run a machine learning model against a set of images, draw bounding boxes, save results in a separate directory."""

import os
import sys

from ultralytics import YOLO

model = YOLO("model.pt")
output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

files = sys.argv[1:]

results = model.predict(
    source=files,
    imgsz=640,
    save=False,  # Saving to be done later
    conf=0.25,
    device="cuda",
    # NOTE: No 'stream=True' needed here since the batch is small
)

for r in results:
    detected_classes = [int(box.cls[0]) for box in r.boxes]

    has_animal = 0 in detected_classes
    has_person = 1 in detected_classes

    if has_animal and not has_person:
        filename = os.path.basename(r.path)
        save_path = os.path.join(output_dir, f"animal_{filename}")
        r.save(filename=save_path)
        print(f"Animal-only photo saved: {filename}")

    elif has_person:
        print(f"Person detected in {os.path.basename(r.path)}, skipping")
