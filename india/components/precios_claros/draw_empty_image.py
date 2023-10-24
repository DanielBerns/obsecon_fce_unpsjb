import io
from PIL import Image

def generate_light_blue_jpg(width, height):
  """Generates a JPEG image with a light blue background.

  Args:
    width: The width of the image in pixels.
    height: The height of the image in pixels.

  Returns:
    A bytes object containing the JPEG image.
  """

  image = Image.new('RGB', (width, height), color=(173, 216, 230))

  # Save the image to a bytes object.
  bytes_io = io.BytesIO()
  image.save(bytes_io, format='JPEG')

  # Return the bytes object.
  return bytes_io.getvalue()

# Example usage:

image_bytes = generate_light_blue_jpg(800, 1450)

# Save the image to a file.
with open('light_blue_image.jpg', 'wb') as f:
  f.write(image_bytes)

 
