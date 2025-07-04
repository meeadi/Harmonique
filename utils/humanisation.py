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