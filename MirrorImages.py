import cv2
import os
from pathlib import Path

def mirror_images_in_folder(folder_path):
    folder = Path(folder_path)
    mirrored_folder = folder / "MIRROR"
    mirrored_folder.mkdir(exist_ok=True)  # Create the MIRROR directory if it doesn't exist

    for img_path in folder.glob("*.jpg"):
        # Check if the image is already a mirrored version
        if img_path.stem.endswith("_mirrored"):
            continue

        img = cv2.imread(str(img_path))
        mirrored_img = cv2.flip(img, 1)  # Horizontal flip

        # Save the mirrored image
        mirrored_img_path = mirrored_folder / f"{img_path.stem}_mirrored{img_path.suffix}"
        cv2.imwrite(str(mirrored_img_path), mirrored_img)
        print(f"Mirrored image saved: {mirrored_img_path}")

# Set the directory containing your images
images_directory = "E:\\Projects\\PHOTOS\\JMCROPPER\\ALLx"
mirror_images_in_folder(images_directory)
