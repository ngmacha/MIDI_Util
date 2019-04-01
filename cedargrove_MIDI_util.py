# The MIT License (MIT)

# Copyright (c) 2019 Jan Goolsbey, Cedar Grove Studios

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`cedargrove_MIDI_util`
================================================================================
cedargrove_MIDI_util.py 2019-03-31 v00 09:20PM
A CircuitPython method collection for processing MIDI notes.

* Author(s): Jan Goolsbey

Implementation Notes
--------------------
**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/CedarGroveStudios/MIDI_Util.git"

from math import log  # required for freq_note helper

# list of valid note names used by note_lexo, note_name, and name_note helpers
note_base = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def note_lexo(input):
    """ Bidirectionally translates a MIDI sequential note value to a note name
          or a note name to a MIDI sequential note value. Note values are
          of integer type in the range of 0 to 127 (inclusive). Note names are
          character strings expressed in the format NoteOctave, such as
          'C4' or 'G#7'. Note names can range from 'C-1' (note value 0) to
          'F#9' (note value 127). If the input value is outside of the note
          value or name range, the value of None is returned.
    """
    if type(input) == str:  # if input is type string, assume it's a name
        return name_note(input)  # get note value from name_note helper
    elif type(input) == int:  # if input is integer, assume it's a note value
        return note_name(input)  # get note name from note_name helper
    else: return None  # invalid input parameter type

def note_name(note):
    """ Translates a MIDI sequential note value to a note name. Note values are
          of integer type in the range of 0 to 127 (inclusive). Note names are
          character strings expressed in the format NoteOctave, such as
          'C4' or 'G#7'. Note names can range from 'C-1' (note value 0) to
          'F#9' (note value 127). If the input value is outside of that range,
          the value of None is returned.
    """
    if 0 <= note <= 127:  # check for valid note value range
        return note_base[note % 12] + str((note // 12)-1)  # assemble name
    else: return None  # note value outside valid range

def name_note(name):
    """ Translates a note name to a MIDI sequential note value. Note names are
          character strings expressed in the format NoteOctave, such as
          'C4' or 'G#7'. Note names can range from 'C-1' (note value 0) to
          'F#9' (note value 127). Note values are of integer type in the range
          of 0 to 127 (inclusive). If the input value is outside of that range,
          the value of None is returned.
    """
    name = name.upper()  # convert lower to uppercase
    if (name[:1] or name[:2]) in note_base:  # check for valid note name
        if '#' in name:  # find name and extract octave
            note = note_base.index(name[:2])
            octave = int(name[2:])
        else:  # find name and extract octave
            note = note_base.index(name[0])
            octave = int(name[1:])
        return note + (12 * (octave + 1))  # calculate note value
    else: return None  # string not in note_base

def note_freq(note):
    """ Translates a MIDI sequential note value to its corresponding frequency
          in Hertz (Hz). Note values are of integer type in the range of 0 to
          127 (inclusive). Frequency values are floating point. If the input
          note value is less than 0 or greater than 127, the input is
          considered to be invalid and the value of None is returned.
          Ref: MIDI Tuning Standard formula.
    """
    if 0 <= note <= 127:
        return pow(2, (note - 69) / 12) * 440
    else: return None  # note value outside valid range

def freq_note(freq):
    """ Translates a frequency in Hertz (Hz) to the closest MIDI sequential
          note value. Frequency values are floating point. Note values are of
          integer type in the range of 0 to 127 (inclusive). If the input
          frequency is less than the corresponding frequency for note 0 or
          greater than note 127, the input is considered to be invalid and
          the value of None is returned. Ref: MIDI Tuning Standard formula.
    """
    if (pow(2, (0 - 69) / 12) * 440) <= freq <= (pow(2, (127 - 69) / 12) * 440):
        return int(69 + (12* log(freq / 440, 2)))
    else: return None  # frequency outside valid range
