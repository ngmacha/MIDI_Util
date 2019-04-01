# MIDI_util_example.py

from cedargrove_MIDI_util import *

note = 61
print('note_lexo helper', note, note_lexo(note))

name = 'G#7'
print('note_lexo helper', name, note_lexo(note))

note = 61
print('note_name helper', note, note_name(note))

name = 'G#7'
print('name_note helper', name, name_note(name))

note = 60
print('note_freq helper', note, note_freq(note))

freq = 262
print('freq_note helper', freq, freq_note(freq))
