import numpy as np
from pathlib import Path
import cv2

home = Path(
    "~",
    "Info",
    "observatorio_fce_unpsjb",
    "india",
    "precios_claros",
    "Storage",
    "images",
).expanduser()


def r(name):
    return str(Path(home, name).with_suffix(".png"))


def write_text_on_image(text, font_size, font_color, background_color):
    """Writes a given text on an empty image with given font size, font color, and background color.

    Args:
      text: The text to be written on the image.
      font_size: The font size of the text.
      font_color: The font color of the text.
      background_color: The background color of the image.

    Returns:
      An image with the text written on it.
    """

    # Set the font.
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Calculate the text size.
    text_size = cv2.getTextSize(text, font, font_size, 1)[0]

    print("text_size:", str(text_size))

    image_side = max(text_size) + 20
    image_size = (image_side, image_side, 3)

    # Create an empty image.
    image = np.zeros(image_size, dtype=np.uint8)

    # Set the background color of the image.
    image[:] = background_color

    # Calculate the text origin.
    text_origin = (
        image.shape[1] // 2 - text_size[0] // 2 + 10,
        image.shape[0] // 2 - text_size[1] // 2,
    )

    print("  image_size:", str(image_size))
    print("  text_origin:", str(text_origin))

    # Write the text on the image.
    cv2.putText(image, text, text_origin, font, font_size, font_color, 6)

    return image


def compose_image(region_size, images):
    """Composes an image from six smaller images.

    Args:
      regions (rows, cols): how to compose the images
         rows * cols == len(images)
      region_size (height, width) the size of each region
      images: a list of numpy.ndarray
    Returns:
      numpy.ndarray: The composed image.
    """

    # Resize the smaller images to the same size.
    resized = [
        (cv2.resize(left, region_size), cv2.resize(right, region_size))
        for left, right in images
    ]

    rows = len(images)
    height, width = region_size
    width_times_2 = 2 * width
    # Create a new image to store the composed image.
    composed_image = np.zeros((height * rows, width_times_2, 3), dtype=np.uint8)

    # Add the smaller images to the composed image.
    for number, (left, right) in enumerate(resized):
        y1, y2 = height * number, height * (number + 1)
        composed_image[y1:y2, 0:width] = left
        composed_image[y1:y2, width:width_times_2] = right

    return composed_image


# Example usage:

size = (1024, 1024)
font_size = 10
font_color = (0, 0, 0)
background_color = (255, 255, 255)

names_and_messages = [
    ("milk_and_eggs", "Leche y huevos         "),
    ("bread", "Pan                    "),
    ("meat", "Carne                  "),
    ("oil_and_butter", "Aceite y margarina     "),
    ("fruits_and_vegetables", "Frutas y vegetales     "),
    ("coffee_and_sugar", "Café, azúcar y especies"),
    ("drinks", "Bebidas                "),
]

images = [
    (
        cv2.imread(r(a_name)),
        write_text_on_image(a_message, font_size, font_color, background_color),
    )
    for a_name, a_message in names_and_messages
]

composed_image = compose_image((1024, 1024), images)
cv2.imwrite(r("composed_image"), composed_image)


# Save the image.
# cv2.imwrite("image_with_title.jpg", image_with_title)
