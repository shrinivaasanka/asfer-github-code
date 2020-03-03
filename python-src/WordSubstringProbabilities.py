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
# Personal website(research): https://sites.google.com/site/kuja27/
# --------------------------------------------------------------------------------------------------------

import nltk
import json
import re
from nltk.probability import FreqDist
englishdict = open("Dictionary.txt", "r")
englishdicttxt = englishdict.readlines()
prefixes = []
suffixes = []
wordlist = []
substrings = []
prefixdict = {}
suffixdict = {}
substringsdict = {}
prefixprobdict = {}
suffixprobdict = {}
substringsprobdict = {}
ExhaustiveSearch = False


def computeprefixessuffixessubstrings(w):
    for n in range(len(w)-1):
        prefixes.append(w[:n].lower())
    for n in range(len(w)-1):
        suffixes.append(w[n:].lower())
    for x in range(len(w)-1):
        for y in range(len(w)-1):
            substrings.append(w[x:y].lower())


def wordprefixsuffixsubstringsprobdist():
    for w in englishdicttxt:
        wtok = w.split()
        if len(wtok) > 0:
            computeprefixessuffixessubstrings(wtok[0])
            wordlist.append(wtok[0])
    # prefixf=open("WordPrefixesProbabilities.txt","w")
    # suffixf=open("WordSuffixesProbabilities.txt","w")
    prefixdict = FreqDist(prefixes)
    suffixdict = FreqDist(suffixes)
    substringsdict = FreqDist(suffixes)
    totalprefixes = sum(prefixdict.values())
    totalsuffixes = sum(suffixdict.values())
    totalsubstrings = sum(substringsdict.values())
    for pk, pv in zip(list(prefixdict.keys()), list(prefixdict.values())):
        prefixprobdict[pk] = float(pv)/float(totalprefixes)
    for pk, pv in zip(list(suffixdict.keys()), list(suffixdict.values())):
        suffixprobdict[pk] = float(pv)/float(totalsuffixes)
    for pk, pv in zip(list(substringsdict.keys()), list(substringsdict.values())):
        substringsprobdict[pk] = float(pv)/float(totalsubstrings)
    # json.dump(prefixprobdict,prefixf)
    # json.dump(suffixprobdict,suffixf)
    #print "prefix probabilities:",prefixprobdict
    #print "suffix probabilities:",suffixprobdict
    return (prefixprobdict, suffixprobdict, substringsprobdict)


def wordlikelydict(comp):
    likelydict = {}
    if ExhaustiveSearch == True:
        for k3, v3 in (list(prefixprobdict.items())):
            for k4, v4 in (list(suffixprobdict.items())):
                #print "k3=",k3,"; k4=",k4
                if len(k3) > 0 and len(k4) > 0 and (k3[len(k3)-1] == k4[0]):
                    likelydict[k3[:-1]+k3[len(k3)-1]+k4[1:]] = v3 * v4
            for k5, v5 in list(suffixprobdict.items()):
                likelydict[k5] = v5
            for k6, v6 in list(prefixprobdict.items()):
                likelydict[k6] = v6
        print(likelydict)
    else:
        compwordregex = "^"+comp.replace("_", "[a-zA-Z]")+"$"
        print("compwordregex:", compwordregex)
        matchstrings = set([(k, v) for k, v in list(substringsprobdict.items(
        )) if re.search(compwordregex, k) is not None])
        for p in matchstrings:
            likelydict[p[0]] = substringsprobdict[p[0]]
        print("likelydict for ", comp, ":", likelydict)
        return likelydict


if __name__ == "__main__":
    wordprefixsuffixprobdist()
