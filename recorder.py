import pyaudio
from pysinewave import SineWave
import numpy as np
from scipy import signal

from pyqtgraph.Qt import QtCore
import pyqtgraph as pg
import sys


# Set up display
win = pg.GraphicsLayoutWidget(show=True, title="PitchGame")
win.resize(1000,600)
win.setWindowTitle('the game to train your ear')
p6 = win.addPlot(title="The freq")
p6.setXRange(-200, 200)
p6.setYRange(0, 10000)
p6.showGrid(x=True, y=True, alpha=1)
curve = p6.plot(pen='y')

# Set up recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 176400
CHUNK = 8192*2
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

# Set up pitch variation from D2 (73) to F4 (350)
rng = np.random.default_rng()
low = 98
high = 261
pitch = 0

def update():
    try:
        data = stream.read(int(CHUNK*1.5))
    except Exception as err:
        print("Failed to read chunk", err)
        sys.exit(-1)
    numpydata = np.frombuffer(data, dtype=np.int16)
    f, P = signal.periodogram(numpydata, RATE)
    curve.setData(f-pitch, P)


s = SineWave(pitch=0, pitch_per_second=1e3, decibels_per_second=5e3)
s.set_volume(-100)
s.play()
def play():
    play.index += 1
    if play.index % 2 == 0:
        s.set_volume(-100)
        return
    global pitch
    pitch = rng.random() * (high - low) + low
    s.set_frequency(pitch)
    s.set_volume(0)
play.index = 0


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)
timer2 = QtCore.QTimer()
timer2.timeout.connect(play)
timer2.start(1500)
pg.exec()
stream.stop_stream()
stream.close()
audio.terminate()
