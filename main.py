import time
from ImageManipulation import *

"""
Configuration
"""
# files have to be png, do not specify extension
defaultInputFile = 'message'
defaultOutputFile = 'output'

defaultDifficulty = 5
maxDifficulty = 25
# 0=easy

# Values taken from https://www.youtube.com/watch?v=zPa-ukzHilk and adapted for a 360 range
# Check hue value with http://colorizer.org/ in hsv mode
redTop = 78         # 55 / 255 => 78 / 360
blueLow = 106       # 75 / 255 => 106 / 360
blueTop = 268       # 190 / 255 => 268 / 360
purpleLow = 282     # 200 / 255 => 282 / 360

version = 1.0


if __name__ == "__main__":
    print("=" * 25)
    print(" Anaglyph generator V{:2.1f}".format(version))
    print("=" * 25)
    print("See documentation on go.epfl.ch/AnaglyphGenerator")

    # Get start time
    start_time = time.time()

    # Try to open file
    inputFile = getInput("Enter name of the message mask (.png)", defaultInputFile)
    im = openFile(inputFile)
    if im is None:
        exit(1)

    # Read user input
    outputFile = getInput("Enter name for the output file (.png)", defaultOutputFile)
    difficulty = getInput("Enter difficulty [0 easier-{} impossible]".format(maxDifficulty), defaultDifficulty, 'int')

    if difficulty is None:
        print("[Error] Please specify a number for the difficulty between 0 and {}".format(maxDifficulty))
        exit(1)

    # Force difficulty range
    if difficulty < 0 or difficulty > maxDifficulty:
        print("[Warning] Invalid value '{}' for difficulty, has to be a number between 0 and {}".
              format(difficulty, maxDifficulty))
        difficulty = maxDifficulty

    print("Converting '{}.png' to '{}.png' with difficulty {}/{}. Picture size is {}x{}px "
          .format(inputFile, outputFile, difficulty, maxDifficulty, im.size[0], im.size[1]))
    print("...")  # This line will be deleted by the progress bar

    # Convert image with hsv range
    im = convertImage(im, difficulty, [redTop, blueLow, blueTop, purpleLow], False)

    if im is None:
        print("[Error] Impossible to convert image")

    # Save image
    path = saveImage(im, outputFile)

    duration = time.time() - start_time

    print("Image converted in {} seconds".format(round(duration, 2)))
    print("Output saved as {}".format(path))

    input("Press enter to terminate")
