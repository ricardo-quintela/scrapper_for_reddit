"""Tools to edit the video automatically
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, ImageClip, AudioClip, CompositeVideoClip

from utils import write_log
from settings import LOG_PATH, VIDEO_FONT

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

def video_captions(clip: VideoFileClip, captions: list, timestamps: list):

    # make a list with the capiton clips
    caption_clips = list()

    font = ImageFont.load(VIDEO_FONT)

    for caption in captions:
        
