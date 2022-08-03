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
# Copyleft (Copyright+):
# NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
# Personal website(research): https://acadpdrafts.readthedocs.io/en/latest/
# ------------------------------------------------------------------------------------------------------------------------------

import cmd,sys
import wikipedia
import RecursiveGlossOverlap_Classifier
from RecursiveLambdaFunctionGrowth import RecursiveLambdaFunctionGrowth
#from googlesearch import search 

if __name__ == "__main__":
    question = sys.argv[1]
    print("================================================================")
    print("Question:",question)
    questiontextgraph = RecursiveGlossOverlap_Classifier.RecursiveGlossOverlap_Classify(question)
    print("Question Textgraph:",questiontextgraph)
    searchquery = ""
    fraction=5
    for core in questiontextgraph[1][:int(len(questiontextgraph[0])/fraction)]:
        searchquery += " " + core[0]
    #print("Search query:",searchquery)
    #for r in search(searchquery):
    #    print("searchresults:",r)
    #    searchresults=r
    #    break
    wikipediasearch=wikipedia.search(question)
    rlfg=RecursiveLambdaFunctionGrowth()
    cnt=1
    for ws in wikipediasearch:
        print("wikipedia search result:",ws)
        try:
            print("wikipedia search result summary:",wikipedia.summary(ws))
        except:
            print("Exception")
        if len(ws) > 0:
            answertextgraphclassified=RecursiveGlossOverlap_Classifier.RecursiveGlossOverlap_Classify(ws)
            answertextgraph=RecursiveGlossOverlap_Classifier.RecursiveGlossOverlapGraph(ws)
            print("Answer Textgraph ",cnt,":",answertextgraphclassified)
            transformerattention=rlfg.rlfg_transformers_attention_model(answertextgraph[0],[[1,2,3],[0.1,0.3,0.5],[3,4,5]],[[4,5,6],[0.1,0.3,0.5],[3,4,5]],[[7,8,9],[0.1,0.3,0.5],[3,4,5]],[[0.1,0.3,0.5],[0.1,0.1,0.1],[0.2,0.3,0.5]])
            #answertextgraph=RecursiveGlossOverlap_Classifier.RecursiveGlossOverlap_Classify(searchresults)
            cnt+=1
