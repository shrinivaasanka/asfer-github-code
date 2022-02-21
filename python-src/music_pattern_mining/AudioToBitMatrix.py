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
import math
import numpy
import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import write
import ast
from sklearn.preprocessing import scale
from scipy.spatial.distance import directed_hausdorff
from scipy.stats import wasserstein_distance
#from RecursiveLambdaFunctionGrowth import RecursiveLambdaFunctionGrowth

# states2notes_machine={'s1-s2':'C','s2-s1':'E','s2-s3':'D','s3-s2':'G','s3-s4':'E','s4-s5':'F','s1-s3':'G','s4-s6':'A','s5-s6':'B','s4-s3':'F','s6-s5':'E','s3-s6':'A','s6-s1':'B'}


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


def audio_distance(audio1, audio2, dur=10):
    bitmap1, waveform1, srate1 = audio_to_bitmatrix(audio1, dur)
    bitmap2, waveform2, srate2 = audio_to_bitmatrix(audio2, dur)
    print(("waveform1:", waveform1))
    print(("waveform2:", waveform2))
    hausdorff_distance = directed_hausdorff([waveform1], [waveform2])
    emd_distance = wasserstein_distance(waveform1, waveform2)
    print(("Hausdorff Distance similarity between two audio waveforms:",
          hausdorff_distance))
    print(("Earth Mover Distance similarity between two audio waveforms:", emd_distance))
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


def audio_to_notes(audio, dur=None):
    print("###################################################")
    print("Audio to Notes")
    print("###################################################")
    if dur is not None:
        waveform, srate = librosa.load(audio, duration=dur)
    freq = np.abs(librosa.stft(waveform))
    print(("Frequencies:", freq))
    notes = librosa.hz_to_note(freq)
    print(("Notes:", notes))
    return notes


def notes_to_audio(automaton=False, function=None, deterministic=True, samplerate=44100, fractal=True):
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
            notes = [amplitude*eval(function) for x in range(0, samplerate*10)]
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


def audio_merit(notes):
    from MinimumDescLength import minimum_descriptive_complexity
    entropy_merit = minimum_descriptive_complexity("".join(notes))
    print(("Merit of Audio - Minimum Descriptive Length and Entropy:", entropy_merit))


if __name__ == "__main__":
    # bm=mel_frequency_cepstral_coefficients("./testlogs/JSBach_Musicological_Offering.mp4",dur=20)
    # speechrecognition_audiograph("testlogs/AudioGraphExample_SpeechRecognition_2019-07-09-103018.wav")
    # audio_distance("./testlogs/JSBach_Musicological_Offering.mp4", "./testlogs/JSBach_Musicological_Offering.mp4")
    # audio_distance("./testlogs/JSBach_Musicological_Offering.mp4", "./testlogs/AudioGraphExample_SpeechRecognition_2019-07-09-103018.wav")
    # bm=audio_to_bitmatrix("/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/music_pattern_mining/testlogs/JSBach_Musicological_Offering.mp4",dur=20)
    # bm=audio_to_bitmatrix("/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/music_pattern_mining/testlogs/Bach Sonata No 2.mp3",dur=10)
    # bm=audio_to_bitmatrix("/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/DFT_multimedia_HilbertRadioAddress.mp3.mpga",dur=10)
    # print "Bitmap:",bm[0]
    # features=audio_features(bm)
    # print "Features:",features
    # notes=audio_to_notes("/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/music_pattern_mining/testlogs/Bach Sonata No 2.mp3",dur=10)
    # notes=audio_to_notes("/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/music_pattern_mining/testlogs/JSBach_Musicological_Offering.mp4",dur=20)
    # merit=audio_merit(notes[0])
    notes_to_audio()
    notes_to_audio(automaton=True)
    notes_to_audio(function='(x*x+x+1) % 32767',fractal=False)
    #notes_to_audio(function='int(math.sin(x*x+x+1) * 32767)',fractal=False)
    notes_to_audio(function='5*(x*x-x) % 32767')
