import pyaudio
import wave
import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

#imports package to handle file paths
import ntpath

#import gui tool
import tkinter as tk
from tkinter import *

import time

main=tk.Tk()

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = int(RATE / 10)
RECORD_SECONDS = 10

output = ""
record = False

def stop():
    record=False
    main.destroy()

def start():

    spoken = ""
    print("entering loop", flush=True)
    record=True
    t0.set("Number of words: " + str(len(input.get().split(' '))))
    output0.update()
    now = time.time()
    while record:
        for i in range(0, 2):
            #sets file name
            file_name = "c:/Users/mhall/Desktop/Speeq/newfile" + str(i) + ".raw"
            file_name = ntpath.normpath(file_name)

            print("recording...", flush=True)
            audio = pyaudio.PyAudio()

            # start Recording
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
            frames = []

            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)
            print("finished recording", flush=True)

            # stop Recording
            stream.stop_stream()
            stream.close()
            audio.terminate()

            print("Recording to " + str(i), flush=True)
            file = open(file_name, "wb")
            file.write(b''.join(frames))
            file.close()

            print("test Client", flush=True)

            # Instantiates a client
            client = speech.SpeechClient()

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
                spoken += " " + result.alternatives[0].transcript
                wordsSpoken = len(spoken.split(' '))
                totWords = len(input.get().split(' '))
                timeElapsed = (time.time() - now) / 60
                expectedMin = timeElapsed * totWords / wordsSpoken
                t1.set("Expected presentation time: {:0.2f}".format(expectedMin) + " minutes.")
                output1.update()
                t2.set("Words Spoken: " + str(wordsSpoken))
                output2.update()

                t3.set("Time Elapsed: {:0.2f}".format(timeElapsed) + " minutes.")
                output3.update()
                print(spoken, flush=True)

tk.Label(main, text="Copy your presentation here:").grid(row=0)
input=tk.Entry(main, width=25)
input.grid(row=1)
tk.Button(main, text='Start', width=25, command = start).grid(row=2)
close=tk.Button(main, text='Close', width=25, command=stop).grid(row=3)
t0=tk.StringVar(main)
output0=tk.Label(main, textvariable=t0)
output0.grid(row=4)
t0.set("Number of words: ")

t1=tk.StringVar(main)
output1=tk.Label(main, textvariable=t1)
t1.set("Expected presentation time:")

t2=tk.StringVar(main)
output2=tk.Label(main, textvariable=t2)
t2.set("Words Spoken:")

t3=tk.StringVar(main)
output3=tk.Label(main, textvariable=t3)
t3.set("Time Elapsed:")

output1.grid(row=5)
output2.grid(row=6)
output3.grid(row=7)

main.mainloop()
