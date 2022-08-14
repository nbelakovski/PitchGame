import pyaudio
from pysinewave import SineWave
import numpy as np
from scipy import signal

from pyqtgraph.Qt import QtCore
import pyqtgraph as pg
import sys


# Set up display
win = pg.GraphicsLayoutWidget(show=True, title="PitchGame")
win.resize(1000, 600)
win.setWindowTitle('the game to train your ear')
p6 = win.addPlot(title="The freq")
p6.setXRange(-200, 200)
p6.setYRange(0, 20000)
p6.showGrid(x=True, y=True, alpha=1)
print(type(p6))
curve = p6.plot(pen='y')
curve2 = p6.plot(pen='b')
curve3 = p6.plot(pen='b')

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
halfstep = 2**(1/12)
sing_above_tone = False
num_halfsteps = 0
scale = halfstep**num_halfsteps if sing_above_tone \
        else 1/(halfstep**num_halfsteps)
low = 90/scale
high = 260/scale
pitch = 0
playtime = 1000
recordtime = 10000


def update():
    try:
        data = stream.read(int(CHUNK*2))
    except Exception as err:
        print("Failed to read chunk", err)
        sys.exit(-1)
    numpydata = np.frombuffer(data, dtype=np.int16)
    f, P = signal.periodogram(numpydata, RATE)
    if s.sinewave_generator.amplitude < 0.9:
        curve.setData(f-pitch*scale, P)
    halfstepabove = pitch*scale*halfstep - pitch*scale
    curve2.setData([halfstepabove, halfstepabove], [0, 20000])
    halfstepbelow = pitch*scale/halfstep - pitch*scale
    curve3.setData([halfstepbelow, halfstepbelow], [0, 20000])


s = SineWave(pitch=0, pitch_per_second=1e3, decibels_per_second=5e2)
s.set_volume(-100)
s.play()

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1)


def play():
    # if play.index % 2 == 0:
    #     s.set_volume(-100)
    #     return
    # timer.stop()
    global pitch
    pitch = rng.random() * (high - low) + low
    s.set_frequency(pitch)
    s.set_volume(0)


play.index = 0


def stop():
    # timer.start()
    s.set_volume(-100)


timer2 = QtCore.QTimer()
timer2.timeout.connect(play)
timer2.start(playtime+recordtime)
# create an offset timer to manage the volume reduction
timer4 = QtCore.QTimer()
timer4.timeout.connect(stop)


def createstoptimer():
    print("Setting stop timer")
    timer4.start(playtime+recordtime)


timer3 = QtCore.QTimer()
timer3.timeout.connect(createstoptimer)
timer3.setSingleShot(True)
timer3.start(playtime)
pg.exec()
stream.stop_stream()
stream.close()
audio.terminate()
