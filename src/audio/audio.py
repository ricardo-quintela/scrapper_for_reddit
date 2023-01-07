"""Module for analysing audio and extractiong timestamps
"""

import wave
from json import dumps, loads

from vosk import Model, KaldiRecognizer, SetLogLevel

from moviepy.editor import AudioFileClip
from utils import write_log, wrap_data
from settings import LOG_PATH, MODEL_PATH, FADE_TO_BLACK_TIME


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


def get_timestamps(audio_track: wave.Wave_read, script: list, save_lines: bool) -> list:
    """Returns the script line timestamps from the audio track

    Args:
        audio_track (Wave_read): the wav mono audio track
        script (list): the list of lines on the script
        save_lines (bool): whether to save the speech recognition lines or not

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

    # get the number of frames to print the progress
    total_of_frames = audio_track.getnframes()

    progress = 0
    # loop through all the audio
    while data := audio_track.readframes(4000):

        # if a sentence has been successfully parsed -> add to results
        if rec.AcceptWaveform(data):
            results += loads(rec.Result())["result"]
            rec.SetGrammar(sentence_list_str)

        else:
            progress += 4000
            write_log(
                f"Generating audio track timestamps: {progress}/{total_of_frames}",
                LOG_PATH
            )

    # add the final sentence
    results += loads(rec.FinalResult())["result"]
    write_log(
        f"Generating audio track timestamps: {total_of_frames}/{total_of_frames}",
        LOG_PATH
    )

    # save the lines gathered to json
    if save_lines:
        model_string = ""
        for word in results:
            w_text = word["word"]
            model_string += f"{w_text} "
        model_lines = wrap_data(model_string)

        with open("speech_recognition_lines.md", "w", encoding="utf-8") as speech_file:
            for line in model_lines:
                speech_file.write(f"{line}\n")

        write_log("Saved speech in speech_recognition_lines.md", LOG_PATH)


    # close the audio file
    audio_track.close()

    # create a list of timestamps
    timestamps = list()

     # add timestamps for all the lines
    index = 0
    for sentence in script:

        # start of the line
        start = results[index]["start"]

        index += len(sentence.split()) - 1

        try:
            # duration of the line
            duration = results[index]["end"] - start

        # while parsing the script doesnt match the audio
        except IndexError:
            write_log(
                "ERROR: audio track doesn't match script\n Did you read the script properly?",
                LOG_PATH
            )
            return

        timestamps.append((start, duration))

        index += 1


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
