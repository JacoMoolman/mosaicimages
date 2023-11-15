
# Photo Mosaic Creator

## Overview

The Photo Mosaic Creator is a Python project that transforms an input image into a mosaic. It comprises two main scripts: `MakeMozzie.py` for creating the mosaic and `MirrorImages.py` for adding variety to the mosaic tiles.

## Getting Started

### Prerequisites

- Python 3.x
- OpenCV
- NumPy

### Installation

1. Clone the repository
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Configure the variables in `MakeMozzie.py`:
   - `H1`, `W1`: Set the height and width for each mosaic tile.
   - `KNUM`: Adjust local randomness in tile selection.
   - `MAX_USES_PER_IMAGE`: Limit how many times a single image can be used.
   - `alpha`: Transparency level for the final overlay.
   - `ImageName`: Name of the output file.
   - `MAINIMAGE`: Path to the main image for the mosaic.
2. Optionally, run `MirrorImages.py` to create mirrored versions of your tile images.
3. Run `MakeMozzie.py` to generate your photo mosaic.

   ```bash
   python MakeMozzie.py
   ```

4. The mosaic image will be saved as specified in `ImageName`.

## How It Works

1. **Image Caching:**
   - `MakeMozzie.py` calculates the average color of images in a specified directory and caches this data.
2. **Mosaic Generation:**
   - The script processes the main image, replacing sections with the best-matching images based on color.
3. **Optional Mirroring:**
   - `MirrorImages.py` can be used to expand the variety of images by mirroring them.

## Contributing

Feel free to contribute by creating issues or submitting pull requests for improvements.

## License

This project is licensed under the [MIT License](LICENSE).
