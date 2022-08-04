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
from collections import defaultdict
import numpy as np
import operator
import WordNetPath
#from googlesearch import search 


def AIQuestionAnswering(question,questionfraction=5,maxanswers=1,keywordsearch=False,wsheading=False,answersliced=1,answerfraction=20):
    print("================================================================")
    print("Question:",question)
    questiontextgraph = RecursiveGlossOverlap_Classifier.RecursiveGlossOverlap_Classify(question)
    print("Question Textgraph:",questiontextgraph)
    searchquery = ""
    answertextgraphs = []
    for core in questiontextgraph[1][:int(len(questiontextgraph[0])/questionfraction)]:
        searchquery += " " + core[0]
    #print("Search query:",searchquery)
    #for r in search(searchquery):
    #    print("searchresults:",r)
    #    searchresults=r
    #    break
    if not keywordsearch:
        wikipediasearch=wikipedia.search(question)
    else:
        wikipediasearch=wikipedia.search(searchquery)
    rlfg=RecursiveLambdaFunctionGrowth()
    cnt=1
    for ws in wikipediasearch:
        print("wikipedia search result:",ws)
        wssummary=None
        wssummarysentences=None
        try:
            wssummary=wikipedia.summary(ws)
            wssummarysentences=wssummary.split(".")
            print("wikipedia search result summary - sliced:",wssummarysentences[:answersliced])
        except:
            print("Wikipedia Summary Exception")
        if len(ws) > 0:
            if wssummary is None or wsheading is True:
                answertextgraphclassified=RecursiveGlossOverlap_Classifier.RecursiveGlossOverlap_Classify(ws)
                answertextgraph=RecursiveGlossOverlap_Classifier.RecursiveGlossOverlapGraph(ws)
            else:
                answertextgraphclassified=RecursiveGlossOverlap_Classifier.RecursiveGlossOverlap_Classify(" ".join(wssummarysentences[:answersliced]))
                answertextgraph=RecursiveGlossOverlap_Classifier.RecursiveGlossOverlapGraph(" ".join(wssummarysentences[:answersliced]))
            print("Answer Textgraph ",cnt,":",answertextgraphclassified)
            dimension=(len(answertextgraph[0].nodes()),len(answertextgraph[0].nodes()))
            queryweights=np.full(dimension,0.5).tolist()
            keyweights=np.full(dimension,0.5).tolist()
            valueweights=np.full(dimension,0.5).tolist()
            variables=np.full(dimension,0.5).tolist()
            transformerattention=rlfg.rlfg_transformers_attention_model(answertextgraph[0],queryweights,keyweights,valueweights,variables)
            #answertextgraph=RecursiveGlossOverlap_Classifier.RecursiveGlossOverlap_Classify(searchresults)
            cnt+=1
            answertextgraphs.append(answertextgraph)
            row=0
            queryweightedges=defaultdict()
            keyweightedges=defaultdict()
            valueweightedges=defaultdict()
            for v1 in answertextgraph[0].nodes():
                 column=0
                 for v2 in answertextgraph[0].nodes():
                     queryweightedges[v1 + "-" + v2]=transformerattention[0][row][column]
                     keyweightedges[v1 + "-" + v2]=transformerattention[1][row][column]
                     valueweightedges[v1 + "-" + v2]=transformerattention[2][row][column]
                     column+=1
                 row+=1
            queryweightedges=sorted(queryweightedges.items(),key=operator.itemgetter(1), reverse=True)
            keyweightedges=sorted(keyweightedges.items(),key=operator.itemgetter(1), reverse=True)
            valueweightedges=sorted(valueweightedges.items(),key=operator.itemgetter(1), reverse=True)
            print("queryweightedges:",queryweightedges)
            print("keyweightedges:",keyweightedges)
            print("valueweightedges:",valueweightedges)
            if cnt == maxanswers:
                break
            naturallanguageanswer=""
            for edge in queryweightedges[:int(len(queryweightedges)/answerfraction)]:
                edgevertices=edge[0].split("-")
                wordnetpath=WordNetPath.path_between(edgevertices[0],edgevertices[1])
                #print("wordnetpath:",wordnetpath)
                if len(wordnetpath) > 1:
                    naturallanguageanswer += make_sentence(wordnetpath)
            print("Bot generated answer from textgraph:",naturallanguageanswer)
        return answertextgraphs

def make_sentence(wordnetsynsets):
    prevword=wordnetsynsets[0]
    sentence=""
    for nextword in wordnetsynsets[1:]:
        sentence += prevword + " is a(n) " + nextword +"."
        prevword=nextword
    return sentence

if __name__ == "__main__":
    question = sys.argv[1]
    AIQuestionAnswering(question)
