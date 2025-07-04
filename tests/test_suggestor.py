from utils.music_theory import get_possible_triads

triads = get_possible_triads(60, 'major')

for i, chord in enumerate(triands):
    print(f"Chord {i+1}: {chord}")