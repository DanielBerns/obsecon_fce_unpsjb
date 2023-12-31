from typing import Dict
from pathlib import Path
from components.core.file_processor import FileProcessor

from PIL import Image
import cv2
import pytesseract

# https://betterprogramming.pub/a-practical-guide-to-extract-text-from-images-ocr-in-python-d8c9c30ae74b

# https://nanonets.com/blog/ocr-with-tesseract/
# https://snyk.io/advisor/python/pytesseract/functions/pytesseract.image_to_data


# read cv2 image
def read_image(resource):
    return cv2.imread(str(resource))


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    angle = -(90 + angle) if angle < -45 else -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )
    return rotated


# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


class ImageFileProcessor(FileProcessor):
    def __init__(self):
        super().__init__()

    def result_to_content(self, result: Dict) -> None:
        pass


class ImageFileProcessorWithTesseractAndPIL(ImageFileProcessor):
    def __init__(self) -> None:
        super().__init__()
        self._image = None

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    def read(self) -> None:
        self.image = Image.open(str(self.origin_identifier))

    def process(self) -> None:
        result = pytesseract.pytesseract.image_to_data(
            self.image, output=pytesseract.Output.DICT
        )
        self.result_to_content(result)

    def write(self) -> None:
        pass


class ImageFileProcessorWithTesseractAndCV2(ImageFileProcessor):
    def __init__(self):
        super().__init__()
        self._image = None

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    def read(self) -> None:
        self.image = read_image(str(self.origin_identifier))

    def process(self) -> None:
        gray = get_grayscale(self.image)
        result = pytesseract.pytesseract.image_to_data(
            self.image, output=pytesseract.Output.DICT
        )
        self.result_to_content(result)

    def write(self) -> None:
        pass
