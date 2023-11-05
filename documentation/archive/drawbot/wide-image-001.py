# This script is meant to be run from the root level
# of your font's git repository. For example, from a Unix terminal:
# $ git clone my-font
# $ cd my-font
# $ python3 documentation/drawbot/image1.py --output documentation/drawbot/image1.png

# Import moduels from external python packages: https://pypi.org/
#from drawbot_skia.drawbot import *
from drawBot import *
from fontTools.ttLib import TTFont
from fontTools.misc.fixedTools import floatToFixedToStr

# Import moduels from the Python Standard Library: https://docs.python.org/3/library/
import subprocess
import sys
import argparse

# Constants, these are the main "settings" for the image
WIDTH, HEIGHT, MARGIN, FRAMES = 2048*2, 1024*2, 128*2, 1
FONT_PATH = "fonts/variable/Blocksync[wdth,wght].ttf"
AUXILIARY_FONT_PATH = "documentation/drawbot/auxiliary-fonts/Hasubi-Mono[wght].ttf"
UNIT = MARGIN/4
GRID_VIEW = False


# Handel the "--output" flag
# For example: $ python3 documentation/image1.py --output documentation/image1.png
parser = argparse.ArgumentParser()
parser.add_argument("--output", metavar="PNG", help="where to write the PNG file")
args = parser.parse_args()

# Load the font with the parts of fonttools that are imported with the line:
# from fontTools.ttLib import TTFont
# Docs Link: https://fonttools.readthedocs.io/en/latest/ttLib/ttFont.html
ttFont = TTFont(FONT_PATH)

# Font Info Constants
MY_URL = subprocess.check_output("git remote get-url origin", shell=True).decode()
#MY_URL = "https://github.com/eliheuer/hasubi-mono "
MY_HASH = subprocess.check_output("git rev-parse --short HEAD", shell=True).decode()
FONT_NAME = ttFont["name"].getDebugName(4)
FONT_VERSION = "v%s" % floatToFixedToStr(ttFont["head"].fontRevision, 16)
FONT_LICENSE = "License: OFL v1.1"


# Draws a grid
def grid():
    stroke(1, 0, 0)
    strokeWidth(2)
    STEP_X, STEP_Y = 0, 0
    INCREMENT_X, INCREMENT_Y = MARGIN / 4, MARGIN / 4
    for x in range(57):
        polygon((MARGIN + STEP_X, MARGIN), (MARGIN + STEP_X, HEIGHT - MARGIN))
        STEP_X += INCREMENT_X
    for y in range(12*2):
        polygon((MARGIN, MARGIN + STEP_Y), (WIDTH - MARGIN, MARGIN + STEP_Y))
        STEP_Y += INCREMENT_Y
    strokeWidth(4)
    fill(None)
    rect(MARGIN, MARGIN, WIDTH - (MARGIN * 2), HEIGHT - (MARGIN * 2))
    polygon((WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
    polygon((0, HEIGHT / 2), (WIDTH, HEIGHT / 2))


# Remap input range to VF axis range
# This is useful for animation
# (E.g. sinewave(-1,1) to wght(100,900))
def remap(value, inputMin, inputMax, outputMin, outputMax):
    inputSpan = inputMax - inputMin  # FIND INPUT RANGE SPAN
    outputSpan = outputMax - outputMin  # FIND OUTPUT RANGE SPAN
    valueScaled = float(value - inputMin) / float(inputSpan)
    return outputMin + (valueScaled * outputSpan)


# Draw the page/frame and a grid if "GRID_VIEW" is set to "True"
def draw_background():
    newPage(WIDTH, HEIGHT)
    fill(0)
    rect(-2, -2, WIDTH + 2, HEIGHT + 2)
    if GRID_VIEW:
        grid()
    else:
        pass


# Draw main text
#GRID_VIEW = True
#SAMPLE_TEXT_1 = 'Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do. Once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, "and what is the use of a book," thought Alice, "without pictures or conversations?" '
def draw_main_text():
    fill(1)
    stroke(None)
    font(FONT_PATH)
    fontSize(UNIT*4)



    fontVariations(wdth=75)
    fontVariations(wght=400)
    text("ABCDEFGHIJKLMNOPQRSTUVWXYZ", (MARGIN+(UNIT*1), MARGIN+(UNIT*18.5)))
    fontVariations(wght=550)
    text("ABCDEFGHIJKLMNOPQRSTUVWXYZ", (MARGIN+(UNIT*1), MARGIN+(UNIT*15.5)))
    fontVariations(wght=700)
    text("ABCDEFGHIJKLMNOPQRSTUVWXYZ", (MARGIN+(UNIT*1), MARGIN+(UNIT*12.5)))


    fontVariations(wdth=125)
    fontVariations(wght=400)
    text("ABCDEFGHIJKLMNOPQRSTUVWXYZ", (MARGIN+(UNIT*1), MARGIN+(UNIT*8.5)))
    fontVariations(wght=550)
    text("ABCDEFGHIJKLMNOPQRSTUVWXYZ", (MARGIN+(UNIT*1), MARGIN+(UNIT*5.5)))
    fontVariations(wght=700)
    text("ABCDEFGHIJKLMNOPQRSTUVWXYZ", (MARGIN+(UNIT*1), MARGIN+(UNIT*2.5)))



# Divider lines
def draw_divider_lines():
    stroke(1)
    strokeWidth(4)
    lineCap("round")
    #line((MARGIN+64, HEIGHT - MARGIN*1.25), (WIDTH - MARGIN-64, HEIGHT - MARGIN*1.25))
    #line((MARGIN+64, MARGIN + (MARGIN / 4)), (WIDTH - MARGIN-64, MARGIN + (MARGIN / 4)))
    line((MARGIN+UNIT, HEIGHT-MARGIN-(UNIT*1)), (WIDTH-MARGIN-(UNIT*1), HEIGHT-MARGIN-(UNIT*1)))
    line((MARGIN+UNIT, MARGIN+UNIT), (WIDTH-MARGIN-UNIT, MARGIN+UNIT))

    stroke(None)


# Draw text describing the font and it's git status & repo URL
def draw_auxiliary_text():
    fontVariations(wght=400)
    # Setup
    font(AUXILIARY_FONT_PATH)
    fontSize(48)
    POS_TOP_LEFT = (MARGIN+UNIT, HEIGHT-MARGIN-(UNIT*0.6))
    POS_TOP_RIGHT = (WIDTH-MARGIN-UNIT, HEIGHT-MARGIN-(UNIT*0.6))
    POS_BOTTOM_LEFT = (MARGIN+UNIT, MARGIN)
    POS_BOTTOM_RIGHT = (WIDTH-MARGIN-UNIT, MARGIN)
    AT_HASH = "Git Commit: " + MY_HASH
    AT_HASH = AT_HASH.replace("\n", " ")
    # Draw Text
    text("GTL002: Blocksync", POS_TOP_LEFT, align="left")
    text("v0.1-Alpha", POS_TOP_RIGHT, align="right")
    text(MY_URL, POS_BOTTOM_LEFT, align="left")
    text(AT_HASH, POS_BOTTOM_RIGHT, align="right")

    font("documentation/drawbot/specimen-fonts/InputMonoCompressed-Regular.ttf")
    fontSize(48)
    #text("Hasubi Mono Regular v0.1-Alpha", (MARGIN+64, HEIGHT - ((MARGIN * 1.275/2))), align="left")
    #text(FONT_LICENSE, (WIDTH - 64 -MARGIN, HEIGHT - ((MARGIN * 1.275)/2)), align="right")
    #text(MY_URL, (MARGIN+64, MARGIN/2), align="left")
    #text(AT_HASH, (WIDTH - 64 - MARGIN * 0.8, MARGIN/2), align="right")


# Build and save the image
if __name__ == "__main__":
    draw_background()
    draw_main_text()
    draw_divider_lines()
    draw_auxiliary_text()
    # Save output, using the "--output" flag location
    saveImage(args.output)
    # Print done in the terminal
    print("DrawBot: Done")
