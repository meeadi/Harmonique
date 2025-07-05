from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from model.suggestor import suggest_notes, suggest_notes_context
from utils.music_theory import get_possible_triads, get_seventh_chords, get_cadence_chords, get_triad, build_scales
from utils.voice_leading import apply_voice_leading
from utils.humanisation import humanize_note

app = Flask(__name__, static_folder='static', template_folder='.')
CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})

# Home Route
@app.route('/')

def index():
    return render_template('static/index.html')

# Suggestion Route
@app.route('/suggest', methods=['POST'])

def suggest():
    data = request.get_json() # Receives JSON input from frontend or curl
    note = data.get('note', 60) # Defaults to C4 if no note provided
    mood = data.get('mood', "nostalgic") # Defaults to happy mood
    suggestions = suggest_notes(note, mood) # Call the Note Suggestion
    return jsonify({'suggestions' : suggestions})

# Contextual Suggestion Route
@app.route('/suggest_context', methods=['POST'])

def suggest_context():
    data = request.get_json()
    recent_notes = data.get('recent_notes', [])
    mood = data.get('mood', 'happy')
    scale = data.get('mode', 'major')

    suggestions = suggest_notes_context(recent_notes, mood, scale)
    return jsonify(suggestions)

# Triad Route
@app.route('/triads', methods=['POST'])

def triads():
    data = request.get_json()
    key_root = data.get('key_root', 60)
    scale_type = data.get('scale_type', 'major')

    chords = get_possible_triads(key_root, scale_type)
    return jsonify({'triads' : chords})

# Seventh Chord Route
@app.route('/sevenths', methods=['POST'])

def sevenths():
    data = request.get_json()
    key_root = data.get('key_root', 60)
    scale_type = data.get('scale_type', 'major')

    chords = get_seventh_chords(key_root, scale_type)
    return jsonify({'sevenths' : chords})

# Voice Leading Route
@app.route('/voice_leading', methods=['POST'])

def voice_leading_route():
    data = request.get_json()
    key_root = data.get('key_root', 60)
    scale_type = data.get('scale_type', 'major')

    chords = get_possible_triads(key_root, scale_type)
    voiced_chords = apply_voice_leading(chords, key_root)
    return jsonify({'voiced_chords' : voiced_chords})

# Cadence Route
@app.route('/cadence', methods=['POST'])

def cadence():
    data = request.get_json()
    key_root = data.get('key_root', 60)
    scale_type = data.get('scale_type', 'major')

    chords = get_cadence_chords(key_root, scale_type)
    return jsonify({'cadence': chords})

# Test Endpoint for Debugging
@app.route('/ping')

def ping():
    return jsonify({'message': 'pong'})


if __name__ == '__main__':
    app.run(debug=True)