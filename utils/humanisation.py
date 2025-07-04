import random

def apply_velocity(mood: str) -> int:
    base = {
        'happy' : 90,
        'sad' : 60,
        'tense' : 70,
        'relaxed' : 75,
        'nostalgic' : 65,
        'epic' : 95,
        'dark' : 50,
        'hopeful' : 80
    }.get(mood.lower(), 80)

    return base + random.randint(-10, 10)

def apply_timing_shift(mood: str) -> float:
    swing = {
        'happy' : 0.05,
        'sad' : 0.02,
        'tense' : 0.08,
        'relaxed' : 0.04,
        'nostalgic' : 0.03,
        'epic' : 0.06,
        'dark' : 0.07,
        'hopeful' : 0.04
    }.get(mood.lower(), 0.03)

    return round(random.uniform(-swing, swing), 3)

def get_articulation(mood: str) -> str:
    if mood in ['sad', 'nostalgic']:
        return 'legato'
    elif mood in ['tense', 'dark']:
        return 'staccato'
    else:
        return 'normal'

def humanize_note(pitch: int, mood: str) -> dict:
    return {
        'pitch' : pitch,
        'velocity' : apply_velocity(mood),
        'timing_shift' : apply_timing_shift(mood),
        'articulation' : get_articulation(mood)
    }

def adjust_octave(pitch: int, mood: str, history: list[int]) -> int:
    shift = 0

    if mood in ['epic', 'hopeful'] and pitch < 65:
        shift = 12 # Higher Octave
    elif mood in ['dark', 'nostalgic'] and pitch > 72:
        shift = -12 # Lower Octave
    elif len(history) >= 3:
        avg = sum(history[-3:]) / 3
        if pitch > avg + 4:
            shift = -12
        else:
            shift = 12

    return pitch + shift