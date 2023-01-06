from video import video_captions, import_video, generate_video

if __name__ == "__main__":
    captions = ["This guy is actually moonwalking", "Wtf am I watching?!", "Please Subscribe!"]
    timestamps = [(5, 4), (12, 4), (20, 5)]

    clip_captions = video_captions(captions, timestamps)

    video = import_video("moonwalk brav.mp4")

    generate_video(video, clip_captions, None, "test.mp4")
