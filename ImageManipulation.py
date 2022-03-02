from PIL import Image, ImageColor, UnidentifiedImageError
import random
from Terminal import *


def openFile(file_name):
    """
    Open an image file with PIL
    :param file_name: File name without .png extension
    :return: PIL Image() if succeed, None otherwise
    """
    try:
        file_name += ".png"
        im = Image.open(file_name)
        return im
    except FileNotFoundError:
        print("[Error] Unable to find '{}', check that file exists.".format(file_name))
    except UnidentifiedImageError:
        print("[Error] '{}' is not a valid message mask file. Please import a .png".format(file_name))
    except Exception as e:
        print("[Error] Unable to open file '{}'. Unhandled error: {}".format(file_name, e))
    return None


def loadImage(image):
    """
    Load pixels from image
    :param image: PIL Image() object
    :return: pixel array if succeed, None otherwise
    """
    try:
        pix = image.load()
        return pix
    except Exception as e:
        print("[Error] Unable to load image. Check that file is a valid .png picture.")
        print("Error: {}".format(e))
    return None


def saveImage(image, file_name):
    """
    Save image as file
    :param image: PIL image
    :param file_name: file name without .png extension
    """
    file_name += ".png"
    image.save(file_name)
    return file_name


def getPixelType(pixel):
    """
    Return pixel type
    :param pixel: Pixel color in (r, g, b, a)
    :return: 'b' for transparent background, 'a' for black pixel (text area),
    't' for white pixel (text pixel), '?' otherwise
    """
    r, g, b, a = pixel
    if a == 0:
        return 'b'  # Alpha is background
    if pixel == (0, 0, 0, 255):
        return 'a'  # Text area
    if pixel == (255, 255, 255, 255):
        return 't'  # Text pixels
    return '?'  # Other pixels, in general semi-alpha color


def getBlackPixelColor(blueLow, blueTop):
    """
    Return a color in the green-cyan range that will be seen
    as black with the red glasses
    Used to fill text pixels and background
    :return: hue, saturation
    """
    hue = random.randint(blueLow, blueTop)
    saturation = 100

    return hue, saturation


def getWhitePixelColor(redTop, purpleLow):
    """
    Return a color in the orange or red-purple range that will be seen
    as white with the red glasses
    Used to fill text area and background
    :return: hue, saturation
    """
    if random.randint(0, 1):
        hue = random.randint(0, redTop)
    else:
        hue = random.randint(purpleLow, 360)

    saturation = 0
    if random.randint(0, 8) > 1:
        saturation = 100

    return hue, saturation


def convertImage(im, difficulty, hue_range, progress_bar=False):
    # Try to extract pixels
    pix = loadImage(im)
    if pix is None:
        return None

    # Total number of pixels
    total_pixels = im.size[0] * im.size[1]
    progress_ctn = 0

    # For readability
    red_top = hue_range[0]
    blue_low = hue_range[1]
    blue_top = hue_range[2]
    purple_low = hue_range[3]

    # Iterate through each pixel
    for y in range(0, im.size[0]):
        for x in range(0, im.size[1]):
            # Get pixel type
            pixel_type = getPixelType(pix[x, y])

            """
            'b' => Background: Both group of color
            'a' => Message area: Light looking color behind the red glass
            't' => Message text: Dark looking color behind the red glass
            """

            brightness = 100

            pixel_difficulty = random.randint(0, 50)

            if pixel_type == 't':  # Text pixels
                if difficulty > pixel_difficulty:
                    hue, saturation = getWhitePixelColor(red_top, purple_low)  # false color to see text
                else:
                    hue, saturation = getBlackPixelColor(blue_low, blue_top)  # correct color to see text
            elif pixel_type == 'a':  # Text area
                if difficulty > pixel_difficulty:
                    hue, saturation = getBlackPixelColor(blue_low, blue_top)  # incorrect color to see text area
                else:
                    hue, saturation = getWhitePixelColor(red_top, purple_low)  # correct color to see text area
            else:  # pixel type 'b' and '?'    # Background and others (grey level)
                # Any color can be chosen for the background
                # Chose black pixel 1 of 3 times, white otherwise
                if random.randint(0, 2) == 0:
                    hue, saturation = getBlackPixelColor(blue_low, blue_top)
                else:
                    hue, saturation = getWhitePixelColor(red_top, purple_low)

            # Convert hsv to rgb
            color_hsv = "hsv({}, {}%, {}%)".format(hue, saturation, brightness)
            color_rgb = ImageColor.getrgb(color_hsv)

            # Replace pixel color
            pix[x, y] = color_rgb

            if progress_bar:
                progress_ctn += 1
                updateProgressBar("Converting image", progress_ctn, total_pixels)

    return im
