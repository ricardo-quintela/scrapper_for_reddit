"""Testing the video generation
"""
from video import video_captions, import_video, generate_video
from audio import get_timestamps, import_audio_track, import_audio_clip, create_audio_subclips, calculate_total_audio_time

if __name__ == "__main__":
    with open("test_audio_script.txt", "r", encoding="utf-8") as file:
        script = file.readlines()

    # import the video
    VIDEO_CLIP = import_video("moonwalk brav.mp4")

    # extract the timestamps
    audio_track = import_audio_track("test_rec.wav")
    timestamps = get_timestamps(audio_track, script)

    # create the audio clips
    audio_clip = import_audio_clip("test_rec.wav")
    audio_subclips = create_audio_subclips(audio_clip, timestamps)

    # create the caption clips
    caption_clips = video_captions(script, timestamps)

    # calculate the supposed video duration
    video_duration = calculate_total_audio_time(timestamps)

    generate_video(VIDEO_CLIP, caption_clips, audio_subclips, video_duration, "test.mp4")

    audio_clip.close()
