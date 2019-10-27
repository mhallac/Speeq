import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

#imports package to handle file paths
import ntpath

# Instantiates a client
client = speech.SpeechClient()

#sets file name
file_name = "c:/Users/mhall/Desktop/Speeq/newfile.raw"
file_name = ntpath.normpath(file_name)

# Loads the audio into memory
with io.open(file_name, 'rb') as audio_file:
    content = audio_file.read()
    audio = types.RecognitionAudio(content=content)

config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code='en-US')

# Detects speech in the audio file
response = client.recognize(config, audio)


for result in response.results:
    print("hi there")
    print('Transcript: {}'.format(result.alternatives[0].transcript))
