    // Constants
    const keyboard = document.getElementById('keyboard');
    const suggestBtn = document.getElementById('suggestBtn');
    const suggestionsBox = document.getElementById('suggestions');
    const moodSelect = document.getElementById('mood')
    const modeSelect = document.getElementById('mode');
    const rhythmMap = {
        'whole' : '1n',
        'half' : '2n',
        'quarter' : '4n',
        'eighth' : '8n',
        'sixteenth' : '16n',
        'dotted-eighth' : '8n.',
        'rest' : null
    };

    let recentNotes = [];

    // Generate simple 1-Octave Keyboard (C4 to B4)
    const baseMIDINote = 60;
    const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];

    noteNames.forEach((name, i) => {
        const key = document.createElement('div');
        key.classList.add('key');
        key.dataset.note = baseMIDINote + i;
        key.textContent = name;
        key.addEventListener('click', () => {
            const midiNote = parseInt(key.dataset.note);
            recentNotes.push(midiNote);
            if (recentNotes.length > 8) recentNotes.shift(); // Kepp only latest 8

            playNote(midiNote);
        });
        keyboard.appendChild(key);
    });

    // Playback using Tone.js
    async function playNote(midi) {
        if (Tone.context.state !== 'running'){
            await Tone.start();
            console.log('AudioContext Sarted');
        }

        const synth = new Tone.Synth().toDestination();
        const freq = Tone.Frequency(midi, 'midi').toFrequency();
        synth.triggerAttackRelease(freq, '8n');
    }

    // Suggest Button Action 
    suggestBtn.addEventListener('click', async() => {
        if (Tone.context.state !== 'running') {
            await Tone.start();
            console.log('AudioContext Started');
        }

        const mood = moodSelect.value;
        const mode = modeSelect.value;

        const response = await fetch('/suggest_context', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({recent_notes: recentNotes, mood, mode})
        });

        const data = await response.json();
        suggestionsBox.textContent = JSON.stringify(data, null, 2);

        if (data.notes) {
            for (let i = 0; i < data.notes.length; i++) {
                const noteObj = data.notes[i];
                const freq = Tone.Frequency(noteObj.pitch, 'midi').toFrequency();
                const synth = new Tone.Synth().toDestination();

                const rhythmLabel = data.rhythms[i];
                const duration = rhythmMap[rhythmLabel] || '8n';

                if (duration !== null) {
                    synth.triggerAttackRelease(freq, duration, Tone.now() + noteObj.timing_shift);
                }
            }
        }
    });