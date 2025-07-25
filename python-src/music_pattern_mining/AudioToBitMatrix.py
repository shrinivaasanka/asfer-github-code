# -------------------------------------------------------------------------------------------------------
# NEURONRAIN ASFER - Software for Mining Large Datasets
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------------------------------
# K.Srinivasan
# NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
# Personal website(research): https://acadpdrafts.readthedocs.io/en/latest/
# --------------------------------------------------------------------------------------------------------

import librosa
import librosa.display
import math
import numpy
import matplotlib.pyplot as plt
import numpy as np
from numpy import polyfit
from scipy.io.wavfile import write
import ast
from sklearn.preprocessing import scale
from scipy.spatial.distance import directed_hausdorff
from scipy.stats import wasserstein_distance
#from RecursiveLambdaFunctionGrowth import RecursiveLambdaFunctionGrowth
import sys
import random
import MinimumDescLength
from scipy.interpolate import barycentric_interpolate 
from collections import defaultdict
from IPython.display import Audio
import mir_eval.sonify
from playsound import playsound
from MultiFractals import music_mfdfa_model
import rstr
import re
from MusicWeightedAutomaton import music_weighted_automaton,audio_to_notes_samples
from splearn.datasets.data_sample import SplearnArray
from GraphMining_GSpan import GSpan
import networkx as nx
from networkx.drawing.nx_pydot import read_dot
from networkx.algorithms.shortest_paths.generic import shortest_path
from music21 import stream,instrument,environment
from music21.note import Note
from music21.tempo import MetronomeMark
from hurst import compute_Hc,random_walk
import os
from threading import Thread 
import time
from pydub import AudioSegment
from pydub.playback import play
from pytimbre2.audio_files.wavefile import WaveFile
from pytimbre2.spectral.spectra import SpectrumByFFT
from MusicSynthesizer_AddOn import pysynth_synthesize_notes,pretty_midi_synthesize_notes


# states2notes_machine={'s1-s2':'C','s2-s1':'E','s2-s3':'D','s3-s2':'G','s3-s4':'E','s4-s5':'F','s1-s3':'G','s4-s6':'A','s5-s6':'B','s4-s3':'F','s6-s5':'E','s3-s6':'A','s6-s1':'B'}
piano_notes={"WesternClassical":{'A':440,'B':493.89,'C':261.63,'D':293.67,'E':329.63,'F':349.23,'G':392,'A♯':466.17,'C♯':227.18,'D♯':311.13,'F♯':370,'G♯':415.31},"Carnatic":{'S':240, 'R₁':254.27, 'R₂':269.39, 'R₃':275,'G₁':285.41, 'G₂':302.38, 'G₃':311, 'M₁':320.36, 'M₂':339.41, 'P':359.60, 'D₁':380.98, 'D₂':403.63, 'D₃':415, 'N₁':425,'N₂':453.06, 'N₃':480}}


def all_12notes_melodies(iterations=10,number_of_notes=10,keynotes=88,tempo=0.25,musicgenre="WesternClassical"):
    global piano_notes
    if keynotes==88:
        twelvenotes=librosa.key_to_notes("C:maj") + librosa.key_to_notes("A:min") + librosa.key_to_notes("A#:min") + librosa.key_to_notes("G#:maj") + librosa.key_to_notes("Fb:min")
    if keynotes==12:
        twelvenotes=list(piano_notes[musicgenre].keys())
    print("twelvenotes:",twelvenotes)
    if musicgenre=="Carnatic":
        notes=[]
        for m in range(1,72):
            melanotes = np.asarray(librosa.mela_to_svara(m))
            for n in melanotes:
                notes.append(n)
        print("Carnatic notes:",notes)
        randnotes = np.random.choice(notes,number_of_notes) 
        music_synthesis(virtual_piano_notes=randnotes,tempo=tempo,musicgenre="Carnatic")
    if musicgenre=="WesternClassical":
        for it in range(iterations):
            randnotes = np.random.choice(twelvenotes, number_of_notes)
            music_synthesis(virtual_piano_notes=randnotes,tempo=tempo,musicgenre=musicgenre)

def audio_to_bitmatrix(audio, dur=None, binary=False):
    bitmap = []
    if binary == False:
        if dur is not None:
            waveform, srate = librosa.load(audio, duration=dur)
        input_audio_array = numpy.asarray(waveform).tolist()
        for r in input_audio_array:
            bitmap.append(r)
    else:
        if dur is not None:
            waveform, srate = librosa.load(
                audio, dtype=numpy.int64, duration=dur)
        input_audio_array = numpy.asarray(waveform).tolist()
        for r in input_audio_array:
            bitmap.append(bin(r))

    # print "audio_to_bitmatrix() for - ",audio,":",bitmap
    return (bitmap, waveform, srate)


def dynamic_time_warping(waveform1, waveform2):
    m = len(waveform1)
    n = len(waveform2)
    print(("dynamic_time_warping(): m = ", m))
    print(("dynamic_time_warping(): n = ", n))
    dtw = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            dtw[i, j] = sys.maxsize
    dtw[0, 0] = 0
    for i in range(1, m-1):
        for j in range(1, n-1):
            cost = abs(waveform1[i] - waveform2[j])
            print(("cost:", cost))
            dtw[i, j] = cost + min([dtw[i-1, j], dtw[i, j-1], dtw[i-1, j-1]])
            #print("i=",i,";j=",j,";dtw[i,j] = ", dtw[i, j])
    return dtw[m-2, n-2]


def audio_distance(audio1, audio2, dur=10, dtw=True):
    bitmap1, waveform1, srate1 = audio_to_bitmatrix(audio1, dur)
    bitmap2, waveform2, srate2 = audio_to_bitmatrix(audio2, dur)
    print(("waveform1:", waveform1))
    print(("waveform2:", waveform2))
    hausdorff_distance = directed_hausdorff([waveform1], [waveform2])
    emd_distance = wasserstein_distance(waveform1, waveform2)
    print(("Hausdorff Distance similarity between two audio waveforms:",
          hausdorff_distance))
    print(("Earth Mover Distance similarity between two audio waveforms:", emd_distance))
    if dtw:
        dtwdistance = dynamic_time_warping(waveform1, waveform2)
        print(("Dynamic Time Warping distance between two audio waveforms:", dtwdistance))
        return dtw
    return (hausdorff_distance, emd_distance)


def speechrecognition_audiograph(audiofile):
    import speech_recognition as spreg
    recog = spreg.Recognizer()
    with spreg.AudioFile(audiofile) as audiosource:
        audiodata = recog.record(audiosource)
    recogspeech = recog.recognize_sphinx(audiodata)
    print(("Recognized Speech:", recogspeech))
    print("Graph Tensor Neuron Network Merit of Recognized Speech:")
    rlfg = RecursiveLambdaFunctionGrowth()
    rlfg.grow_lambda_function3(recogspeech)


def audio_features(audiofilename=None,signal_bitmap=None,frame_size=1024,hop_length=256,timbreaveragefeatures=False):
    print("################################################")
    print("Histogram/Probability Distribution of the audio signal")
    print("################################################")
    hist, bin = np.histogram(signal_bitmap[0], density=True)
    print(("hist:", hist))
    print(("bin:", bin))
    # plt.hist(signal_bitmap, color='r', range=(0, 0.2), alpha=0.5, bins=20)
    # plt.show()
    print("#################################################")
    print("Note Onset Detection")
    print("#################################################")
    onstrength = librosa.onset.onset_strength(
        y=signal_bitmap[1], sr=signal_bitmap[2])
    times = librosa.frames_to_time(
        np.arange(len(onstrength)), sr=signal_bitmap[2])
    onset_frames = librosa.onset.onset_detect(
        onset_envelope=onstrength, sr=signal_bitmap[2])
    print(("Notes onsets occur at:", onset_frames))
    print("################################################")
    print("Timbre and Envelope")
    print("################################################")
    envelope=[]
    for x in range(0,len(signal_bitmap),hop_length):
        frame=signal_bitmap[0][x:x+frame_size]
        maxframe=max(frame)
        envelope.append(maxframe)
    print("Envelope :",envelope)
    #plt.plot(len(envelope),envelope)
    wfm = WaveFile(audiofilename)
    print("PyTimbre2 - Amplitude Modulation:",wfm.amplitude_modulation)
    spectrum = SpectrumByFFT(wfm)
    print("PyTimbre2 - Spectral roll off:",spectrum.spectral_roll_off)
    if timbreaveragefeatures:
        print("PyTimbre2 - Average Features:",spectrum.get_average_features())
    #plt.show()
    return (hist, bin, times, onstrength, onset_frames, envelope, wfm.amplitude_modulation, spectrum)

def audio_to_notes(audio, dur=1, music="Carnatic",raaga="chitrambari"):
    print("###################################################")
    print("Audio to Notes")
    print("###################################################")
    waveform, srate = librosa.load(audio, duration=dur)
    print(("raw waveform:", waveform))
    music_polynomial = polyfit(list(range(len(waveform))), waveform, 5)
    print(("polynomial learnt from raw audio-music waveform:", music_polynomial))
    freq = np.abs(librosa.stft(waveform))
    print(("Frequencies:", freq))
    try:
        if music == "Carnatic":
            index = librosa.list_mela()
            print(index)
            notes = librosa.hz_to_svara_c(freq,Sa=66,mela=raaga)
            print(("Carnatic Notes:", notes))
            return notes
        if music == "Hindustani":
            notes = librosa.hz_to_svara_h(freq)
            print(("Hindustani Notes:", notes))
            return notes
        else:
            notes = librosa.hz_to_note(freq)
            print(("Notes:", notes))
            return notes
    except Exception as e:
        print("Exception in librosa - hertz-to-note")

def get_piano_frequencies(virtual_piano_notes,genre="WesternClassical"):
    global piano_notes
    piano_freq=[]
    for n in virtual_piano_notes:
        if genre == "WesternClassical":
            piano_freq.append(piano_notes[genre][n])
        if genre == "Carnatic":
            piano_freq.append(piano_notes[genre][n])
    if len(piano_freq) > 100:
        H, c, data = compute_Hc(piano_freq)
        print("Hurst exponent of notes timeseries:",H)
        print("Hurst constant of notes timeseries:",c)
    return piano_freq

def percussion_synthesis(virtual_piano_notes=None,percussions=["Saxophone","Guitar","Trumpet","Violin","SteelDrum","Flute","BassDrum","TenorDrum"],tempo=2000):
    environment.set("midiPath","/usr/bin/musescore")
    score=stream.Score()
    for percussion in percussions:
        percussionpart = stream.Part()
        if percussion == "Saxophone":
             percussionpart.insert(0, instrument.Saxophone())
        if percussion == "SteelDrum":
             percussionpart.insert(0, instrument.SteelDrum())
        if percussion == "Flute":
             percussionpart.insert(0, instrument.Flute())
        if percussion == "BassDrum":
             percussionpart.insert(0, instrument.BassDrum())
        if percussion == "TenorDrum":
             percussionpart.insert(0, instrument.TenorDrum())
        if percussion == "Violin":
             percussionpart.insert(0, instrument.Violin())
        if percussion == "Trumpet":
             percussionpart.insert(0, instrument.Trumpet())
        if percussion == "Guitar":
             percussionpart.insert(0, instrument.Guitar())
        percussionmeasure = stream.Measure()
        percussionmeasure.append(MetronomeMark(number=tempo)) 
        for note in virtual_piano_notes:
            n=Note(note,type='whole')
            percussionmeasure.append(n)
        percussionpart.append(percussionmeasure)
        score.insert(0,percussionpart)
    score.show("text",addEndTimes=True)
    score.write('midi',"./music21_percussion_for_piano.midi")
    os.system("cat /dev/null > ./music21_percussion_for_piano.wav")
    os.system("fluidsynth -ni /usr/share/fluidr3mono-gm-soundfont/FluidR3Mono_GM.sf3 ./music21_percussion_for_piano.midi -F ./music21_percussion_for_piano.wav -r 44100")
    #playsound("./music21_percussion_for_piano.wav")

def music_synthesis(training_music=None,dur=5,samplerate=44100,polynomial_interpolation=True,polyfeatures=False,virtual_piano_notes=None,tempo=1,amplitude=4096,musicgenre="WesternClassical",musicwfa_notes_weights=None,playsynthesis=False,addon_synthesizers=["Pretty-MIDI"]):
    music_interpol_poly=[]
    synthesized_poly=0
    if training_music is None and virtual_piano_notes is not None:
        print("virtual piano notes:",virtual_piano_notes)
        for addon_synthesizer in addon_synthesizers:
            if addon_synthesizer == "PySynth":
                pysynth_synthesize_notes(virtual_piano_notes,duration=0.25,filename="PySynth_music.wav")
            if addon_synthesizer == "Pretty-MIDI":
                pretty_midi_synthesize_notes(virtual_piano_notes,instrument_name="Steel Drums",veloCT=100,filename="pretty_midi_music.midi",filetype="MIDI")
                os.system("fluidsynth -ni /usr/share/fluidr3mono-gm-soundfont/FluidR3Mono_GM.sf3 ./pretty_midi_music.midi -F ./pretty_midi_music.wav -r 44100")
        #freq=librosa.note_to_hz(virtual_piano_notes)
        freq=get_piano_frequencies(virtual_piano_notes,genre=musicgenre)
        print("freq:",freq)
        #audio=mir_eval.sonify.pitch_contour(librosa.times_like(freq),freq,samplerate,amplitudes=amps)
        audio=[]
        fqcnt=0
        for fq in freq:
            print("frequency:",abs(fq))
            signal = librosa.tone(abs(fq),duration=tempo)
            print("signal:",signal)
            #amps=np.arange(len(signal))
            #amps.fill(2*np.iinfo(np.int16).max)
            #signal=mir_eval.sonify.pitch_contour(librosa.times_like(signal),signal,samplerate/100,amplitudes=amps)
            print("length of signal:",len(signal))
            #print("length of amplitudes:",len(amps))
            n=0
            amps=np.arange(len(signal))
            #amps.fill(2*np.iinfo(np.int16).max)
            #if musicwfa_notes_weights is not None:
            #    amps.fill((musicwfa_notes_weights[fqcnt] + 1)*amplitude)
            #else:
            amps.fill(amplitude)
            #amps=np.iinfo(np.int16).max*2*np.random.random_sample(len(signal))
            for s in signal:
                 audio.append(amps[n]*s) 
                 n +=1
            fqcnt+=1
        audio=np.asarray(audio)
        #audio=np.concatenate(audio)
        #print("Synthesized audio:",audio)
        #plt.figure(figsize=(14, 5))
        if musicgenre=="WesternClassical":
            write("virtual_piano_music.WesternClassical.wav", samplerate, audio.astype(np.int16))
            if playsynthesis == True:
                playsound("virtual_piano_music.WesternClassical.wav")
        if musicgenre=="Carnatic":
            write("virtual_piano_music.Carnatic.wav", samplerate, audio.astype(np.int16))
            if playsynthesis == True:
                playsound("virtual_piano_music.Carnatic.wav")
        #waveform, srate = librosa.load("virtual_piano_music.wav")
        #librosa.display.waveshow(waveform)
        #plt.show()
        return
    if polynomial_interpolation:
        for music in training_music:
           waveform, srate = librosa.load(music, duration=dur)
           x_points = list(range(len(waveform))) 
           print("x_points:",len(x_points))
           y_points = waveform
           print("y_points:",len(y_points))
           #x = np.linspace(min(x_points),max(x_points),10)
           #interpol = barycentric_interpolate(x_points,y_points,x)
           if not polyfeatures:
                intpoly = polyfit(x_points,y_points,5) 
           else:
                spectra=np.abs(librosa.stft(waveform))
                interpol=librosa.feature.poly_features(S=spectra,order=5)
                fig, ax = plt.subplots(nrows=5, sharex=True, figsize=(8, 8))
                times=librosa.times_like(interpol)
                librosa.display.waveplot(waveform, srate, alpha=0.8)
                ax[0].plot(times, interpol[0], label='order=5', alpha=0.8)
                ax[1].plot(times, interpol[1], label='order=5', alpha=0.8)
                ax[2].plot(times, interpol[2], label='order=5', alpha=0.8)
                ax[3].plot(times, interpol[3], label='order=5', alpha=0.8)
                ax[4].plot(times, interpol[4], label='order=5', alpha=0.8)
                plt.show()
                print("times:",len(times))
                print("Librosa poly_features() - Interpolated Degree 5 polynomial learnt from music waveform:",interpol[4])
                intpoly = polyfit(times,interpol[4],5) 
           music_interpol_poly.append(intpoly)
        for interpol in music_interpol_poly:
           synthesized_poly += interpol
        synth_poly_string=""
        degree=0
        for monomial in synthesized_poly:
            synth_poly_string += str(monomial*np.iinfo(np.int16).max) + "*math.pow(x,"+str(degree)+")+"
            degree += 1
        print("Synthesized music polynomial:",synth_poly_string)
        notes_to_audio(function=synth_poly_string[:len(synth_poly_string)-1], fractal=False, periodicity=100)
    else:
        synth_notes_freq=defaultdict()
        synth_music=[]
        minnoteslength=np.iinfo(np.int16).max
        for m in training_music:
            synth_notes_freq[m] = get_piano_frequencies(virtual_piano_notes=audio_to_notes(m,music=musicgenre),genre=musicgenre)
        iterations=dur
        print("iterations:",iterations)
        for it in range(iterations):
            synthslice=int(dur/20)
            randindex1=random.randint(0,len(training_music)-1)
            randindex2=random.randint(0,len(training_music[randindex1])-synthslice)
            frequencies=synth_notes_freq[training_music[randindex1]][randindex2-synthslice:randindex2+synthslice]
            print("frequencies:",frequencies)
            for frequency in frequencies:
                signal = librosa.tone(frequency,duration=tempo)
                print("signal:",signal)
                n=0
                amps=np.arange(len(signal))
                amps.fill(amplitude)
                for s in signal:
                   synth_music.append(amps[n]*s) 
                   n +=1
        npsynth = np.asarray(synth_music)
        if musicgenre=="WesternClassical":
            write("virtual_piano_music.WesternClassical.wav", samplerate, npsynth.astype(np.int16))
            if playsynthesis:
                playsound("virtual_piano_music.WesternClassical.wav")
        if musicgenre=="Carnatic":
            write("virtual_piano_music.Carnatic.wav", samplerate, npsynth.astype(np.int16))
            if playsynthesis:
                playsound("virtual_piano_music.Carnatic.wav")

def notes_to_audio(automaton=False, function=None, deterministic=True, samplerate=44100, fractal=True, periodicity=500, weightedautomatadotfile=None,state2notedict=None,genre="WesternClassical",wfaweight_threshold=0.0,instruments=["Saxophone","Guitar","Trumpet","Violin","SteelDrum","Flute","BassDrum","TenorDrum"],format="WAV",playsynthesis=False,tempo=1):
    amplitude = np.iinfo(np.int16).max
    if function != None:
        print("###################################################")
        print("Function to Audio")
        print("###################################################")
        print(("Function:", function))
        # Example:
        # >>> map(lambda x: eval('x*x+x+1'),range(1,10))
        # [3, 7, 13, 21, 31, 43, 57, 73, 91]
        notes = []
        if fractal:
            function_nplus1 = 2
            for y in range(0, samplerate*10):
                x = function_nplus1
                function_nplus1 = eval(function)
                notes.append(function_nplus1)
                #print("function_nplus1:", function_nplus1)
        else:
            #notes = [amplitude*eval(function) for x in range(0, samplerate*10)]
            notes = []
            points = []
            x = 0
            while x < periodicity:
                points = [amplitude*eval(function)]
                print("points:",points)
                for point in points:
                    print("frequency:",abs(point))
                    signal = librosa.tone(abs(point),duration=tempo)
                    print("signal:",signal)
                    print("length of signal:",len(signal))
                    for s in signal:
                        notes.append(amplitude*s) 
                x += 1
        npnotes = np.asarray(notes)
        #scalednpnotes = np.int16(npnotes/np.max(npnotes)*32767)
        scalednpnotes = npnotes
        print(("Notes :", scalednpnotes))
        print(("Size of scaled notes:", len(scalednpnotes)))
        if fractal:
            write("function_synthesized_music_fractal.wav",
                  samplerate, scalednpnotes.astype(np.int16))
        else:
            write("function_synthesized_music.wav",
                  samplerate, scalednpnotes.astype(np.int16))
        return
    if function == None and automaton == False:
        print("###################################################")
        print("Notes to Audio")
        print("###################################################")
        npnotes = amplitude*np.random.uniform(10, 100, 44100)
        # scalednpnotes=np.int16(npnotes/np.max(npnotes)*32767)
        scalednpnotes = npnotes
        print(("Notes :", scalednpnotes))
        print(("Size of scaled notes:", len(scalednpnotes)))
        write("notes_synthesized_music.wav", samplerate,
              scalednpnotes.astype(np.int16))
        return
    if automaton == True:
        if weightedautomatadotfile is not None:
            musicwfagraph=nx.DiGraph(nx.nx_pydot.read_dot(weightedautomatadotfile))
            stpaths=shortest_path(musicwfagraph)
            print("Music WFA graph:",musicwfagraph.edges(data=True))
            print("Music WFA Shortest paths:",stpaths)
            edgeslist=list(musicwfagraph.edges(data=True))
            start_node=edgeslist[0][0]
            iterations=0 
            if state2notedict is None:
                state2notedict={'0':'C','1':'D','2':'E','3':'F','4':'G','5':'A','6':'B'}
            synthesized_notes=[state2notedict[start_node]]
            node=start_node
            prev_successors=None
            while iterations < periodicity :
                 print("iterations:",iterations)
                 wfatransitionweights=[]
                 successors=list(musicwfagraph.successors(node))
                 if prev_successors is not None and set(successors)==set(prev_successors):
                    print("successors:",successors)
                    print("prev_successors:",prev_successors)
                    nodenp=np.random.choice(musicwfagraph.nodes(),1)
                    node=nodenp[0]
                    print("node:",node)
                    successors=list(musicwfagraph.successors(node))
                 if len(successors) == 0:
                    node=edgeslist[np.random.randint(len(edgeslist),size=1)[0]][0]
                    successors=list(musicwfagraph.successors(node))
                 print("successors:",successors)
                 distribution=[]
                 for s in successors:
                    wfatransitionweight=abs(float(musicwfagraph[node][s]["label"].split(":")[1][:-1]))
                    print("Music WFA successor transition weight:",wfatransitionweight)
                    #if wfatransitionweight >= wfaweight_threshold:
                    #    wfatransitionweights.append(wfatransitionweight)
                    wfatransitionweights.append(wfatransitionweight)
                 print("wfatransitionweights:",wfatransitionweights)
                 if len(wfatransitionweights) > 1:
                    print(sum(wfatransitionweights))
                    if sum(wfatransitionweights) != 1.0:
                        sumwfatransitionweights=float(sum(wfatransitionweights))
                        print("sumfatransitionweights:",sumwfatransitionweights)
                        for n in range(len(wfatransitionweights)):
                            wfatransitionweights[n] = float(wfatransitionweights[n]) / sumwfatransitionweights
                            print(wfatransitionweights[n])
                    print("wfatransitionweights:",wfatransitionweights)
                    wfatransitionweights_np=np.array(wfatransitionweights)
                    if sum(wfatransitionweights) < 1.0:
                       zeroelements=0
                       for w in wfatransitionweights:
                           if w == 0.0:
                              zeroelements+=1
                       print("zeroelements:",zeroelements)
                       for n in range(len(wfatransitionweights)):
                           if wfatransitionweights[n] == 0.0:
                              wfatransitionweights_np[n]=((1.0-sum(wfatransitionweights))/zeroelements)
                    print("wfatransitionweights_np:",wfatransitionweights_np)
                    print("successors:",successors)
                    next_random_node_np=np.random.choice(successors,1,p=wfatransitionweights_np[:len(successors)].tolist())
                    print("next_random_node:",next_random_node_np[0])
                    next_random_node=str(next_random_node_np[0])
                    synthesized_notes.append(state2notedict[next_random_node])
                    node=next_random_node
                 prev_successors=successors
                 iterations+=1
            print("Notes synthesized by random walk on music WFA graph:",synthesized_notes)
            if len(wfatransitionweights_np) > 0:
                pianotrack=Thread(target=music_synthesis,kwargs={'virtual_piano_notes':synthesized_notes,'tempo':0.35,'musicgenre':genre,'musicwfa_notes_weights':wfatransitionweights_np.tolist()})
            else:
                pianotrack=Thread(target=music_synthesis,kwargs={'virtual_piano_notes':synthesized_notes,'tempo':0.35,'musicgenre':genre,'musicwfa_notes_weights':None})
            pianotrack.start()
            if genre=="WesternClassical":
                percussiontrack=Thread(target=percussion_synthesis,kwargs={'virtual_piano_notes':synthesized_notes,'percussions':instruments})
                percussiontrack.start()
                percussiontrack.join()
            pianotrack.join()
            if genre == "WesternClassical":
                piano=AudioSegment.from_file("virtual_piano_music.WesternClassical.wav")
            else:
                piano=AudioSegment.from_file("virtual_piano_music.Carnatic.wav")
            if genre=="WesternClassical":
                percussion=AudioSegment.from_file("music21_percussion_for_piano.wav")
                mixing=piano.overlay(percussion)
                if format == "MPEG":
                    mixing.export("music21_piano_with_percussions.mp3",format="mp3")
                    if playsynthesis:
                        play(mixing)
                else:
                    mixing.export("music21_piano_with_percussions.wav",format="wav")
                    if playsynthesis:
                        playsound("music21_piano_with_percussions.wav")
        else:
            print("###################################################")
            print("Automaton to Audio")
            print("###################################################")
            states2notes_machine_file = open("NotesStateMachine.txt", "r")
            states2notes_machine = ast.literal_eval(states2notes_machine_file.read())
            dfanotes = [int(librosa.note_to_hz(states2notes_machine['start-s1'])*1000)]
            prevstates = ['start']
            iter = 0
            while iter < samplerate*10:
                possibletransitions = []
                prevprevstates = prevstates
                prevstates = []
                # print "prevstate:",prevstate
                # if 'fs' in prevstate:
                #	break
                for k, v in list(states2notes_machine.items()):
                    statetransition = k.split("-")
                    if statetransition[0] in prevprevstates:
                       possibletransitions.append(states2notes_machine[k])
                       prevstates.append(statetransition[1])
                       if deterministic:
                          break
                for note in possibletransitions:
                    hertz = librosa.note_to_hz(note)
                    # print "Hertz:",hertz
                    dfanotes.append(amplitude*int(hertz*1000))
                    # break
                iter += 1
            npnotes = np.array(dfanotes)
            # scalednpnotes=np.int16(npnotes/np.max(npnotes)*32767)
            scalednpnotes = npnotes
            print(("Notes :", scalednpnotes))
            print(("Size of scaled dfanotes:", len(scalednpnotes)))
            write("automaton_synthesized_music.wav", samplerate, scalednpnotes.astype(np.int16))
            return


def mel_frequency_cepstral_coefficients(audiofile, dur=10):
    print("###################################################")
    print("MFCCs of Music")
    print("###################################################")
    waveform, srate = librosa.load(audiofile, duration=dur)
    mfccs = librosa.feature.mfcc(waveform, sr=srate)
    mfccs = scale(mfccs, axis=1)
    print(("mfccs:", mfccs))
    print(("mfccs shape:", mfccs.shape))
    print(("mfccs mean:", mfccs.mean(axis=1)))
    print(("mfccs variance:", mfccs.var(axis=1)))
    print(("zero crossing rate:", librosa.feature.zero_crossing_rate(waveform)))
    return (mfccs, mfccs.shape, mfccs.mean(axis=1), mfccs.var(axis=1))

def weierstrass_fractal_fourier_sinusoids(a, b, n):
    b = b + 5.7142/a
    #lambda_function_string = "np.iinfo(np.int16).max * math.pow(" + str(a) + "," + str(1) + ")*math.cos(math.pow(" + str(b) + "," + str(1) + ")*3.1428*x)"
    lambda_function_string = "math.pow(" + str(a) + "," + str(1) + ")*math.cos(math.pow(" + str(b) + "," + str(1) + ")*3.1428*x)"
    for i in range(2, n):
        #lambda_function_string += " + np.iinfo(np.int16).max*math.pow(" + str(a) + "," + str(i) + ")*math.cos(math.pow(" + str(b) + "," + str(i) + ")*3.1428*x)"
        lambda_function_string += " + math.pow(" + str(a) + "," + str(i) + ")*math.cos(math.pow(" + str(b) + "," + str(i) + ")*3.1428*x)"
    print(("weierstrass_fractal_fourier_sinusoids(): lambda_function_string = ",
          lambda_function_string))
    return lambda_function_string

def audio_merit(notes):
    mdl_entropy_merit = MinimumDescLength.minimum_descriptive_complexity(
        "".join(notes))
    print(("Merit of Audio - Minimum Descriptive Length and Entropy:", mdl_entropy_merit))

def music_weighted_automaton_from_waveform(music_clip,duration=10,note2statedict=None,genre="WesternClassical",raaga=None):
    if genre == "WesternClassical":
        sample, notesencoded=audio_to_notes_samples(music_clip,duration,note2statedict,genre="WesternClassical")
    if genre == "Carnatic":
        sample, notesencoded=audio_to_notes_samples(music_clip,duration,note2statedict,genre="Carnatic",raaga=raaga)
    print("Samples:")
    print(sample)
    print("Notes encoded:")
    print(notesencoded)
    pref={}
    suff={}
    fact={}
    splarray=SplearnArray(notesencoded,len(notesencoded[0]),len(notesencoded[0]),sample,pref,suff,fact)
    dotfile=music_weighted_automaton(music_clip,sample,splarray,len(notesencoded[0]),len(notesencoded[0]))
    return dotfile

def music_weighted_automata_analytics(weightedautomata):
    musicautomatadataset=[]
    for n in range(len(weightedautomata)-1):
        musicautomatadataset.append(nx.Graph(read_dot(weightedautomata[n])))
    gspan = GSpan(musicautomatadataset)
    gspan.GraphSet_Projection()

def generate_virtual_piano_notes(function="",randomnotesstringfrom=None,length=10, genre="WesternClassical"):
    synth_notes=[]
    if function != "":
        x=0
        notes=list(piano_notes[genre].keys())
        print("generate_virtual_piano_notes(): notes=",notes)
        while x < length:
            note_index = int(eval(function)) % len(notes)
            synth_notes.append(notes[note_index])
            x+=1
    if randomnotesstringfrom != None:
        randomnotesstring=rstr.rstr(randomnotesstringfrom,length)
        if genre=="WesternClassical":
            synth_notes_temp=randomnotesstring
            x=0
            while x <= len(synth_notes_temp)-2:
                if synth_notes_temp[x+1] == "♯":
                    synth_notes.append(synth_notes_temp[x]+synth_notes_temp[x+1])
                    x+=1
                else:
                    synth_notes.append(synth_notes_temp[x])
                x+=1
        if genre=="Carnatic":
            #synth_notes_temp=re.split("₁|₂|₃",randomnotesstring)
            synth_notes_temp=randomnotesstring
            x=0
            while x <= len(synth_notes_temp)-2:
                if synth_notes_temp[x+1] in ['₁','₂','₃']:
                    synth_notes.append(synth_notes_temp[x]+synth_notes_temp[x+1])
                    x+=1
                else:
                    synth_notes.append(synth_notes_temp[x])
                x+=1
        print("synth_notes:",synth_notes)
    return synth_notes

if __name__ == "__main__":
    # bm=mel_frequency_cepstral_coefficients("./testlogs/JSBach_Musicological_Offering.mp4",dur=20)
    # speechrecognition_audiograph("testlogs/AudioGraphExample_SpeechRecognition_2019-07-09-103018.wav")
    # audio_distance("./testlogs/JSBach_Musicological_Offering.mp4",
    #               "./testlogs/AudioGraphExample_SpeechRecognition_2019-07-09-103018.wav", dur=0.01, dtw=True)
    # audio_distance("./testlogs/JSBach_Musicological_Offering.mp4", "./testlogs/AudioGraphExample_SpeechRecognition_2019-07-09-103018.wav")
    # bm=audio_to_bitmatrix("/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/music_pattern_mining/testlogs/JSBach_Musicological_Offering.mp4",dur=20)
    # bm=audio_to_bitmatrix("/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/music_pattern_mining/testlogs/Bach Sonata No 2.mp3",dur=10)
    # bm=audio_to_bitmatrix("/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/DFT_multimedia_HilbertRadioAddress.mp3.mpga",dur=10)
    # print "Bitmap:",bm[0]
    # features=audio_features(bm)
    # print "Features:",features
    # notes=audio_to_notes("/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/music_pattern_mining/testlogs/Bach Sonata No 2.mp3",dur=10)
    #notes1 = audio_to_notes(
    #    "testlogs/JSBach_Musicological_Offering.mp4", dur=10)
    #notes2 = audio_to_notes("testlogs/Bach_Flute_Sonata_EFlat.mp4", dur=10)
    #mdl1 = audio_merit(notes1[0])
    #mdl2 = audio_merit(notes2[0])
    #MinimumDescLength.normalized_compression_distance(
    #    "".join(notes1[0]), "".join(notes2[0]))
    # merit=audio_merit(notes[0])
    # notes_to_audio()
    # notes_to_audio(automaton=True)
    #notes_to_audio(function='(x*x+x+1) % 32767', fractal=False)
    #notes_to_audio(function='int(math.sin(x*x+x+1) * 32767)',fractal=False)
    #notes_to_audio(function='5*(x*x-x) % 32767',fractal=False)
    #notes_to_audio(function='(300*math.sin(3*x) + 200*math.sin(2*x) + 100*math.sin(x))',fractal=False)
    #notes_to_audio(function='((np.iinfo(np.int16).max/(1+x))*math.sin(2*3.1428/720*x) + (np.iinfo(np.int16).max/(1+x))*math.sin(2*3.1428/1240*x) + (np.iinfo(np.int16).max/(1+x))*math.sin(2*3.1428/2400*x))', fractal=False)
    #notes_to_audio(function='(np.iinfo(np.int16).max*math.sin(2*3.1428*720*x) + np.iinfo(np.int16).max*math.sin(2*3.1428*1240*x) + np.iinfo(np.int16).max*math.sin(2*3.1428*2400*x))', fractal=False)
    #notes_to_audio(function=weierstrass_fractal_fourier_sinusoids(0.5, 5, 20), fractal=False)
    #notes_to_audio(function='(np.iinfo(np.int16).max*math.sin(2*3.1428*720*x) + np.iinfo(np.int16).max*math.sin(2*3.1428*1240*x) + np.iinfo(np.int16).max*math.sin(2*3.1428*2400*x))', fractal=False, periodicity=35)
    #music_synthesis(["testlogs/JSBach_Musicological_Offering.mp4","testlogs/Bach_Flute_Sonata_EFlat.mp4"],musicgenre="WesternClassical",dur=60,polynomial_interpolation=False, tempo=0.25)
    #all_12notes_melodies(iterations=5,number_of_notes=100,keynotes=12,tempo=0.5,musicgenre="Carnatic")
    #Twinkle Twinkle Little Star
    #music_synthesis(virtual_piano_notes=['C','C','G','G','A','A','G','F','F','E','E','D','D','C','G','G','F','F','E','E','D','G','G','F','F','E','E','D','C','C','G','G','A','A','G','F','F','E','E','D','D','C','C','C','G','G','A','A','G','F','F','E','E','D','D','C','G','G','F','F','E','E','D','G','G','F','F','E','E','D','C','C','G','G','A','A','G','F','F','E','E','D','D','C'],tempo=1)
    #music_synthesis(virtual_piano_notes=audio_to_notes("testlogs/JSBach_Musicological_Offering.mp4",music="WesternClassical")[0])
    #music_synthesis(virtual_piano_notes=generate_virtual_piano_notes(function='(np.iinfo(np.int16).max*math.sin(2*3.1428*720*x) + np.iinfo(np.int16).max*math.sin(2*3.1428*1240*x) + np.iinfo(np.int16).max*math.sin(2*3.1428*2400*x) + np.iinfo(np.int16).max*math.sin(2*3.1428*4800*x))',length=300,genre="WesternClassical"),tempo=0.25)
    #music_mfdfa_model("virtual_piano_music.wav",order=2)
    #music_mfdfa_model("testlogs/Bach_Flute_Sonata_EFlat.mp4",order=2)
    #music_mfdfa_model("testlogs/JSBach_Musicological_Offering.mp4",order=2)
    #music_mfdfa_model("testlogs/054-SBC-Aanandhamridhakarshini.mp4",order=2)
    #music_synthesis(virtual_piano_notes=generate_virtual_piano_notes(randomnotesstringfrom=piano_notes["WesternClassical"].keys(),length=300),tempo=0.35,musicgenre="WesternClassical")
    #music_synthesis(virtual_piano_notes=generate_virtual_piano_notes(randomnotesstringfrom=piano_notes["Carnatic"].keys(),length=300,genre="Carnatic"),tempo=0.35,musicgenre="Carnatic")
    #music_weighted_automaton_from_waveform("./virtual_piano_music.WesternClassical.wav")
    #music_weighted_automaton_from_waveform("./virtual_piano_music.Carnatic.wav")
    #dotfile1=music_weighted_automaton_from_waveform("testlogs/JSBach_Musicological_Offering.mp4")
    #dotfile2=music_weighted_automaton_from_waveform("testlogs/Bach_Flute_Sonata_EFlat.mp4",duration=12,note2statedict={'C':0,'D':1,'E':2,'F':3,'G':4,'A':5,'B':6,'A♯':7,'C♯':8,'D♯':9,'F♯':10,'G♯':11},genre="WesternClassical")
    #dotfile3=music_weighted_automaton_from_waveform("testlogs/054-SBC-Aanandhamridhakarshini.mp3",note2statedict={'S':0, 'R₁':1, 'R₂':2, 'R₃':3,'G₁':4, 'G₂':5, 'G₃':6, 'M₁':7, 'M₂':8, 'P':9, 'D₁':10, 'D₂':11, 'D₃':12, 'N₁':13,'N₂':14, 'N₃':15, 'Ṣ':16,'G̣₃':17,'G̣₂':18,'Ṛ₁':19,'Ṃ₂':20,'Ḍ₁':21,'P̣':22,'Ṛ₂':23,'Ḍ₂':24,'Ḍ₃':25,'Ṇ₃':26},genre="Carnatic",raaga="chitrambari")
    #music_weighted_automata_analytics([dotfile1,dotfile2,dotfile3])

    #notes_to_audio(automaton=True,weightedautomatadotfile="testlogs/JSBach_Musicological_Offering.mp4_MusicWeightedAutomaton.dot",state2notedict={'0':'A','1':'B','2':'C','3':'D','4':'E','5':'F','6':'G','7':'A♯','8':'C♯','9':'D♯','10':'F♯','11':'G♯'},genre="WesternClassical")

    #notes_to_audio(automaton=True,weightedautomatadotfile="testlogs/054-SBC-Aanandhamridhakarshini.mp3_MusicWeightedAutomaton.dot",state2notedict={'0':'S', '1':'R₁', '2':'R₂', '3':'R₃','4':'G₁', '5':'G₂', '6':'G₃', '7':'M₁', '8':'M₂', '9':'P', '10':'D₁', '11':'D₂', '12':'D₃', '13':'N₁','14':'N₂', '15':'N₃','16':'Ṣ','17':'G̣₃','18':'G̣₂','19':'Ṛ₁','20':'Ṃ₂','21':'Ḍ₁','22':'P̣','23':'Ṛ₂','24':'Ḍ₂','25':'Ḍ₃','26':'Ṇ₃'},genre="Carnatic",playsynthesis=True)
    notes_to_audio(automaton=True,weightedautomatadotfile="testlogs/054-SBC-Aanandhamridhakarshini.mp3_MusicWeightedAutomaton.dot",state2notedict={'0':'C','1':'D','2':'E','3':'F','4':'G','5':'A','6':'B','7':'A♯','8':'C♯','9':'D♯','10':'F♯','11':'G♯'},genre="WesternClassical",playsynthesis=True)
    #notes_to_audio(automaton=True,weightedautomatadotfile="testlogs/JSBach_Musicological_Offering.mp4_MusicWeightedAutomaton.dot",state2notedict={'0':'A','1':'B','2':'C','3':'D','4':'E','5':'F','6':'G','7':'A♯','8':'C♯','9':'D♯','10':'F♯','11':'G♯'},genre="WesternClassical")
    #bm=audio_to_bitmatrix("virtual_piano_music.WesternClassical.wav",dur=10)
    #features1=audio_features(audiofilename="virtual_piano_music.WesternClassical.wav",signal_bitmap=bm)
    #features2=audio_features(audiofilename="virtual_piano_music.WesternClassical.wav",signal_bitmap=bm,timbreaveragefeatures=True)
