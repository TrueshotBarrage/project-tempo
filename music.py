import csv
import random
import operator
import subprocess
import numpy as np


class Music:
  def __init__(self, key):
    self.midi_type = 1
    self.num_tracks = 1
    self.quarter_note = 480
    self.ts_num = 4
    self.ts_denom = 2  # negative power of two, e.g. quarter note = 2; eighth note = 3
    self.key_signature = key  # -7 to 7 inclusive; flats (-) & sharps (+)
    self.major = "major"
    self.bpm = 120
    # 500000 = 120 quarter notes (beats) per minute; also 60,000,000 / bpm
    self.tempo = 60000000 / self.bpm

    self.LH_instrument = 0
    self.RH_instrument = 0
    self.misc_instrument1 = 0
    self.misc_instrument2 = 26  # Electric Guitar (jazz)

    self.LH_time = 0
    self.RH_time = 0
    self.misc_time1 = 0
    self.misc_time2 = 0
    self.lines = []

  # Song setup
  def start(self):
    self.lines.append(
        [0, 0, 'Header', self.midi_type, self.num_tracks, self.quarter_note])
    self.lines.append([1, 0, 'Start_track'])
    self.lines.append(
        [1, 0, 'Time_signature', self.ts_num, self.ts_denom, 24, 8])
    self.lines.append([1, 0, 'Key_signature', self.key_signature, self.major])
    self.lines.append([1, 0, 'Tempo', self.tempo])

    # These remain to be seen what they do exactly...
    self.lines.append([1, 0, 'Control_c', 0, 121, 0])
    self.lines.append([1, 0, 'Program_c', 0, self.LH_instrument])  # 0 = piano
    self.lines.append([1, 0, 'MIDI_port', 0])

    self.lines.append([1, 0, 'Control_c', 1, 121, 0])
    self.lines.append([1, 0, 'Program_c', 1, self.RH_instrument])
    self.lines.append([1, 0, 'MIDI_port', 1])

    self.lines.append([1, 0, 'Control_c', 2, 121, 0])
    self.lines.append([1, 0, 'Program_c', 2, self.misc_instrument1])
    self.lines.append([1, 0, 'MIDI_port', 2])

    self.lines.append([1, 0, 'Control_c', 3, 121, 0])
    self.lines.append([1, 0, 'Program_c', 3, self.misc_instrument2])
    self.lines.append([1, 0, 'MIDI_port', 3])

  # Song wrap-up
  def finish(self, filename):
    self.lines = sorted(self.lines, key=operator.itemgetter(1))
    total_time = self.LH_time if self.LH_time > self.RH_time else self.RH_time
    total_time = self.misc_time1 if self.misc_time1 > total_time else total_time
    total_time = self.misc_time2 if self.misc_time2 > total_time else total_time

    self.lines.append([1, total_time, 'End_track'])
    self.lines.append([0, 0, 'End_of_file'])

    with open(filename + ".csv", 'w') as writeFile:
      writer = csv.writer(writeFile)
      writer.writerows(self.lines)

    writeFile.close()
    subprocess.run(["./csvmidi", filename + ".csv", filename + ".mid"])

  # Wrapper for repeating any method indefinitely
  def repeat(self, func, args, n):
    for _ in range(n):
      x = func(*args)
    return

# ----------------------------------------------------------------------------------------------

# 1-3-5 block chords and their inversions

  def major_135_chord(self, note, length, ch):
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note, 80])
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 4, 80])
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 7, 80])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note, 0])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 4, 0])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 7, 0])

    self.LH_time += length

  def minor_135_chord(self, note, length, ch):
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note, 80])
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 3, 80])
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 7, 80])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note, 0])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 3, 0])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 7, 0])

    self.LH_time += length

  def major_135_chord_inv1(self, note, length, ch):
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 4, 80])
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 7, 80])
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 12, 80])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 4, 0])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 7, 0])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 12, 0])

    self.LH_time += length

  def minor_135_chord_inv1(self, note, length, ch):
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 3, 80])
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 7, 80])
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 12, 80])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 3, 0])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 7, 0])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 12, 0])

    self.LH_time += length

  def major_135_chord_inv2(self, note, length, ch):
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 7, 80])
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 12, 80])
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 16, 80])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 7, 0])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 12, 0])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 16, 0])

    self.LH_time += length

  def minor_135_chord_inv2(self, note, length, ch):
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 7, 80])
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 12, 80])
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 15, 80])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 7, 0])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 12, 0])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 15, 0])

    self.LH_time += length

# ------------------------------------------------------------------------------------------------

# 1-5 chords and their inversions (1-5, 3-8, 5-10)

  def major_15_chord(self, note, length, ch):
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note, 80])
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 7, 80])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note, 0])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 7, 0])

    self.LH_time += length

  def minor_15_chord(self, note, length, ch):
    self.lines.append([1, self.LH_time, 'Note_on_c', 0, note, 80])
    self.lines.append([1, self.LH_time, 'Note_on_c', 0, note + 7, 80])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', 0, note, 0])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', 0, note + 7, 0])

    self.LH_time += length

  def major_15_chord_inv1(self, note, length, ch):
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 4, 80])
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 12, 80])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 4, 0])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 12, 0])

    self.LH_time += length

  def minor_15_chord_inv1(self, note, length, ch):
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 3, 80])
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 12, 80])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 3, 0])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 12, 0])

    self.LH_time += length

  def major_15_chord_inv2(self, note, length, ch):
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 7, 80])
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 16, 80])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 7, 0])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 16, 0])

    self.LH_time += length

  def minor_15_chord_inv2(self, note, length, ch):
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 7, 80])
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 15, 80])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 7, 0])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 15, 0])

    self.LH_time += length

# -------------------------------------------------------------------------------------------------

# 1-3-5 arpeggiated chord
# Played on beats 1, 2, 3 (not 4)

  def major_135_chord_arpeg(self, note, length, ch):
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note, 80])
    self.lines.append(
        [1, self.LH_time + (length / 4), 'Note_off_c', ch, note, 0])
    self.lines.append(
        [1, self.LH_time + (length / 4), 'Note_on_c', ch, note + 4, 80])
    self.lines.append(
        [1, self.LH_time + (length / 2), 'Note_off_c', ch, note + 4, 0])
    self.lines.append(
        [1, self.LH_time + (length / 2), 'Note_on_c', ch, note + 7, 80])
    self.lines.append(
        [1, self.LH_time + length, 'Note_off_c', ch, note + 7, 0])

    self.LH_time += length

  def minor_135_chord_arpeg(self, note, length, ch):
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note, 80])
    self.lines.append(
        [1, self.LH_time + (length / 4), 'Note_off_c', ch, note, 0])
    self.lines.append(
        [1, self.LH_time + (length / 4), 'Note_on_c', ch, note + 3, 80])
    self.lines.append(
        [1, self.LH_time + (length / 2), 'Note_off_c', ch, note + 3, 0])
    self.lines.append(
        [1, self.LH_time + (length / 2), 'Note_on_c', ch, note + 7, 80])
    self.lines.append(
        [1, self.LH_time + length, 'Note_off_c', ch, note + 7, 0])

    self.LH_time += length

  # 1-5-8 arpeggiated chord
  # Played on beats 1, 2, 3 (not 4)
  def tonic_158_chord_arpeg(self, note, length, ch):
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note, 80])
    self.lines.append(
        [1, self.LH_time + (length / 4), 'Note_off_c', ch, note, 0])
    self.lines.append(
        [1, self.LH_time + (length / 4), 'Note_on_c', ch, note + 7, 80])
    self.lines.append(
        [1, self.LH_time + (length / 2), 'Note_off_c', ch, note + 7, 0])
    self.lines.append(
        [1, self.LH_time + (length / 2), 'Note_on_c', ch, note + 12, 80])
    self.lines.append(
        [1, self.LH_time + length, 'Note_off_c', ch, note + 12, 0])

    self.LH_time += length

  # 1-5-8-10 arpeggiated chord
  # Played on all 4 beats
  def modified_tonic_158_chord_arpeg(self, note, length, ch):
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note, 80])
    self.lines.append(
        [1, self.LH_time + (length / 4), 'Note_off_c', ch, note, 0])
    self.lines.append(
        [1, self.LH_time + (length / 4), 'Note_on_c', ch, note + 7, 80])
    self.lines.append(
        [1, self.LH_time + (length / 2), 'Note_off_c', ch, note + 7, 0])
    self.lines.append(
        [1, self.LH_time + (length / 2), 'Note_on_c', ch, note + 12, 80])
    self.lines.append(
        [1, self.LH_time + (3 * length / 4), 'Note_off_c', ch, note + 12, 0])
    self.lines.append(
        [1, self.LH_time + (3 * length / 4), 'Note_on_c', ch, note + 14, 80])
    self.lines.append(
        [1, self.LH_time + length, 'Note_off_c', ch, note + 14, 0])

    self.LH_time += length

  # 3-5-8 arpeggiated chord
  # Really fast! Good finisher.
  def fast_358_chord_arpeg(self, note, length, ch):
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, note + 4, 80])
    self.lines.append(
        [1, self.LH_time + (length / 32), 'Note_off_c', ch, note + 4, 0])
    self.lines.append(
        [1, self.LH_time + (length / 32), 'Note_on_c', ch, note + 7, 80])
    self.lines.append(
        [1, self.LH_time + (length / 16), 'Note_off_c', ch, note + 7, 0])
    self.lines.append(
        [1, self.LH_time + (length / 16), 'Note_on_c', ch, note + 12, 80])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, note + 12, 0])

    self.RH_time += length

# -------------------------------------------------------------------------------------------------

# Truly something else. Just try it out...
# Too hard to explain in words. Jazzy!

  def jazzy_rhythm_note_top(self, note, length, ch):
    self.lines.append([1, self.RH_time, 'Note_on_c', ch, note, 80])
    self.lines.append(
        [1, self.RH_time + (length / 16), 'Note_off_c', ch, note, 0])
    self.lines.append(
        [1, self.RH_time + (2 * length / 16), 'Note_on_c', ch, note, 80])
    self.lines.append(
        [1, self.RH_time + (3 * length / 16), 'Note_off_c', ch, note, 0])
    self.lines.append(
        [1, self.RH_time + (4 * length / 16), 'Note_on_c', ch, note, 80])
    self.lines.append(
        [1, self.RH_time + (5 * length / 16), 'Note_off_c', ch, note, 0])
    self.lines.append(
        [1, self.RH_time + (6 * length / 16), 'Note_on_c', ch, note, 80])
    self.lines.append(
        [1, self.RH_time + (7 * length / 16), 'Note_off_c', ch, note, 0])
    self.lines.append(
        [1, self.RH_time + (8 * length / 16), 'Note_on_c', ch, note, 80])
    self.lines.append(
        [1, self.RH_time + (9 * length / 16), 'Note_off_c', ch, note, 0])
    self.lines.append(
        [1, self.RH_time + (10 * length / 16), 'Note_on_c', ch, note, 80])
    self.lines.append(
        [1, self.RH_time + (11 * length / 16), 'Note_off_c', ch, note, 0])

    self.lines.append(
        [1, self.RH_time + (23 * length / 32), 'Note_on_c', ch, note, 80])
    self.lines.append(
        [1, self.RH_time + (12 * length / 16), 'Note_off_c', ch, note, 0])
    self.lines.append(
        [1, self.RH_time + (25 * length / 32), 'Note_on_c', ch, note, 80])
    self.lines.append(
        [1, self.RH_time + (13 * length / 16), 'Note_off_c', ch, note, 0])
    self.lines.append(
        [1, self.RH_time + (14 * length / 16), 'Note_on_c', ch, note, 80])
    self.lines.append(
        [1, self.RH_time + (15 * length / 16), 'Note_off_c', ch, note, 0])

    self.RH_time += length

# -------------------------------------------------------------------------------------------------

# Random block chords

  def random_block_chords(self, amount, chord_length, ch):
    for _ in range(amount):
      note = random.randrange(48, 60, 1)
      self.major_135_chord(note, chord_length, ch)

  # 1-4-6-5 chord progression, played in random keys
  def random_block_prog_1465(self, amount, chord_length, ch):
    for _ in range(amount):
      offset = random.randrange(0, 11, 1)
      prog = np.array([36, 41, 45, 43]) + offset

      self.major_135_chord(prog[0], chord_length, ch)
      self.major_135_chord(prog[1], chord_length, ch)
      self.minor_135_chord(prog[2], chord_length, ch)
      self.major_135_chord(prog[3], chord_length, ch)

    return prog

  # 1-4-6-5 block chord progression,
  # played with specific "key" offset
  def block_prog_1465(self, amount, chord_length, key, ch):
    for _ in range(amount):
      prog = np.array([36, 41, 45, 43]) + key

      self.major_135_chord(prog[0], chord_length, ch)
      self.major_135_chord(prog[1], chord_length, ch)
      self.minor_135_chord(prog[2], chord_length, ch)
      self.major_135_chord(prog[3], chord_length, ch)

    return prog

  # 1-4-6-5 arpeggiated chord progression,
  # played with specific "key" offset
  def arpeg_prog_1465(self, amount, chord_length, key, ch):
    for _ in range(amount):
      prog = np.array([36, 41, 45, 43]) + key

      self.major_135_chord_arpeg(prog[0], chord_length, ch)
      self.major_135_chord_arpeg(prog[1], chord_length, ch)
      self.minor_135_chord_arpeg(prog[2], chord_length, ch)
      self.major_135_chord_arpeg(prog[3], chord_length, ch)

    return prog

  # 1-4-6-5 arpeggiated chord progression,
  # played with specific "key" offset,
  # with tonic chords instead of major/minor chords
  def tonic_arpeg_prog_1465(self, amount, chord_length, key, ch):
    for _ in range(amount):
      prog = np.array([36, 41, 45, 43]) + key

      self.tonic_158_chord_arpeg(prog[0], chord_length, ch)
      self.tonic_158_chord_arpeg(prog[1], chord_length, ch)
      self.tonic_158_chord_arpeg(prog[2], chord_length, ch)
      self.tonic_158_chord_arpeg(prog[3], chord_length, ch)

    return prog

  # 1-4-5-5 block chord progression,
  # played with specific "key" offset
  # Extremely jazzy offbeats included!
  def jazzy_block_prog_1455(self, amount, chord_length, key, ch):
    for _ in range(amount):
      # prog contains a duplicate 43 because the double-count
      # has to be maintained for the returned array for other
      # methods to work (i.e. shuffled prog method)
      prog = np.array([36, 41, 43, 43]) + key

      self.major_135_chord_inv1(prog[0], chord_length / 4, ch)
      self.repeat(self.major_15_chord_inv1, [prog[0], chord_length / 4, ch], 2)
      self.repeat(self.major_15_chord_inv1, [prog[0], chord_length / 8, ch], 2)

      self.repeat(self.major_15_chord, [prog[1], chord_length / 4, ch], 3)
      self.repeat(self.major_15_chord, [prog[1], chord_length / 8, ch], 2)

      # The middle two lines could be combined into one repeat(4);
      # functionally the same, but written as such for semantics
      self.repeat(self.major_15_chord, [prog[2], chord_length / 4, ch], 3)
      self.repeat(self.major_15_chord, [prog[2], chord_length / 8, ch], 2)
      self.repeat(self.major_15_chord, [prog[3], chord_length / 8, ch], 2)
      self.repeat(self.major_15_chord, [prog[3], chord_length / 4, ch], 3)

    return prog

  # 6-4-5-5 block chord progression,
  # played with specific "key" offset
  # Extremely jazzy offbeats included!
  def jazzy_block_prog_6455(self, amount, chord_length, key, ch):
    for _ in range(amount):
      # prog contains a duplicate 43 because the double-count
      # has to be maintained for the returned array for other
      # methods to work (i.e. shuffled prog method)
      prog = np.array([45, 41, 43, 43]) + key

      self.minor_135_chord(prog[0], chord_length / 4, ch)
      self.repeat(self.minor_15_chord, [prog[0], chord_length / 4, ch], 2)
      self.repeat(self.minor_15_chord, [prog[0], chord_length / 8, ch], 2)

      self.repeat(self.major_15_chord, [prog[1], chord_length / 4, ch], 3)
      self.repeat(self.major_15_chord, [prog[1], chord_length / 8, ch], 2)

      # The middle two lines could be combined into one repeat(4);
      # functionally the same, but written as such for semantics
      self.repeat(self.major_15_chord, [prog[2], chord_length / 4, ch], 3)
      self.repeat(self.major_15_chord, [prog[2], chord_length / 8, ch], 2)
      self.repeat(self.major_15_chord, [prog[3], chord_length / 8, ch], 2)
      self.repeat(self.major_15_chord, [prog[3], chord_length / 4, ch], 3)

    return prog

  # Xavier's Theme from X-Men: Days of
  # Future Past (left hand)!
  # 6-3-4-2 arpeggiated chord progression.
  def xmen_prog_6342(self, amount, chord_length, key, ch):
    for _ in range(amount):
      prog = np.array([45, 40, 41, 38]) + key
      self.repeat(self.tonic_158_chord_arpeg, [prog[0], chord_length, ch], 2)
      self.repeat(self.tonic_158_chord_arpeg, [prog[1], chord_length, ch], 2)
      self.repeat(self.tonic_158_chord_arpeg, [prog[2], chord_length, ch], 2)
      self.repeat(self.tonic_158_chord_arpeg, [prog[3], chord_length, ch], 2)

    return prog

  # Random assortment of chord progressions.
  # Highly experimental right now.
  def shuffled_chord_progs(self, amount, chord_length, key, ch):
    prog = np.array([], dtype=int)

    options = [(self.block_prog_1465, [1, chord_length, key, ch]),
               (self.arpeg_prog_1465, [1, chord_length, key, ch]),
               (self.tonic_arpeg_prog_1465, [1, chord_length, key, ch]),
               (self.jazzy_block_prog_1455, [1, int(chord_length), key, ch]),
               (self.jazzy_block_prog_6455, [1, int(chord_length), key, ch])]

    for _ in range(amount):
      x = random.randrange(0, len(options))
      prog = np.append(prog, options[x][0](*options[x][1]))

    return prog


# -------------------------------------------------------------------------------------------------

# Plays a (truly) random RH melody,
# chosen from any 7 notes of the major scale

  def truly_random_melody(self, amount, length, key, ch):
    notes = np.array([60, 62, 64, 65, 67, 69, 71, 72]) + key

    for _ in range(amount):
      note = random.choice(notes)
      self.lines.append([1, self.misc_time1, 'Note_on_c', ch, note, 80])
      self.lines.append(
          [1, self.misc_time1 + (7 * length / 8), 'Note_off_c', ch, note, 0])

      self.misc_time1 += length

  # Plays a random RH melody, but uses weights
  # to probabilistically determine the next (best) note
  def random_melody(self, amount, length, key, ch):
    n = 0
    notes = np.array([n, n - 1, n + 2, n - 3, n + 4, n - 5, n + 6]) + key + 65
    note = random.choice(notes)

    for _ in range(amount):
      self.lines.append([1, self.misc_time1, 'Note_on_c', ch, note, 80])
      self.lines.append(
          [1, self.misc_time1 + (7 * length / 8), 'Note_off_c', ch, note, 0])

      self.misc_time1 += length

      weights = [0.016, 0.38, 0.38, 0.08, 0.08, 0.032, 0.032]
      n = note - 65
      next_note = random.choices(population=notes, weights=weights)
      note = next_note[0]

  # Takes an input note and plays a randomly chosen
  # major note, assuming the given note is the tonic
  # note (i.e. one of 1-3-5 for a given 1)
  def tonic_major_melody(self, note, amount, length, ch):
    notes = np.array([note, note + 4, note + 7])

    for _ in range(amount):
      new_note = random.choice(notes)
      self.lines.append([1, self.RH_time, 'Note_on_c', ch, new_note, 80])
      self.lines.append(
          [1, self.RH_time + (7 * length / 8), 'Note_off_c', ch, new_note, 0])

      self.RH_time += length

  # Same as tonic_major_melody but minor
  def tonic_minor_melody(self, note, amount, length, ch):
    notes = np.array([note, note + 3, note + 7])

    for _ in range(amount):
      new_note = random.choice(notes)
      self.lines.append([1, self.RH_time, 'Note_on_c', ch, new_note, 80])
      self.lines.append(
          [1, self.RH_time + (7 * length / 8), 'Note_off_c', ch, new_note, 0])

      self.RH_time += length

  # Hardcoded melody of "Holy is the Lord"
  # by Chris Tomlin
  def holy_is_the_lord_melody(self, key, ch):
    self.misc_time2 += 960
    self.misc_time1 += 1920
    self.LH_time += 1920
    self.RH_time += 1920

    key = key - 12

    for i in range(2):
      self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 76 + key, 80])
      self.lines.append(
          [1, self.misc_time2 + (7 * 240 / 8), 'Note_off_c', ch, 76 + key, 0])
      self.misc_time2 += 240
      self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 77 + key, 80])
      self.lines.append(
          [1, self.misc_time2 + (7 * 120 / 8), 'Note_off_c', ch, 77 + key, 0])
      self.misc_time2 += 120
      self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 76 + key, 80])
      self.lines.append(
          [1, self.misc_time2 + (7 * 240 / 8), 'Note_off_c', ch, 76 + key, 0])
      self.misc_time2 += 240
      self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 74 + key, 80])
      self.lines.append(
          [1, self.misc_time2 + (7 * 120 / 8), 'Note_off_c', ch, 74 + key, 0])
      self.misc_time2 += 120
      self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 72 + key, 80])
      self.lines.append(
          [1, self.misc_time2 + (7 * 120 / 8), 'Note_off_c', ch, 72 + key, 0])
      self.misc_time2 += 120
      self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 72 + key, 80])
      self.lines.append(
          [1, self.misc_time2 + (7 * 840 / 8), 'Note_off_c', ch, 72 + key, 0])
      self.misc_time2 += 840

      self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 79 + key, 80])
      self.lines.append(
          [1, self.misc_time2 + (7 * 480 / 8), 'Note_off_c', ch, 79 + key, 0])
      self.misc_time2 += 480
      self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 77 + key, 80])
      self.lines.append(
          [1, self.misc_time2 + (7 * 240 / 8), 'Note_off_c', ch, 77 + key, 0])
      self.misc_time2 += 240
      self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 76 + key, 80])
      self.lines.append(
          [1, self.misc_time2 + (7 * 240 / 8), 'Note_off_c', ch, 76 + key, 0])
      self.misc_time2 += 240
      self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 76 + key, 80])
      self.lines.append(
          [1, self.misc_time2 + (7 * 480 / 8), 'Note_off_c', ch, 76 + key, 0])
      self.misc_time2 += 480
      self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 74 + key, 80])
      self.lines.append(
          [1, self.misc_time2 + (7 * 1200 / 8), 'Note_off_c', ch, 74 + key, 0])
      self.misc_time2 += 1200
      self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 72 + key, 80])
      self.lines.append(
          [1, self.misc_time2 + (7 * 240 / 8), 'Note_off_c', ch, 72 + key, 0])
      self.misc_time2 += 240
      self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 76 + key, 80])
      self.lines.append(
          [1, self.misc_time2 + (7 * 720 / 8), 'Note_off_c', ch, 76 + key, 0])
      self.misc_time2 += 720

      self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 72 + key, 80])
      self.lines.append(
          [1, self.misc_time2 + (7 * 240 / 8), 'Note_off_c', ch, 72 + key, 0])
      self.misc_time2 += 240
      self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 77 + key, 80])
      self.lines.append(
          [1, self.misc_time2 + (7 * 480 / 8), 'Note_off_c', ch, 77 + key, 0])
      self.misc_time2 += 480
      self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 76 + key, 80])
      self.lines.append(
          [1, self.misc_time2 + (7 * 240 / 8), 'Note_off_c', ch, 76 + key, 0])
      self.misc_time2 += 240
      self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 72 + key, 80])
      self.lines.append(
          [1, self.misc_time2 + (7 * 240 / 8), 'Note_off_c', ch, 72 + key, 0])
      self.misc_time2 += 240
      self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 76 + key, 80])
      self.lines.append(
          [1, self.misc_time2 + (7 * 480 / 8), 'Note_off_c', ch, 76 + key, 0])
      self.misc_time2 += 480
      self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 74 + key, 80])
      self.lines.append([
          1, self.misc_time2 + (7 * (720 + (i * 480)) / 8), 'Note_off_c', ch,
          74 + key, 0
      ])
      self.misc_time2 += 720 + (i * 480)

    self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 72 + key, 80])
    self.lines.append(
        [1, self.misc_time2 + (7 * 240 / 8), 'Note_off_c', ch, 72 + key, 0])
    self.misc_time2 += 240
    self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 76 + key, 80])
    self.lines.append(
        [1, self.misc_time2 + (7 * 720 / 8), 'Note_off_c', ch, 76 + key, 0])
    self.misc_time2 += 720
    self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 72 + key, 80])
    self.lines.append(
        [1, self.misc_time2 + (7 * 240 / 8), 'Note_off_c', ch, 72 + key, 0])
    self.misc_time2 += 240
    self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 77 + key, 80])
    self.lines.append(
        [1, self.misc_time2 + (7 * 480 / 8), 'Note_off_c', ch, 77 + key, 0])
    self.misc_time2 += 480
    self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 76 + key, 80])
    self.lines.append(
        [1, self.misc_time2 + (7 * 240 / 8), 'Note_off_c', ch, 76 + key, 0])
    self.misc_time2 += 240
    self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 72 + key, 80])
    self.lines.append(
        [1, self.misc_time2 + (7 * 240 / 8), 'Note_off_c', ch, 72 + key, 0])
    self.misc_time2 += 240
    self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 76 + key, 80])
    self.lines.append(
        [1, self.misc_time2 + (7 * 480 / 8), 'Note_off_c', ch, 76 + key, 0])
    self.misc_time2 += 480
    self.lines.append([1, self.misc_time2, 'Note_on_c', ch, 74 + key, 80])
    self.lines.append(
        [1, self.misc_time2 + (7 * 1200 / 8), 'Note_off_c', ch, 74 + key, 0])
    self.misc_time2 += 1200

  # Plays a jazzy progression of both the RH and LH,
  # with similar vibes found in Holy is the Lord by
  # Chris Tomlin (not plagiarized tho)
  def jazzy_prog(self, amount, length, key, ch):
    for _ in range(amount):
      self.repeat(self.jazzy_rhythm_note_top, [60 + key, length / 2, ch],
                  3)  # RH
      self.jazzy_block_prog_1455(1, length, key, ch)  # LH
      self.jazzy_block_prog_6455(1, length, key, ch)

    self.jazzy_block_prog_6455(1, length, key, ch)

  # Full, random melody + Xavier's Theme chord progression;
  # length is one full cycle of the chord progression.
  # Recommended instruments: 89, 89, 0
  def xmen_full(self, amount, length, key, ch):
    prog = self.xmen_prog_6342(amount, length, key, ch)
    prog += 24

    for _ in range(amount):
      self.tonic_minor_melody(prog[0], 8, length / 4, ch + 1)
      self.tonic_minor_melody(prog[1], 8, length / 4, ch + 1)
      self.tonic_major_melody(prog[2], 8, length / 4, ch + 1)
      self.tonic_minor_melody(prog[3], 8, length / 4, ch + 1)

    # Original hardcoded melody of the song
    for _ in range(amount):
      notes = np.array([57, 60, 59, 57]) + key + 12
      for i in range(2):
        for note in notes:
          self.lines.append(
              [1, self.misc_time1, 'Note_on_c', ch + 2, note, 80])
          self.lines.append(
              [1, self.misc_time1 + length / 2, 'Note_off_c', ch + 2, note, 0])
          self.misc_time1 += length / 2

        # First iteration of the loop
        if i is 0:
          self.lines.append(
              [1, self.misc_time1, 'Note_on_c', ch + 2, 55 + key + 12, 80])
          self.lines.append([
              1, self.misc_time1 + length / 2, 'Note_off_c', ch + 2,
              55 + key + 12, 0
          ])
          self.misc_time1 += length / 2
          self.lines.append(
              [1, self.misc_time1, 'Note_on_c', ch + 2, 57 + key + 12, 80])
          self.lines.append([
              1, self.misc_time1 + length / 2 * 3, 'Note_off_c', ch + 2,
              57 + key + 12, 0
          ])
          self.misc_time1 += length / 2 * 3

        # Second iteration of the loop
        else:
          self.lines.append(
              [1, self.misc_time1, 'Note_on_c', ch + 2, 53 + key + 12, 80])
          self.lines.append([
              1, self.misc_time1 + length, 'Note_off_c', ch + 2, 53 + key + 12,
              0
          ])
          self.misc_time1 += length
          self.lines.append(
              [1, self.misc_time1, 'Note_on_c', ch + 2, 52 + key + 12, 80])
          self.lines.append([
              1, self.misc_time1 + length, 'Note_off_c', ch + 2, 52 + key + 12,
              0
          ])
          self.misc_time1 += length

  # Random, shuffled chords + corresponding random melody
  def random_chord_prog_full(self, amount, length, key, ch):
    prog = self.shuffled_chord_progs(amount, length, key, ch)
    prog += 24

    for note in prog:
      if note != 69 + key:
        self.tonic_major_melody(note, 4, length / 4, ch + 1)
      else:
        self.tonic_minor_melody(note, 4, length / 4, ch + 1)

    return prog

  # # Holy is the Lord chords + corresponding random melody
  # # Work in progress.
  # def random_chord_prog_full(self, amount, length, key, ch):
  #     prog = self.holy_is_the_lord_melody(amount, length, key, ch)
  #     prog += 24

  #     for note in prog:
  #         if note != 69 + key:
  #             self.tonic_major_melody(note, 4, length / 4, ch + 1)
  #         else:
  #             self.tonic_minor_melody(note, 4, length / 4, ch + 1)

  #     return prog

  # The classic arpeggio to end all arpeggios!
  def arpeg_ending(self, key, length, ch):
    self.modified_tonic_158_chord_arpeg(36 + key, length / 2, ch)
    self.RH_time += length / 2

    self.modified_tonic_158_chord_arpeg(48 + key, length / 2, ch)
    self.RH_time += length / 2

    self.ending(key, length, ch)

  # RH: Classic fast 3-5-8 arpeggio finisher
  # LH: Boring 1-8 tonic chord
  def ending(self, key, length, ch):
    self.fast_358_chord_arpeg(60 + key, length, ch)

    self.lines.append([1, self.LH_time, 'Note_on_c', ch, 36 + key, 80])
    self.lines.append([1, self.LH_time, 'Note_on_c', ch, 48 + key, 80])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, 36 + key, 0])
    self.lines.append(
        [1, self.LH_time + (7 * length / 8), 'Note_off_c', ch, 48 + key, 0])
    self.LH_time += length
