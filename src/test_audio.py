from audio import import_audio_track, get_timestamps

if __name__ == "__main__":
    audio_track = import_audio_track("test_rec.wav")

    with open("test_audio_script.txt", "r", encoding="utf-8") as file:
        script = file.readlines()

    data = get_timestamps(audio_track, script)

    print(data)
