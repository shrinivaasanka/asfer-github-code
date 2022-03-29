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

import nltk
class SentiWordNet:
    def __init__(self):
	self.lemmas = []
	self.pos = {}
	self.neg = {}
	try:
	    filename = "SentiWordNet_1.0.1.txt"
            fileobj = open(filename)
	    filelines = fileobj.readlines()
	    for fileline in filelines:			
            	if not fileline.startswith('#'):		
	    		filelinetoks = fileline.split('\t')
			#print filelinetoks
	    		#Note offset values can change in the same version of
			#WordNet due to minor edits in glosses.
			#Thus offsets are reported here just for reference, and
			#are not intended for use in applications.
			#Use lemmas instead.
			#String offset = data[0]+data[1]
		        positivity = float(filelinetoks[2])
		        negativity = float(filelinetoks[3])
		        synsetLemmas = nltk.word_tokenize(filelinetoks[4])
		    	for i in synsetLemmas:
				lemma = i
				self.pos[lemma] = positivity
				self.neg[lemma] = negativity
				self.lemmas.append(lemma)
				#print self.pos
				#print self.neg
				#print self.lemmas
	except IOError:
	    pass
	
    def getPositivity(self, lemma):
	return self.pos.get(lemma)

    def getNegativity(self, lemma):
	return self.neg.get(lemma)

    def getObjectivity(self, lemma):
	return 1-(self.pos.get(lemma) + self.neg.get(lemma))

    def getLemmas(self):
	return self.lemmas

swn=SentiWordNet()
print swn.getPositivity('good')
print swn.getLemmas()
print swn.getNegativity('sucks')
