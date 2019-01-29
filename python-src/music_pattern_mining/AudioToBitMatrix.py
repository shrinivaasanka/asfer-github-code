#-------------------------------------------------------------------------------------------------------
#NEURONRAIN ASFER - Software for Mining Large Datasets
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------------
#K.Srinivasan
#NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
#Personal website(research): https://sites.google.com/site/kuja27/
#--------------------------------------------------------------------------------------------------------

import librosa
import numpy
import matplotlib.pyplot as plt
import numpy as np 
from MinimumDescLength import minimum_descriptive_complexity

def audio_to_bitmatrix(audio,dur=None,binary=False):
	bitmap=[]
	if binary == False:
		if dur is not None:
			waveform,srate=librosa.load(audio,duration=dur)
		input_audio_array=numpy.asarray(waveform).tolist()
		for r in input_audio_array:
			bitmap.append(r)
	else:
		if dur is not None:
			waveform,srate=librosa.load(audio,dtype=numpy.int64,duration=dur)
		input_audio_array=numpy.asarray(waveform).tolist()
		for r in input_audio_array:
			bitmap.append(bin(r))
		
	#print "audio_to_bitmatrix() for - ",audio,":",bitmap
	return (bitmap,waveform,srate)

def audio_features(signal_bitmap):
	print "################################################"
	print "Histogram/Probability Distribution of the audio signal"
	print "################################################"
	hist, bin = np.histogram(signal_bitmap[0],density=True)
	print "hist:",hist
	print "bin:",bin
	#plt.hist(signal_bitmap, color='r', range=(0, 0.2), alpha=0.5, bins=20)
	#plt.show()
	print "#################################################"
	print "Note Onset Detection"
	print "#################################################"
	onstrength=librosa.onset.onset_strength(signal_bitmap[1],sr=signal_bitmap[2])
	times=librosa.frames_to_time(np.arange(len(onstrength)), sr=signal_bitmap[2])	
	onset_frames=librosa.onset.onset_detect(onset_envelope=onstrength,sr=signal_bitmap[2])
	print "Notes onsets occur at:",onset_frames
	return (hist,bin,times,onstrength,onset_frames)

def audio_to_notes(audio,dur=None):
	print "###################################################"
	print "Audio to Notes"
	print "###################################################"
	if dur is not None:
		waveform,srate=librosa.load(audio,duration=dur)
	freq=np.abs(librosa.stft(waveform))
	print "Frequencies:",freq
	notes=librosa.hz_to_note(freq)
	print "Notes:",notes
	return notes

def audio_merit(notes):
	entropy_merit=minimum_descriptive_complexity("".join(notes))
	print "Merit of Audio - Minimum Descriptive Length and Entropy:",entropy_merit

if __name__=="__main__":
	bm=audio_to_bitmatrix("/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/music_pattern_mining/testlogs/JSBach_Musicological_Offering.mp4",dur=20)
	#bm=audio_to_bitmatrix("/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/music_pattern_mining/testlogs/Bach Sonata No 2.mp3",dur=10)
	#bm=audio_to_bitmatrix("/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/DFT_multimedia_HilbertRadioAddress.mp3.mpga",dur=10)
	print "Bitmap:",bm[0]
	features=audio_features(bm)
	print "Features:",features
	#notes=audio_to_notes("/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/music_pattern_mining/testlogs/Bach Sonata No 2.mp3",dur=10)
	notes=audio_to_notes("/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/music_pattern_mining/testlogs/JSBach_Musicological_Offering.mp4",dur=20)
	merit=audio_merit(notes[0])
