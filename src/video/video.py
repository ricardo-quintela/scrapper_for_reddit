"""Tools to edit the video automatically
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, ImageClip, AudioClip, CompositeVideoClip

from utils import write_log
from settings import LOG_PATH, VIDEO_FONT, FONT_SIZE, FONT_COLOR, STROKE_WIDTH, STROKE_COLOR

def import_video(path: str) -> VideoFileClip:
    """Opens a video file for editing and removes its audio\n
    The pointer must be closed after usage

    Args:
        path (str): the path to the file

    Returns:
        VideoFileClip: the imported video without audio
    """

    try:
        video = VideoFileClip(path)

    except IOError:
        write_log(f"Video file at {path} could not be found", LOG_PATH)
        return

    video = video.without_audio()

    return video


def make_caption_image(text: str, font: ImageFont.FreeTypeFont) -> np.ndarray:
    """Creates an image in array format with the given text
    written on it

    Args:
        text (str): the text to write on the image
        font (FreeTypeFont): the font to write the image

    Returns:
        ndarray: the generated image in array format
    """

    # calculate the width and height of the desired text
    width, height = font.getsize(text, stroke_width=STROKE_WIDTH)

    # calculate the total image size
    image_size = width, height

    # create a blank canvas to draw the text later
    image = Image.new("RGBA", image_size, color=(255,255,255,255))

    # create a draw interface on the created image
    draw_interface = ImageDraw.Draw(image)

    # draw the text on the image
    draw_interface.text(
        (STROKE_WIDTH, 0),
        text,
        font=font,
        fill=FONT_COLOR,
        stroke_width=STROKE_WIDTH,
        stroke_fill=STROKE_COLOR
    )

    return np.array(image)


def make_caption_clip(text: str, font: ImageFont.FreeTypeFont, timestamp: tuple) -> ImageClip:
    """Generates a clip with the given image

    Args:
        text (str): the text to write on the image
        font (FreeTypeFont): the font to write the image
        timestamp (list): the entry time ((minute, second), duration)

    Returns:
        ImageClip: the generated clip
    """
    clip = ImageClip(make_caption_image(text, font))

    clip = clip.set_start(timestamp[0])
    clip = clip.set_duration(timestamp[1])
    clip = clip.set_position(("center", "center"))

    return clip


def video_captions(captions: list, timestamps: list):
    """Generates the caption clips to put in the video

    Args:
        captions (list): the list of text captions to add to the video
        timestamps (list): the timestamp of each caption ((minute, second), duration)
    """

    # make a list with the capiton clips
    caption_clips = list()

    font = ImageFont.truetype(VIDEO_FONT, FONT_SIZE)

    for i, caption in enumerate(captions):
        text_clip = make_caption_clip(caption, font, timestamps[i])

        caption_clips.append(text_clip)

    return caption_clips


def generate_video(background_clip: VideoFileClip, caption_clips: list, audio_track: AudioClip, file_path: str):
    """Generates the final video

    Args:
        background_clip (VideoFileClip): the video that plays in the background
        caption_clips (list): the list of caption clips
        audio_track (AudioClip): the audio track that plays in the video
        file_path (str): the path where to save the file
    """

    video = CompositeVideoClip([background_clip] + caption_clips)

    # write the video file
    video.write_videofile(file_path)

    # release all of the used resources
    background_clip.close()
    for clip in caption_clips:
        clip.close()
    #audio_track.close()

    video.close()
