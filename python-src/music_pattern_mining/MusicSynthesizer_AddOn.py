import pysynth as ps

def pysynth_synthesize_notes(virtual_piano_notes,duration,filename):
    notes_sequences=[]
    for n in virtual_piano_notes:
        note=[n.lower(), duration] 
        notes_sequences.append(note)
    print("notes_sequences:",notes_sequences)
    notestuple=tuple([tuple(x) for x in notes_sequences])
    print("notes tuple:",notestuple)
    ps.make_wav(notestuple, fn=filename)

if __name__=="__main__":
    pysynth_synthesize_notes(virtual_piano_notes=['C','C','G','G','A','A','G','F','F','E','E','D','D','C','G','G','F','F','E','E','D','G','G','F','F','E','E','D','C','C','G','G','A','A','G','F','F','E','E','D','D','C','C','C','G','G','A','A','G','F','F','E','E','D','D','C','G','G','F','F','E','E','D','G','G','F','F','E','E','D','C','C','G','G','A','A','G','F','F','E','E','D','D','C'],duration=4,filename="PySynth_music.wav")
    #pysynth_synthesize_notes((('c', 4), ('c*', 4), ('eb', 4), ('g#', 4),  ('g*', 2), ('g5', 4), ('g5*', 4), ('r', 4), ('e5', 16), ('f5', 16),  ('e5', 16),  ('d5', 16), ('e5*', 4)),filename="PySynth_music.wav")
