from adafruit_circuitplayground.express import cpx
import time
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.control_change   import ControlChange

stopper = 1

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)
pentatonic = [61, 63, 66, 68, 70, 73, 75, 78, 80, 82, 83, 85, 87, 90, 92, 94]

cpx.pixels.brightness = 0.1
cpx.pixels.fill((0, 0, 0))
midi.send(ControlChange(67,0))

def run():
    while True:
        global stopper
        x_float, y_float, z_float = cpx.acceleration  # read accelerometer
        speed = (abs(int(y_float-10)/40))
        pitchbend = (int(x_float+10))
        velocitybend = (int(y_float+20)*4)
        if cpx.button_a:
            time.sleep(0.1)
            cpx.pixels[5] = (255,0,0)
            wait()
        elif cpx.touch_A2 and pitchbend > 0 and pitchbend < 16:
            midi.send(NoteOn(54,100))
            midi.send(NoteOn(pentatonic[pitchbend], velocitybend))
            time.sleep(speed)
        elif pitchbend > 0 and pitchbend < 16:
            print(stopper)
            midi.send(NoteOn(pentatonic[pitchbend], velocitybend))
            stopper = pitchbend
            time.sleep(speed)

def test():
    while True:
        x, y, z = cpx.acceleration  # read accelerometer
        print((x,y,z))
        cpx.pixels[5] = (0,0,255)
        if cpx.button_b:
            time.sleep(0.2)
            wait()
        elif (y < 10):
            midi.send(ControlChange(50,int((y+10)*6.35)))


def wait():
    cpx.pixels[5] = (255,0,0)
    while True:
        if cpx.button_a:
            time.sleep(0.2)
            cpx.pixels[5] = (0, 255, 0)
            run()
        if cpx.button_b:
            time.sleep(0.2)
            test()

wait()