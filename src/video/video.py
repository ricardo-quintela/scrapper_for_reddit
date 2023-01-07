"""Tools to edit the video automatically
"""

import re
from PIL import ImageFont
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip
from moviepy.video.fx.fadeout import fadeout

from utils import write_log, VideoProgressBar
from image import make_caption_image
from settings import LOG_PATH, VIDEO_FONT, FONT_SIZE, FADE_TO_BLACK_TIME, TITLE_BACKGROUND, TITLE_DURATION, CROSS_FADE_IN_OUT

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


def make_caption_clip(text: str, font: ImageFont.FreeTypeFont, timestamp: tuple) -> ImageClip:
    """Generates a clip with the given image

    Args:
        text (str): the text to write on the image
        font (FreeTypeFont): the font to write the image
        timestamp (list): the entry time (timestamp, duration)

    Returns:
        ImageClip: the generated clip
    """

    # if the caption is a title
    if re.search(r"Story [0-9]+", text):
        clip = ImageClip(make_caption_image(text, font, caption_background=TITLE_BACKGROUND))

        clip = clip.set_start(timestamp[0])
        clip = clip.set_duration(timestamp[1] + TITLE_DURATION)
        clip = clip.set_position(("center", 0.3), relative=True)
        clip = clip.crossfadein(CROSS_FADE_IN_OUT).crossfadeout(CROSS_FADE_IN_OUT)
        return clip

    clip = ImageClip(make_caption_image(text, font))

    clip = clip.set_start(timestamp[0])
    clip = clip.set_duration(timestamp[1])
    clip = clip.set_position(("center", "center"))

    return clip


def video_captions(captions: list, timestamps: list):
    """Generates the caption clips to put in the video

    Args:
        captions (list): the list of text captions to add to the video
        timestamps (list): the timestamp of each caption (timestamp, duration)
    """

    # make a list with the capiton clips
    caption_clips = list()

    font = ImageFont.truetype(VIDEO_FONT, FONT_SIZE)

    for i, caption in enumerate(captions):
        write_log(f"Generating captions: {i+1}/{len(captions)}", LOG_PATH)
        text_clip = make_caption_clip(caption, font, timestamps[i])

        caption_clips.append(text_clip)

    write_log("Captions generated Successfully", LOG_PATH)
    return caption_clips


def generate_video(background_clip: VideoFileClip, caption_clips: list, audio_clips: list, video_duration: float, file_path: str):
    """Generates the final video

    Args:
        background_clip (VideoFileClip): the video that plays in the background
        caption_clips (list): the list of caption clips
        audio_clips (list): the list of audio clips
        video_duration (float): the video duration in seconds
        file_path (str): the path where to save the file
    """

    audio = CompositeAudioClip(audio_clips)

    video = CompositeVideoClip([background_clip] + caption_clips)

    # set the video's audio
    video = video.set_audio(audio)

    # crop the video according to the given duration
    video = video.set_end(video_duration)

    # fade to black
    video = fadeout(video, FADE_TO_BLACK_TIME, (0,0,0))

    write_log("Rendering video...", LOG_PATH)

    # write the video file
    video.write_videofile(file_path, logger=VideoProgressBar())

    # release all of the used resources
    background_clip.close()
    for clip in caption_clips:
        clip.close()
    for clip in audio_clips:
        clip.close()

    audio.close()
    video.close()

    write_log(f"Video generated successfully at {file_path}", LOG_PATH)
