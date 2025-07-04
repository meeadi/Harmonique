import random
from utils.music_theory import EMOTION_MODIFIERS, generate_rhythm_pattern, get_scale_notes
from utils.humanisation import apply_velocity, apply_timing_shift, get_articulation

def suggest_notes_context(recent_notes: list, mood: str, scale: str) -> dict:
    if not recent_notes:
        recent_notes = [60]

    last_note = recent_notes[-1]
    modifiers = EMOTION_MODIFIERS.get(mood.lower(), [2, 4, 7])
    suggestions = [(last_note + interval) % 12 for interval in modifiers]

    enriched_notes = []

    for note in suggestions:
        enriched_notes.append({
            'pitch' : note, 
            'velocity' : apply_velocity(mood),
            'timing_shift' : apply_timing_shift(mood),
            'articulation' : get_articulation(mood)
        })

    rhythms = generate_rhythm_pattern(mood, len(enriched_notes))

    return {
        'notes' : enriched_notes, 
        'rhythms' : rhythms
    }

def suggest_notes(note: int, mood: str = 'happy') -> list:
    base_note = note % 12
    modifiers = EMOTION_MODIFIERS.get(mood.lower(), [2, 4, 7])
    suggestions = [(note + interval) % 128 for interval in modifiers]

    return suggestions