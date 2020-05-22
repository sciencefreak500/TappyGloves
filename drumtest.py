
import serial
import pyglet
pyglet.options['search_local_libs'] = True
from datetime import datetime


bpm = 120
bps = bpm/60
start_time = datetime.now()
time_build = 0
data_array = {}
temp_array = {}
register_hit = {}
bass_hit = False

# hi-hat
low_hi_hat = pyglet.media.StaticSource(
    pyglet.media.load('selected_sounds/hi_hat/hi_hat_5.wav')
)
high_hi_hat = pyglet.media.StaticSource(
    pyglet.media.load('selected_sounds/hi_hat/hi_hat_8.wav')
)

# snare drum
low_snare = pyglet.media.StaticSource(
    pyglet.media.load('selected_sounds/snare/snare_3.wav')
)
high_snare = pyglet.media.StaticSource(
    pyglet.media.load('selected_sounds/snare/snare_5.wav')
)

# splash
low_splash = pyglet.media.StaticSource(
    pyglet.media.load('selected_sounds/splash/crash_3.wav')
)
high_splash = pyglet.media.StaticSource(
    pyglet.media.load('selected_sounds/splash/crash_4.wav')
)

# bell
low_bell = pyglet.media.StaticSource(
    pyglet.media.load('selected_sounds/bell/bell_1.wav')
)
high_bell = pyglet.media.StaticSource(
    pyglet.media.load('selected_sounds/bell/bell_2.wav')
)

kick_sound = pyglet.media.StaticSource(
    pyglet.media.load('selected_sounds/kick/kick_4.wav')
)

def array_average(arr):
    result = 0
    for i in arr:
        result += i
    return result/len(arr)


def sense_bass(value):
    global bass_hit
    if value < 17:
        if not bass_hit:
            bass_hit = True
            kick_sound.play()
    else:
        bass_hit = False


def play_sound(pin, value):
    if pin == 'middle':
        if value > 60:
            print('light hit')
            # low_hi_hat.play()
            high_hi_hat.play()
            kick_sound.play()
        else:
            print('heavy hit')
            high_hi_hat.play()
    if pin == 'index':
        if value > 100:
            print('light hit')
            low_snare.play()
        else:
            print('heavy hit')
            high_snare.play()
    if pin == 'ring':
        if value > 50:
            print('light hit')
            low_splash.play()
        else:
            print('heavy hit')
            high_splash.play()
    if pin == 'pinky':
        if value > 40:
            print('light hit')
            low_bell.play()
        else:
            print('heavy hit')
            high_bell.play()


def metronome():
    pass
    # current_time = datetime.now()
    # time_diff = start_time - current_time




def sense_hits(pin, value, threshold):
    try:
        data_array[pin].append(value)
    except KeyError:
        data_array[pin] = []
        data_array[pin].append(value)
    if len(data_array[pin]) > 19:
        data_array[pin].pop(0)
    value = array_average(data_array[pin])

    if value < threshold:
        try:
            register_hit[pin]
        except KeyError:
            register_hit[pin] = False
        if not register_hit[pin]:
            try:
                temp_array[pin].append(value)
            except KeyError:
                temp_array[pin] = []
                temp_array[pin].append(value)
        if len(temp_array[pin]) > 5:
            if (temp_array[pin][-1] > temp_array[pin][-2] and
                temp_array[pin][-2] > temp_array[pin][-3] and
                temp_array[pin][-3] > temp_array[pin][-4] and
                temp_array[pin][-4] > temp_array[pin][-5]
            ):
                print(pin, value)
                register_hit[pin] = True
                temp_array[pin] = []
                play_sound(pin, value)
    else:
        register_hit[pin] = False
        temp_array[pin] = []


flora = serial.Serial('/dev/ttyACM0', 9800, timeout=.1)
# bassflora = serial.Serial('/dev/ttyACM1', 9800, timeout=.1)
print(flora)

while True:
    metronome()
    data = flora.readline()[:-2]  # bassflora.readline()[:-2])
    if data:
        try:
            obj = data.decode().split(',')
            # bass = data[1].decode().split(',')
            thresholds = {
                'index': 200,
                'middle': 225,
                'ring': 100,
                'pinky': 100
            }
            try:
                pinnout = str(obj[0])
                vals = int(obj[1])
                threshes = thresholds[obj[0]]
                sense_hits(pinnout, vals, threshes)
            except:
                print('skip')
            # sense_bass(int(bass[1]))
        except IndexError:
            print('fuck you')
