import random
from collections import Counter
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
    full_history = recent_notes[-8:] # Sequence Memory

    # Count Frequency of notes to avoid overuse
    frequency_counter = Counter([n % 12 for n in full_history])

    # Select top 5 least used notes and sample from them
    sorted_scale = sorted(scale, key = lambda n: frequency_counter.get(n, 0)) # Less used notes First
    bias_candidates = sorted_scale[:5] if len (sorted_scale) >= 5 else sorted_scale

    emotion_intervals = EMOTION_MODIFIERS.get(mood.lower(), [2, 4, 7])
    selected = []
    attempts = 0

    while len(selected) < 3 and attempts < 20:
        interval = weighted_interval_choice(emotion_intervals)
        raw_pitch = (last_note + interval) % 12

        if raw_pitch in bias_candidates and raw_pitch not in selected:
            selected.append(raw_pitch)

        attempts += 1

    # Fall back to random scale notes if nothing valid found
    if not selected:
        selected = random.sample(bias_candidates, min(3, len(bias_candidates)))

    rhythms = generate_rhythm_pattern(mood, len(selected))

    history = recent_notes.copy()
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