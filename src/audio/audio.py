"""Module for analysing audio and extractiong timestamps
"""

import wave
from json import dumps, loads

from vosk import Model, KaldiRecognizer, SetLogLevel

from utils import write_log
from settings import LOG_PATH, MODEL_PATH, FADE_TO_BLACK_TIME
from moviepy.editor import AudioFileClip


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

    write_log("Generating timestamps for the audio track", LOG_PATH)

    # don't show log messages of the vosk library
    SetLogLevel(-3)

    try:
        model = Model(MODEL_PATH)
    except Exception:
        write_log(f"No model found in {MODEL_PATH}", LOG_PATH)
        return

    # create a string of the sentences that can be used in the audio
    sentence_list_str = dumps(script)

    # create the speech recognizer instance
    rec = KaldiRecognizer(model, audio_track.getframerate(), sentence_list_str)
    # enable word timestamp extraction
    rec.SetWords(True)
    rec.SetGrammar(sentence_list_str)

    results = list()

    # loop through all the audio
    while data := audio_track.readframes(4000):

        # if a sentence has been successfully parsed -> add to results
        if rec.AcceptWaveform(data):
            results += loads(rec.Result())["result"]
            rec.SetGrammar(sentence_list_str)

    # add the final sentence
    results += loads(rec.FinalResult())["result"]

    # close the audio file
    audio_track.close()

    # create a list of timestamps
    timestamps = list()

     # add timestamps for all the lines
    index = 0
    for sentence in script:

        # start of the line
        start = results[index]["start"]

        index += len(sentence.split()) - 2

        # duration of the line
        duration = results[index]["end"] - start

        timestamps.append((start, duration))

    write_log("Successfully generated timestamps for the audio track", LOG_PATH)
    return timestamps


def import_audio_clip(path: str) -> list:
    """Opens a audio file for editing\n
    The pointer must be closed after usage

    Args:
        path (str): the path to the file

    Returns:
        AudioFileClip: the imported audio
    """

    try:
        audio_clip = AudioFileClip(path)

    except IOError:
        write_log(f"Audio file at {path} could not be found", LOG_PATH)
        return

    return audio_clip


def create_audio_subclips(audio_clip: AudioFileClip, timestamps: list) -> list:
    """Generates subclips with the audio subtitles

    Args:
        audio_clip (AudioFileClip): the main audio track
        timestamps (list): a list with the timestamps

    Returns:
        list: a list of audio subclips
    """


    subclips = list()

    for timestamp in timestamps:
        clip = audio_clip.subclip(t_start=timestamp[0], t_end=sum(timestamp))
        clip = clip.set_start(timestamp[0])

        subclips.append(clip)



    return subclips

def calculate_total_audio_time(timestamps: list) -> float:
    """Calculates the total video time based on the audio timestamps

    Args:
        timestamps (list): the audio timestamp list

    Returns:
        float: the video duration in seconds
    """
    return sum(timestamps[-1]) + FADE_TO_BLACK_TIME
