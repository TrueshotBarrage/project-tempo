from music import Music


def test(s):
  s.minor_135_chord(60, 1920)
  s.major_135_chord_inv1(60, 960)
  s.major_15_chord_inv2(60, 960)


# Actual contents of the song!
# Edit this method to customize the settings
# for the song you want to make.
def main():
  song = Music(0)
  song.start()
  # song.random_block_chords(10, 1920, 0)
  # song.block_prog_1465(4, 1920, 0, 0)
  # song.tonic_arpeg_prog_1465(4, 1920, 9, 0)

  # song.holy_is_the_lord_melody(9, 2)
  # song.jazzy_prog(4, 1920, 9, 1)

  # song.arpeg_ending(9, 1920, 3)

  # song.xmen_full(2, 1920, 0, 0)
  # song.random_chord_prog_full(6, 1920, 0, 0)

  test(song)
  song.finish("example")


if __name__ == "__main__":
  main()
