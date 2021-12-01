import pyaudio
from pysinewave import SineWave
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import wave

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2048
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print("recording...")
frames = []
# pick a random number between 98 (G2) and 350 (F4)
# generate the tone with sinewave for 2 seconds
# record for 2 seconds displaying delta between
# detected pitch and chosen pitch
#
rng = np.random.default_rng()
low = 98
high = 350
# while True:  # or until ctrl+d
pitch = rng.random() * (high - low) + low
#     print("WIP")

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    numpydata = np.frombuffer(data, dtype=np.int16)
    f, P = signal.periodogram(numpydata, RATE)
    print("P:", max(P))
    idx = signal.find_peaks(P, height=10000)[0][0]
    print("f: ", f[idx])
    frames.append(data)
print("finished recording")
print(dir(data))


# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
pg.plot(f, P)
s = SineWave()
s.set_frequency(pitch)
s.play()
pg.exec()
s.stop()
