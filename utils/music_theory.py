import random

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

EMOTION_MODIFIERS = { # Defining which interval feels appropriate for each mood
    'happy' : [2, 4, 7],
    'sad' : [3, 5, 8],
    'tense' : [1, 6, 10],
    'relaxed' : [2, 5, 9],
    'nostalgic' : [3, 7, 10],
    'dark' : [1, 6, 11],
    'hopeful' : [2, 5, 9]
}

MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]
MINOR_SCALE = [0, 2, 3, 5, 7, 8, 10]

CHORD_FORMULAS = { # Useful for for suggesting Triads or detect them
    'major' : [0, 4, 7,],
    'minor' : [0, 3, 7],
    'diminished' : [0, 3, 6]
}

TRIAD_TYPES = {
    "major" : ['major', 'minor', 'minor', 'major', 'major', 'minor', 'diminished'],
    "minor" : ['minor', 'diminished', 'major', 'minor', 'minor', 'major', 'major']
}

RHYTHM_LIBRARY = {
    'happy' : ['eighth', 'quarter', 'quarter', 'eighth'],
    'sad' : ['half', 'whole', 'rest', 'half'],
    'nostalgic' : ['quarter', 'rest', 'eighth', 'half'],
    'epic' : ['quarter', 'quarter', 'half', 'quarter'],
    'playful' : ['eighth', 'dotted_eighth', 'rest', 'quarter']
}

# Scale Logic
def build_scales(root: int, scale_type: str) -> list:
    if scale_type == 'major':
        intervals = MAJOR_SCALE
    elif scale_type == 'minor':
        intervals = MINOR_SCALE
    else:
        raise ValueError(f"Unsupported scale type: {scale_type}")

    return [(root + i) % 12 for i in intervals]

def get_scale_notes(root: int, scale_type: str) -> list:
    return build_scales(root, scale_type)

# Chord Logic
def get_triad(root_note: int, chord_type: str) -> list:
    return [(root_note + interval) % 12 for interval in CHORD_FORMULAS[chord_type]]

def get_possible_triads(key_root: int=60, scale_type: str='major') -> list:
    scale = build_scales(key_root % 12, scale_type)
    triads = []

    for i, degree in enumerate(scale):
        chord_type = TRIAD_TYPES[scale_type][i]
        triad = get_triad(degree, chord_type)
        triads.append(triad)

    return triads

def get_seventh_chords(key_root: int, scale_type: str='major') -> list:
    scale = build_scales(key_root, scale_type)
    seventh_chords = []

    for i in range(7):
        root = scale[i]
        third = scale[(i + 2) % 7]
        fifth = scale[(i + 4) % 7]
        seventh = scale[(i + 6) % 7]
        chord = [root % 12, third % 12, fifth % 12, seventh % 12]
        seventh_chords.append(chord)

    return seventh_chords

# Rhythm Logic
def generate_rhythm_pattern(mood: str, length: int) -> list:
    mood = mood.lower()
    pattern = RHYTHM_LIBRARY.get(mood, ['quarter'] * length)
    return [random.choice(pattern) for _ in range(length)]

# Utility
def get_note_name(note: int) -> str:
    return NOTE_NAMES[note % 12]

def note_number_to_name_list(notes: list) -> list:
    return [get_note_name(n) for n in notes]

# Cadence Logic
def get_cadence_chords(key_root: int, scale_type: str = 'major') -> list:
    scale = build_scales(key_root % 12, scale_type)

    if scale_type == 'major':
        
        return [
            get_triad(scale[0], 'major'), # I
            get_triad(scale[3], 'major'), # IV
            get_triad(scale[4], 'major'), # V
            get_triad(scale[0], 'major'), # I again
            get_triad(scale[1], 'minor'), # ii
            get_triad(scale[4], 'major'), # V
            get_triad(scale[0], 'major') # I
        ]
    
    else:

        return [
            get_triad(scale[0], 'minor'), # i
            get_triad(scale[3], 'minor'), # iv
            get_triad(scale[4], 'minor'), # v
            get_triad(scale[0], 'minor') # i again
        ]