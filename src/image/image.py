"""Module for generating and working with images
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from settings import STROKE_WIDTH, STROKE_COLOR, FONT_COLOR

def make_caption_image(text: str, font: ImageFont.FreeTypeFont, caption_background: tuple=(0,0,0,0)) -> np.ndarray:
    """Creates an image in array format with the given text
    written on it

    Args:
        text (str): the text to write on the image
        font (FreeTypeFont): the font to write the image
        caption_background (tuple, optional): _description_. Defaults to (0,0,0,0).

    Returns:
        ndarray: the generated image in array format
    """

    # calculate the width and height of the desired text
    width, height = font.getsize(text.upper(), stroke_width=STROKE_WIDTH)

    # calculate the total image size
    image_size = width + STROKE_WIDTH * 2, height + STROKE_WIDTH * 2

    # create a blank canvas to draw the text later
    image = Image.new("RGBA", image_size, color=caption_background)

    # create a draw interface on the created image
    draw_interface = ImageDraw.Draw(image)

    # draw the text on the image
    draw_interface.text(
        (STROKE_WIDTH * 2, STROKE_WIDTH),
        text.upper(),
        font=font,
        fill=FONT_COLOR,
        stroke_width=STROKE_WIDTH,
        stroke_fill=STROKE_COLOR
    )

    return np.array(image)
