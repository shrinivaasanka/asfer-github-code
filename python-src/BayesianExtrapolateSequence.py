from collections import defaultdict
from nltk.probability import FreqDist
from MusicSynthesizer_AddOn import pysynth_synthesize_notes 
import numpy as np 
from scipy.io.wavfile import write
import librosa
from playsound import playsound

succeedingelementdict=defaultdict(list)
elementprobabilities=defaultdict(float)

def compute_prior_probabilities_and_extend(originalsequence,trainingsequence,alphabetsize=7,extension=20):
    for n in range(len(trainingsequence)-2):
        succeedingelementdict[trainingsequence[n]].append(trainingsequence[n+1])
    succeedingelementdict[trainingsequence[len(trainingsequence)-1]].append(" ")
    print("succeedingelementdict:",succeedingelementdict)
    for element,nextelements in succeedingelementdict.items():
        freqdist=FreqDist()
        for nextelement in nextelements:
            freqdist[nextelement] += 1
        elementprobabilities[element]=defaultdict(float)
        print("FreqDist for elements succeeding:",element)
        freqdist.pprint()
        for nextelement,freq in freqdist.items():
            elementprobabilities[element][nextelement]=float(freq)/float(len(nextelements))
    print("elementprobabilities:",elementprobabilities)
    randpast=np.random.randint(1,len(trainingsequence))
    extendedsequence=extend_sequence(originalsequence,length=extension,history=randpast)
    return extendedsequence

def extend_sequence(originalsequence,length=10,history=5):
    extendedsequence=originalsequence
    iterations=0
    while iterations < length:
        maxprobability=-1.0
        maxprobelement=""
        print("elementprobabilities[extendedsequence[len(extendedsequence)-1]].items():",elementprobabilities[extendedsequence[len(extendedsequence)-history]].items())
        for nextelement,probability in elementprobabilities[extendedsequence[len(extendedsequence)-history]].items():
           print("nextelement:",nextelement,"---probability:",probability)
           if probability > maxprobability: 
              maxprobelement=nextelement
              maxprobability=probability
        iterations+=1
        if maxprobelement not in [" ","(",")","."]: 
            extendedsequence.append(maxprobelement)
    succeedingelementdict.clear()
    elementprobabilities.clear()
    print("extendedsequence:",extendedsequence)
    return extendedsequence

if __name__=="__main__":
    #extrapolate a music notes sequence
    musicnotessequence=['C','C','G','G','A','A','G','F','F','E','E','D','D','C','G','G','F','F','E','E','D','G','G','F','F','E','E','D','C','C','G','G','A','A','G','F','F','E','E','D','D','C','C','C','G','G','A','A','G','F','F','E','E','D','D','C','G','G','F','F','E','E','D','G','G','F','F','E','E','D','C','C','G','G','A','A','G','F','F','E','E','D','D','C']
    learntmusicnotessequence=musicnotessequence
    learntmusicnotessequence=compute_prior_probabilities_and_extend(originalsequence=musicnotessequence,trainingsequence=learntmusicnotessequence,alphabetsize=7,extension=50)
    pysynth_synthesize_notes(virtual_piano_notes=learntmusicnotessequence,duration=5,filename="BayesianExtrapolateSequence.wav")
    playsound("BayesianExtrapolateSequence.wav")
    #extrapolate a numeric sequence
    succeedingelementdict=defaultdict(list)
    elementprobabilities=defaultdict(float)
    numericsequence="141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165271201909145648566923460348610454326648213393607260249141273724587006606315588174881520920962829254091715364367892590360011330530548820466521384146"
    compute_prior_probabilities_and_extend(originalsequence=list(numericsequence),trainingsequence=list(numericsequence),alphabetsize=10,extension=20)
    #extrapolate a text sentence 
    succeedingelementdict=defaultdict(list)
    elementprobabilities=defaultdict(float)
    sentence="Changes in the region traditionally associated with El Niño phenomenon (central and eastern tropical Pacific) are about four times as large as it might be expected simply by increases in moisture, consiste"
    extendedsentence=compute_prior_probabilities_and_extend(originalsequence=list(sentence),trainingsequence=list(sentence),alphabetsize=30,extension=20)
