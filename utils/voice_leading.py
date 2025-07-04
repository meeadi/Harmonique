def apply_voice_leading(chord_progression, start_root=60):
    voiced_progression = []
    previous_chord = []

    for i, chord in enumerate(chord_progression):
        voiced_chord = []

        for note in chord:
            base_note = (start_root // 12) * 12 + note

            while base_note < start_root:
                base_note += 12

            if previous_chord:
                distances = []
                for prev in previous_chord:
                    options = [base_note - 12, base_note, base_note + 12]
                    best = min(options, key = lambda x: abs(x - prev))
                    distances.append(best)
                base_note = min(distances, key = lambda x: abs(x - base_note))

            voiced_chord.append(base_note)

        voiced_chord = sorted(voiced_chord)
        voiced_progression.append(voiced_chord)
        previous_chord = voiced_chord

    return voiced_progression