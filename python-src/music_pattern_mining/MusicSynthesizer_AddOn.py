import tomita.legacy.pysynth as ps
import pretty_midi
from scipy.io.wavfile import write

def signalflow_synthesize_notes(oscillator="Sine",nvelop="ADSR",maxiterations=100):
    from signalflow import AudioGraph,Envelope,SineOscillator,ADSREnvelope 
    n=0
    graph = AudioGraph()
    while n < maxiterations:
        if nvelop=="ADSR":
            gate = Envelope([1, 1, 0], [0.2, 0])
            envelope = ADSREnvelope(0.1, 0.1, 0.5, 0.05, gate=gate)
        if oscillator=="Sine":
            sine = SineOscillator([440, 880])
            output = sine * envelope
            print("output:",output)
            output.play()
        n+=1

def pysynth_synthesize_notes(virtual_piano_notes,duration,filename):
    notes_sequences=[]
    for n in virtual_piano_notes:
        note=[n.lower(), duration] 
        notes_sequences.append(note)
    print("notes_sequences:",notes_sequences)
    notestuple=tuple([tuple(x) for x in notes_sequences])
    print("notes tuple:",notestuple)
    ps.make_wav(notestuple, fn=filename)

def pretty_midi_synthesize_notes(virtual_piano_notes=[],instrument_name="SynthDrum",veloCT=200,notesuffix="1",per_note_duration=0.1,filename="PrettyMIDI_music.wav",samplerate=44100,filetype="wav"):
    c_chord = pretty_midi.PrettyMIDI()
    program = pretty_midi.instrument_name_to_program(instrument_name)
    percussion = pretty_midi.Instrument(program=program)
    s=0
    e=per_note_duration
    for note_name in virtual_piano_notes:
        print("note_name:",note_name+notesuffix)
        note_number = pretty_midi.note_name_to_number(note_name+notesuffix)
        print("note_number:",note_number)
        note = pretty_midi.Note(velocity=veloCT, pitch=note_number, start=s, end=e)
        print("MIDI note:",note)
        percussion.notes.append(note)
        s=s+per_note_duration
        e=e+per_note_duration
    c_chord.instruments.append(percussion)
    c_chord.remove_invalid_notes()
    musicsynth=c_chord.synthesize()
    print("musicsynth:",musicsynth)
    if filetype=="wav":
        write(filename, samplerate, musicsynth)
    if filetype=="MIDI":
        c_chord.write(filename)

if __name__=="__main__":
    signalflow_synthesize_notes()
    pysynth_synthesize_notes(virtual_piano_notes=['C','C','G','G','A','A','G','F','F','E','E','D','D','C','G','G','F','F','E','E','D','G','G','F','F','E','E','D','C','C','G','G','A','A','G','F','F','E','E','D','D','C','C','C','G','G','A','A','G','F','F','E','E','D','D','C','G','G','F','F','E','E','D','G','G','F','F','E','E','D','C','C','G','G','A','A','G','F','F','E','E','D','D','C'],duration=4,filename="PySynth_music.wav")
    pretty_midi_synthesize_notes(virtual_piano_notes=['C','C','G','G','A','A','G','F','F','E','E','D','D','C','G','G','F','F','E','E','D','G','G','F','F','E','E','D','C','C','G','G','A','A','G','F','F','E','E','D','D','C','C','C','G','G','A','A','G','F','F','E','E','D','D','C','G','G','F','F','E','E','D','G','G','F','F','E','E','D','C','C','G','G','A','A','G','F','F','E','E','D','D','C'],filename="PrettyMIDI_music.wav")
    #pysynth_synthesize_notes((('c', 4), ('c*', 4), ('eb', 4), ('g#', 4),  ('g*', 2), ('g5', 4), ('g5*', 4), ('r', 4), ('e5', 16), ('f5', 16),  ('e5', 16),  ('d5', 16), ('e5*', 4)),filename="PySynth_music.wav")
