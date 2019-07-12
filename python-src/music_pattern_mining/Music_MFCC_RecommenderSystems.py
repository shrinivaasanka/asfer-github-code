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

from AudioToBitMatrix import mel_frequency_cepstral_coefficients
from scipy.stats import wasserstein_distance
import operator

def mfcc_earth_mover_distance_similarity(audio1,audio2):
    print "==========================================================="
    print "Earth mover distance similarity between ",audio1," and ",audio2
    print "==========================================================="
    mfccs1=mel_frequency_cepstral_coefficients(audio1)
    mfccs2=mel_frequency_cepstral_coefficients(audio2)
    earthmoverdist=wasserstein_distance(mfccs1[2],mfccs2[2]) 
    return earthmoverdist

def music_mfcc_recommender(audiolist):
    emdsimilarities={}
    for audio1 in audiolist:
        for audio2 in audiolist:
            emdsimilarities[audio1+" - "+audio2]=mfcc_earth_mover_distance_similarity(audio1,audio2)
    print "Earth Mover Similarity (low values imply high similarity):", sorted(emdsimilarities.items(),key=operator.itemgetter(1),reverse=True)
    
if __name__=="__main__":
    audiolist=["testlogs/054-SBC-Aanandhamridhakarshini.mp3","testlogs/Bach_Flute_Sonata_EFlat.mp3","testlogs/JSBach_Musicological_Offering.mp4"]
    music_mfcc_recommender(audiolist)

