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
		
	print "audio_to_bitmatrix() for - ",audio,":",bitmap
	return bitmap

if __name__=="__main__":
	bm=audio_to_bitmatrix("/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/DFT_multimedia_HilbertRadioAddress.mp3.mpga",dur=10)
	print "Bitmap:",bm
