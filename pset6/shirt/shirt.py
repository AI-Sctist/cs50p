import os.path
import sys

from PIL import Image, ImageOps

SUPPORTED_EXTENSIONS = [".png", ".jpg", ".jpeg"]
SHIRT_IMAGE_PATH = "images/shirt.png"


def supported_extensions(extensions: list[str]) -> bool:
    for extension in extensions:
        if extension.lower() not in SUPPORTED_EXTENSIONS:
            return False
    return True


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")

    input_image = sys.argv[1]
    output_image = sys.argv[2]

    input_ext = os.path.splitext(input_image)[1]
    output_ext = os.path.splitext(output_image)[1]

    if not supported_extensions([input_ext, output_ext]):
        sys.exit("Invalid input")
    if input_ext != output_ext:
        sys.exit("Input and output have different extensions")

    with Image.open(SHIRT_IMAGE_PATH) as shirt:
        try:
            with Image.open(input_image) as im:
                photo = ImageOps.fit(im, shirt.size)
                photo.paste(shirt, shirt)
                photo.save(output_image)
        except FileNotFoundError:
            sys.exit("Input does not exist")


if __name__ == "__main__":
    main()
