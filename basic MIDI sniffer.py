# KJW sniffer.py
# 2019-06-14 Cedar Grove Studios
# based upon @kevinjwalter's midi library and examples
#

import time
import usb_midi
import adafruit_midi
import busio
import board

from adafruit_midi.timing_clock            import TimingClock
from adafruit_midi.channel_pressure        import ChannelPressure
from adafruit_midi.control_change          import ControlChange
from adafruit_midi.note_off                import NoteOff
from adafruit_midi.note_on                 import NoteOn
from adafruit_midi.pitch_bend              import PitchBend
from adafruit_midi.polyphonic_key_pressure import PolyphonicKeyPressure
from adafruit_midi.program_change          import ProgramChange
from adafruit_midi.start                   import Start
from adafruit_midi.stop                    import Stop
from adafruit_midi.system_exclusive        import SystemExclusive
from adafruit_midi.midi_message            import MIDIUnknownEvent

from cedargrove_MIDI_util                  import *

UART = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
midi = adafruit_midi.MIDI(midi_in=UART, in_channel=0)
# 0 is MIDI channel 1

print("basic MIDI sniffer.py 2019-06-14 CedarGrove")
# Convert channel numbers at the presentation layer to the ones musicians use
print("Input channel:", midi.in_channel + 1 )

t0 = time.monotonic()

while True:

    msg = midi.receive()
    if msg is not None:
        # print("Time: ",time.monotonic())  # time stamp

        if isinstance(msg, NoteOn):
            print("NoteOn : #%02d %s %5.3fHz" % (msg.note, note_lexo(msg.note), note_freq(msg.note)))
            print("     vel   %03d     chan #%02d" %(msg.velocity, msg.channel + 1))

        elif isinstance(msg, NoteOff):
            print("NoteOff: #%02d %s %5.3fHz" % (msg.note, note_lexo(msg.note), note_freq(msg.note)))
            print("     vel   %03d     chan #%02d" %(msg.velocity, msg.channel + 1))

        elif isinstance(msg, TimingClock):
            print("-- Tick: %03.1f BPM" % (1/((time.monotonic()-t0)*24)*60))  # compared to previous tick
            t0 = time.monotonic()

        elif isinstance(msg, ChannelPressure):
            print("ChannelPressure: ")
            print("     press %03d     chan #%02d" %(msg.pressure, msg.channel + 1))

        elif isinstance(msg, ControlChange):
            print("ControlChange: ctrl #%03d" % msg.control)
            print("     value %03d     chan #%02d" %(msg.value, msg.channel + 1))

        elif isinstance(msg, PitchBend):
            print("PitchBend: ")
            print("     bend  %05d   chan #%02d" %(msg.pitch_bend, msg.channel + 1))

        elif isinstance(msg, PolyphonicKeyPressure):
            print("PolyphonicKeyPressure:")
            print("          #%02d %s %5.3fHz" % (msg.note, note_lexo(msg.note), note_freq(msg.note)))
            print("     press %03d     chan #%02d" %(msg.pressure, msg.channel + 1))

        elif isinstance(msg, ProgramChange):
            print("ProgramChange:")
            print("     patch %03d     chan #%02d" %(msg.patch, msg.channel + 1))

        elif isinstance(msg, Start): print("-- Start --")

        elif isinstance(msg, Stop): print("-- Stop --")

        elif isinstance(msg, SystemExclusive):
            print("SystemExclusive:  ID= ", msg.manufacturer_id,
                  ", data= ", msg.data)

        elif isinstance(msg, MIDIUnknownEvent):
            # Message are only known if they are imported
            print("Unknown MIDI event status ", msg.status)
