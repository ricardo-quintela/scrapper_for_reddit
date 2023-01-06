"""Module for analysing audio and extractiong timestamps
"""

import wave
from json import dumps, loads

from vosk import Model, KaldiRecognizer, SetLogLevel

from utils import write_log
from settings import LOG_PATH, MODEL_PATH


def import_audio_track(path: str) -> wave.Wave_read:
    """Imports the audio track to add to the video

    Args:
        path (str): the path to the audio track

    Returns:
        Wave_read: the wudio track
    """

    # try to open the file
    try:
        audio_track = wave.open(path, "rb")

    except IOError:
        write_log(f"Could not open file at {path}", LOG_PATH)
        return


    # audio is in a wrong format
    if audio_track.getnchannels() != 1:
        write_log(
            f"Could not process audio track at {path}: Audio file must be WAV format mono PCM",
            LOG_PATH
        )
        return

    if audio_track.getsampwidth() != 2:
        write_log(
            f"Could not process audio track at {path}: Audio file must be WAV format mono PCM",
            LOG_PATH
        )
        return

    if audio_track.getcomptype() != "NONE":
        write_log(
            f"Could not process audio track at {path}: Audio file must be WAV format mono PCM",
            LOG_PATH
        )
        return

    # success
    write_log(f"Audio track at {path} loaded successfully", LOG_PATH)
    return audio_track


def get_timestamps(audio_track: wave.Wave_read, script: list) -> list:
    """Returns the script line timestamps from the audio track

    Args:
        audio_track (Wave_read): the wav mono audio track
        script (list): the list of lines on the script

    Returns:
        list: the timestamps (timestamp, duration)
    """
    
    SetLogLevel(-1)

    try:
        model = Model(MODEL_PATH)
    except Exception:
        write_log(f"No model found in {MODEL_PATH}", LOG_PATH)
        return

    sentence_list_str = dumps(script)

    rec = KaldiRecognizer(model, audio_track.getframerate(), sentence_list_str)
    # enable word timestamp extraction
    rec.SetWords(True)
    rec.SetGrammar(sentence_list_str)

    results = list()

    while data := audio_track.readframes(4000):

        if rec.AcceptWaveform(data):
            results += loads(rec.Result())["result"]
            rec.SetGrammar(sentence_list_str)

    results += loads(rec.FinalResult())["result"]

    audio_track.close()

    timestamps = list()

    index = 0
    for sentence in script:
        start = results[index]["start"]

        index += len(sentence.split()) - 2
        
        duration = results[index]["end"] - start

        timestamps.append((start, duration))


    return timestamps
