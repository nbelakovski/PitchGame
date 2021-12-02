import pyaudio
from pysinewave import SineWave
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import wave

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

win = pg.GraphicsLayoutWidget(show=True, title="PitchGame")
win.resize(1000,600)
win.setWindowTitle('the game to train your ear')

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 176400
CHUNK = 8192*2
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "file.wav"

# start Recording

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

p6 = win.addPlot(title="The freq")
p6.setXRange(50, 400)
p6.setYRange(0, 10000)
p6.showGrid(x=True, y=True, alpha=1)
curve = p6.plot(pen='y')
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
def update():
    
    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    numpydata = np.frombuffer(data, dtype=np.int16)
    f, P = signal.periodogram(numpydata, RATE)
    curve.setData(f, P)
    print("P:", max(P))
    # idx = signal.find_peaks(P, height=10000)[0][0]
    # print("f: ", f[idx])


s = SineWave()
def play():
    play.index += 1
    if play.index % 2:
        s.stop()
        return
    
    pitch = rng.random() * (high - low) + low
    s.set_frequency(pitch)
    s.play()


    
play.index = 0
print("finished recording")
# print(dir(data))
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)
timer2 = QtCore.QTimer()
timer2.timeout.connect(play)
timer2.start(1000)
pg.exec()
stream.stop_stream()
stream.close()
audio.terminate()



# waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# waveFile.setnchannels(CHANNELS)
# waveFile.setsampwidth(audio.get_sample_size(FORMAT))
# waveFile.setframerate(RATE)
# waveFile.writeframes(b''.join(frames))
# waveFile.close()
# pg.plot(f, P)
# s = SineWave()
# s.set_frequency(pitch)
# s.play()
# s.stop()
