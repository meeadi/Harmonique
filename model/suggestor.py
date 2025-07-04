import random
from utils.music_theory import EMOTION_MODIFIERS, generate_rhythm_pattern, get_scale_notes, build_scales
from utils.humanisation import apply_velocity, apply_timing_shift, get_articulation, humanize_note, adjust_octave

def weighted_interval_choice(modifiers: list[int]) -> int:
    weights = {
        1: 1.0, 2: 1.2, 3: 1.5, 4: 1.3, 5: 1.4, 6: 1.1,
        7: 1.6, 8: 1.2, 9: 1.1, 10: 1.3, 11: 1.0
    }

    weighted_pool = []
    for interval in modifiers: 
        weighted_pool.extend([interval] * int(weights.get(interval, 1.0) * 10))
    
    return random.choice(weighted_pool)

def suggest_notes_context(recent_notes, mood, mode):
    if not recent_notes:
        return {'notes': [], 'rhythms': []}

    last_note = recent_notes[-1]
    scale = build_scales(last_note % 12, mode)

    emotion_intervals = EMOTION_MODIFIERS.get(mood.lower(), [2, 4, 7])
    selected = []

    for _ in range(min(3, len(scale))):
        interval = weighted_interval_choice(emotion_intervals)
        pitch = (last_note + interval) %  12
        selected.append(pitch)
    
    rhythms = generate_rhythm_pattern(mood, len(selected))

    history = recent_notes or []
    humanized = []

    for pitch in selected:
        adjusted_pitch = adjust_octave(pitch + last_note, mood, history)
        note_data = humanize_note(adjusted_pitch, mood)
        note_data['pitch'] = adjusted_pitch
        humanized.append(note_data)
        history.append(adjusted_pitch)

    return {
        'notes': humanized,
        'rhythms': rhythms
    }

def suggest_notes(note: int, mood: str = 'happy') -> list:
    base_note = note % 12
    modifiers = EMOTION_MODIFIERS.get(mood.lower(), [2, 4, 7])
    suggestions = [(note + interval) % 128 for interval in modifiers]

    return suggestions