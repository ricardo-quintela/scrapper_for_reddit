"""Generate a video
"""
from utils import import_data
from video import import_video, video_captions, generate_video
from audio import import_audio_clip, import_audio_track, get_timestamps,\
    create_audio_subclips, calculate_total_audio_time

def generate_video_file(video_path: str, audio_path: str, script_path: str, filename: str):
    """Generates a video from a background clip, an audio clip and a script file

    Args:
        video_path (str): the video file path
        audio_path (str): the audio file path
        script_path (str): the script file path
        filename (str): the name of the video to be generated
    """

    script = import_data(script_path)

    if script is None:
        return

    # import the video
    video_clip = import_video(video_path)
    if video_clip is None:
        return

    # extract the timestamps
    audio_track = import_audio_track(audio_path)
    if audio_track is None:
        video_clip.close()
        return

    timestamps = get_timestamps(audio_track, script)
    if timestamps is None:
        video_clip.close()
        audio_track.close()
        return

    # create the audio clips
    audio_clip = import_audio_clip(audio_path)
    if audio_clip is None:
        video_clip.close()
        audio_track.close()
        audio_clip.close()
        return

    # generate the audio subclips
    audio_subclips = create_audio_subclips(audio_clip, timestamps)

    # create the caption clips
    caption_clips = video_captions(script, timestamps)

    # calculate the supposed video duration
    video_duration = calculate_total_audio_time(timestamps)

    generate_video(video_clip, caption_clips, audio_subclips, video_duration, filename)

    audio_clip.close()
