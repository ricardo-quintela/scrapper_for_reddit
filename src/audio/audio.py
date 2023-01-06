"""Module for analysing audio and extractiong timestamps
"""

import wave
from json import dumps

from vosk import Model, KaldiRecognizer

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


def analyze_audio(audio_track: wave.Wave_read, script: str):

    model = Model(MODEL_PATH)

    sentence_list_str = dumps(script)

    rec = KaldiRecognizer(model, audio_track.getframerate(), sentence_list_str)
    rec.SetGrammar(sentence_list_str)
