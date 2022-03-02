import os
import random
import time
from PIL import Image, ImageColor


"""
Configuration
"""
difficulty = 3
# 0=easy, 25=impossible

# Color
textPixelsColor = (0, 0, 0, 255)        # black
textAreaColor = (255, 255, 255, 255)    # white

# Check hue value with http://colorizer.org/ in hsv mode
redTop = 78         # 55 / 255 => 78 / 360
blueLow = 106       # 75 / 255 => 106 / 360
blueTop = 268       # 190 / 255 => 268 / 360
purpleLow = 282     # 200 / 255 => 282 / 360


def getBlackPixelColor():
    """
    Return a color in the green-cyan range that will be seen
    as black with the red glasses
    Used to fill text pixels and background
    :return: hue, saturation
    """
    hue = random.randint(blueLow, blueTop)
    saturation = 100

    return hue, saturation


def getWhitePixelColor():
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


def getPixelType(pixel):
    """
    Return pixel type
    :param pixel: Pixel color in (r, g, b, a)
    :return: 'b' for transparent background, 'a' for black pixel (text area),
    't' for white pixel (text pixel), '?' otherwise
    """
    r, g, b, a = pixel
    if a == 0:
        return 'b'          # Alpha is background
    if pixel == textPixelsColor:
        return 'a'          # Text area
    if pixel == textAreaColor:
        return 't'          # Text pixels
    return '?'  # Other pixels, in general semi-alpha color


# Get start time
start_time = time.time()

# Load message image
im = Image.open('message.png')
pix = im.load()

# Total number of pixels
totalPixels = im.size[0] * im.size[1]
progressCtn = 0

# Iterate through each pixel
for y in range(0, im.size[0]):
    for x in range(0, im.size[1]):
        # Get pixel type
        pixelType = getPixelType(pix[x, y])

        """
        'b' => Background: Both group of color
        'a' => Message area: Light looking color behind the red glass
        't' => Message text: Dark looking color behind the red glass
        """

        brightness = 100

        pixelDifficulty = random.randint(0, 50)

        if pixelType == 't':    # Text pixels

            if difficulty > pixelDifficulty:
                hue, saturation = getWhitePixelColor()  # false color to see text
            else:
                hue, saturation = getBlackPixelColor()   # correct color to see text
        elif pixelType == 'a':  # Text area
            pixelDifficulty = random.randint(0, 50)

            if difficulty > pixelDifficulty:
                hue, saturation = getBlackPixelColor()   # incorrect color to see text area
            else:
                hue, saturation = getWhitePixelColor()  # correct color to see text area
        else:   # pixel type 'b' and '?'    # Background and others (grey level)
            # Any color can be chosen for the background
            # Chose black pixel 1 of 3 times, white otherwise
            if random.randint(0, 2) == 0:
                hue, saturation = getBlackPixelColor()
            else:
                hue, saturation = getWhitePixelColor()

        # Convert hsv to rgb
        colorHsv = "hsv({}, {}%, {}%)".format(hue, saturation, brightness)
        colorRGB = ImageColor.getrgb(colorHsv)

        # Replace pixel color
        pix[x, y] = colorRGB

        progressCtn += 1
        print("Converting image - {}%".format(round(progressCtn / totalPixels * 100, 1)))

# Save new image as output.png
path = os.path.dirname(os.path.abspath(__file__))
path += "\output.png"
im.save(path)

duration = time.time() - start_time

print("Finished in {} seconds".format(round(duration, 2)))
print("File saved  in {}".format(path))

