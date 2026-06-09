from collections import defaultdict
from nltk.probability import FreqDist

succeedingelementdict=defaultdict(list)
elementprobabilities={}

def compute_prior_probabilities_and_extend(trainingsequence,alphabetsize=7):
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
            elementprobabilities[element][nextelement]=float(freq)/float(alphabetsize)
    print("elementprobabilities:",elementprobabilities)
    extendedsequence=extend_sequence(trainingsequence)
    return extendedsequence

def extend_sequence(trainingsequence,length=1):
    extendedsequence=trainingsequence
    iterations=0
    while iterations < length:
        maxprobability=-1
        maxprobelement=""
        for nextelement,probability in elementprobabilities[extendedsequence[len(extendedsequence)-1]].items():
           if probability > maxprobability and nextelement not in [" ","(",")","."]: 
              maxprobelement=nextelement
              extendedsequence.append(maxprobelement)
              print("extendedsequence:",extendedsequence)
              break
        iterations+=1
    return extendedsequence

if __name__=="__main__":
    #extrapolate a music notes sequence
    musicnotessequence="G-3 B-3 A-3 D♯-2 F♯-2 E-2 D-2 C♯-2 D-2 D♯-2 D♯-2 F-2 G-2 G♯-2 G♯-2 A-2 A♯-2 B-2 B-2 C-2 C-2 C-2 C♯-1 D-1 D-1 D-1 D♯-1 D♯-1 D♯-1 D♯-1 D♯-1 E-1 E-1 E-1 E-1 E-1 E-1 F-1 F-1 F-1 F-1 F-1 E-1 F♯-2F-3 D♯-3 E-4 E-3 G♯-3 D♯-3 E-3 B-4 D-3 D♯-3 D-3 F♯-3 F♯-3 A-3 G♯-3 G♯-3 B-3 B-3 A♯-3 C-3 C♯-2 B-3 D-2 D-2 C♯-2 D-2 D♯-2 D-2 D♯-2 D♯-2 D♯-2 E-2 E-2 D♯-2 F-2 E-2 E-2 F-2 E-2 F-2 F-2 F-2 G-2 D-2B-4 F♯-4 C♯-5 F-6 A♯-5 B-7 C-6 D-4 D-5 A-6 D-5 B-8 A-8 C-6 G-6 G-6 F♯-8 G♯-6 F-8 D-5 B-6 D-6 A♯-6 G-7 C-6 E-7 A♯-7 C-9 G♯-7 G♯-8 A♯-8 D♯-6 D-8 B-6 F♯-6 B-7 C♯-6 B-6 F-6 A♯-7 D-6 D-7 G♯-5 D♯-3D♯-4 G♯-5 G♯-6 C-6 F♯-5 C♯-4 G♯-4 A♯-4 G♯-5 A-5 F-5 E-6 F-5 B-5 A-5 A-5 F♯-5 C-6 G♯-6 G-5 B-6 D-7 C♯-5 F♯-5 F♯-5 G♯-5 A♯-5 G♯-5 F♯-5 B-6 E-6 E-5 G-5 D♯-5 G-7 D-6 A-6 G-5 A-5 B-6 C-6 D♯-6 D-5 E-4E-4 A♯-5 F♯-4 D-4 E-6 C♯-4 B-4 A♯-4 F♯-5 D-4 B-5"
    compute_prior_probabilities_and_extend(trainingsequence=musicnotessequence.split(" "),alphabetsize=7)
    #extrapolate a numeric sequence
    succeedingelementdict=defaultdict(list)
    elementprobabilities={}
    numericsequence="141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165271201909145648566923460348610454326648213393607260249141273724587006606315588174881520920962829254091715364367892590360011330530548820466521384146"
    compute_prior_probabilities_and_extend(trainingsequence=list(numericsequence),alphabetsize=10)
    #extrapolate a text sentence 
    succeedingelementdict=defaultdict(list)
    elementprobabilities={}
    sentence="Changes in the region traditionally associated with El Niño phenomenon (central and eastern tropical Pacific) are about four times as large as it might be expected simply by increases in moisture, consiste"
    extendedsentence=compute_prior_probabilities_and_extend(trainingsequence=list(sentence),alphabetsize=30)
