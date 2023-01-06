import wave
from json import loads, dumps

from vosk import Model, KaldiRecognizer

model_path = "model/vosk-model-en-us-0.22"
audio_filename = "test_rec.wav"

model = Model(model_path)
wf = wave.open(audio_filename, "rb")


with open("test_audio_script.txt", "r", encoding="utf-8") as file:
    script = dumps(file.readlines())


# set words need to be set to true to record the timestamps
rec = KaldiRecognizer(model, wf.getframerate(), script)
rec.SetWords(True)
rec.SetGrammar(script)

# get the list of JSON dictionaries
results = []
# recognize speech using vosk model
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        part_result = loads(rec.Result())
        results.append(part_result)
# part_result = json.loads(rec.FinalResult())
# results.append(part_result)

wf.close()  # close audiofile
# convert list of JSON dictionaries to list of 'Word' objects
list_of_Words = []


print(results)
