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

# states2notes_machine={'s1-s2':'C','s2-s1':'E','s2-s3':'D','s3-s2':'G','s3-s4':'E','s4-s5':'F','s1-s3':'G','s4-s6':'A','s5-s6':'B','s4-s3':'F','s6-s5':'E','s3-s6':'A','s6-s1':'B'}
piano_notes={"WesternClassical":{'A':440,'B':493.89,'C':261.63,'D':293.67,'E':329.63,'F':349.23,'G':392,'a':466.17,'c':227.18,'d':311.13,'f':370,'g':415.31},"Carnatic":{'S':240, 'R₁':254.27, 'R₂':269.39, 'R₃':275,'G₁':285.41, 'G₂':302.38, 'G₃':311, 'M₁':320.36, 'M₂':339.41, 'P':359.60, 'D₁':380.98, 'D₂':403.63, 'D₃':415, 'N₁':425,'N₂':453.06, 'N₃':480}}


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


def audio_features(signal_bitmap):
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
        signal_bitmap[1], sr=signal_bitmap[2])
    times = librosa.frames_to_time(
        np.arange(len(onstrength)), sr=signal_bitmap[2])
    onset_frames = librosa.onset.onset_detect(
        onset_envelope=onstrength, sr=signal_bitmap[2])
    print(("Notes onsets occur at:", onset_frames))
    return (hist, bin, times, onstrength, onset_frames)

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
        piano_freq.append(piano_notes[genre][n])
    return piano_freq

def music_synthesis(training_music=None,dur=5,samplerate=44100,polynomial_interpolation=True,polyfeatures=False,virtual_piano_notes=None,tempo=1,amplitude=4096,musicgenre="WesternClassical"):
    music_interpol_poly=[]
    synthesized_poly=0
    if training_music is None and virtual_piano_notes is not None:
        print("virtual piano notes:",virtual_piano_notes)
        #freq=librosa.note_to_hz(virtual_piano_notes)
        freq=get_piano_frequencies(virtual_piano_notes,genre=musicgenre)
        print("freq:",freq)
        #audio=mir_eval.sonify.pitch_contour(librosa.times_like(freq),freq,samplerate,amplitudes=amps)
        audio=[]
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
            amps.fill(amplitude)
            #amps=np.iinfo(np.int16).max*2*np.random.random_sample(len(signal))
            for s in signal:
                 audio.append(amps[n]*s) 
                 n +=1
        audio=np.asarray(audio)
        #audio=np.concatenate(audio)
        #print("Synthesized audio:",audio)
        plt.figure(figsize=(14, 5))
        write("virtual_piano_music.wav", samplerate, audio.astype(np.int16))
        playsound("virtual_piano_music.wav")
        waveform, srate = librosa.load("virtual_piano_music.wav")
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
        synth_notes=defaultdict()
        synth_music=[]
        minnoteslength=np.iinfo(np.int16).max
        for music in training_music:
            waveform, srate = librosa.load(music, duration=dur)
            x_points = list(range(len(waveform))) 
            print("x_points:",len(x_points))
            y_points = waveform
            print("y_points:",len(y_points))
            freq = np.abs(librosa.stft(waveform))
            try:
                print("freq:",freq)
                notes = librosa.hz_to_note(freq)
                print("notes from hz_to_note():",len(notes))
                synth_notes[music]=notes
                if minnoteslength > len(notes):
                    minnoteslength=len(notes)
            except Exception as e:
                print("Exception in librosa - hertz-to-note")
                continue
        iterations=int(minnoteslength/10)
        print("iterations:",iterations)
        for it in range(iterations):
            randindex1=random.randint(0,len(training_music)-1)
            randindex2=random.randint(0,len(training_music[randindex1])-1)
            notes=synth_notes[training_music[randindex1]][randindex2]
            randindex3=random.randint(0,len(notes)-1)
            frequency=librosa.note_to_hz(notes[randindex3])
            print("frequency:",frequency)
            signal = librosa.tone(frequency,duration=1)
            print("signal:",signal)
            for s in signal:
                synth_music.append(s*np.iinfo(np.int16).max) 
        npsynth = np.asarray(synth_music)
        write("function_synthesized_music.wav", samplerate, npsynth.astype(np.int16))

def notes_to_audio(automaton=False, function=None, deterministic=True, samplerate=44100, fractal=True, periodicity=100):
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
                    signal = librosa.tone(abs(point),duration=0.25)
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
        print("###################################################")
        print("Automaton to Audio")
        print("###################################################")
        states2notes_machine_file = open("NotesStateMachine.txt", "r")
        states2notes_machine = ast.literal_eval(
            states2notes_machine_file.read())
        dfanotes = [int(librosa.note_to_hz(
            states2notes_machine['start-s1'])*1000)]
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
        write("automaton_synthesized_music.wav",
              samplerate, scalednpnotes.astype(np.int16))
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
    #music_synthesis(["testlogs/JSBach_Musicological_Offering.mp4","testlogs/Bach_Flute_Sonata_EFlat.mp4"],dur=10)
    all_12notes_melodies(iterations=5,number_of_notes=100,keynotes=12,tempo=0.5,musicgenre="Carnatic")
    #Twinkle Twinkle Little Star
    #music_synthesis(virtual_piano_notes=['C','C','G','G','A','A','G','F','F','E','E','D','D','C','G','G','F','F','E','E','D','G','G','F','F','E','E','D','C','C','G','G','A','A','G','F','F','E','E','D','D','C','C','C','G','G','A','A','G','F','F','E','E','D','D','C','G','G','F','F','E','E','D','G','G','F','F','E','E','D','C','C','G','G','A','A','G','F','F','E','E','D','D','C'],tempo=1)
    #music_synthesis(virtual_piano_notes=audio_to_notes("testlogs/JSBach_Musicological_Offering.mp4",music="WesternClassical")[0])
