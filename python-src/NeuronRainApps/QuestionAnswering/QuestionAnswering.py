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
import numpy as np
import operator
#from googlesearch import search 
import os
import networkx as nx
import spacy
import itertools
import pprint
from pyplexity import PerplexityModel
import collections
from KnowledgeGraph import create_SpaCy_knowledge_graph
from nltk.corpus import wordnet as wn

def OpenAIQuestionAnswering(question):
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    chat_completion = client.chat.completions.create(messages=[{ "role": "user", "content": question, } ], model="gpt-3.5-turbo")
    print("chat completion:",chat_completion)

def WikipediaRLFGTransformersQuestionAnswering(question,questionfraction=1,maxanswers=1,keywordsearch=False,wsheading=True,answerslice=1,answerfraction=1,bothvertices_intersection=True,sentence_type="xtag_node34_triplets",number_of_random_walks=10,number_of_words_per_sentence=5,number_of_cores_per_random_walk=5,std_sentence_PoS_dict={"ADJ":[],"PROPN":[],"NOUN":[],"AUX":[],"ADP":[],"ADV":[],"VERB":[],"DET":[],"PRON":[],"CCONJ":[],"NUM":[],"SYM":[],"X":[]},blanks=False):
    import RecursiveGlossOverlap_Classifier
    from RecursiveLambdaFunctionGrowth import RecursiveLambdaFunctionGrowth
    from collections import defaultdict
    import WordNetPath
    answersfile=open("QuestionAnswering.FormalLLM.txt","w")
    print("================================================================")
    print("Question:",question)
    questiontextgraphclassified = RecursiveGlossOverlap_Classifier.RecursiveGlossOverlap_Classify(question)
    questiontextgraph = RecursiveGlossOverlap_Classifier.RecursiveGlossOverlapGraph(question)
    print("Question Textgraph:",questiontextgraph)
    searchquery = ""
    answertextgraphs = []
    for core in questiontextgraphclassified[1][:int(len(questiontextgraph[0])/questionfraction)]:
        searchquery += " " + core[0]
    print("Search query:",searchquery)
    for r in wikipedia.search(searchquery):
        print("searchresults:",r)
        searchresults=r
        break
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
            print("wssummarysentences:",wssummarysentences)
            wssummarysentences=wssummarysentences[:int(len(wssummarysentences)*answerslice+2)-1]
        except:
            print("Wikipedia Summary Exception")
        if len(ws) > 0:
            if sentence_type=="knowledgegraph_random_walk":
                if wssummary is None or wsheading is True:
                     print("ws:",ws)
                     knowledgegraph=create_SpaCy_knowledge_graph(ws)
                else:
                     print("wssummarysentences:",wssummarysentences)
                     knowledgegraph=create_SpaCy_knowledge_graph(" ".join(wssummarysentences))
                random_walks = list(nx.generate_random_paths(knowledgegraph[0].to_undirected(),number_of_random_walks,path_length=number_of_words_per_sentence))
                numrw=0
                sentences_synthesized=defaultdict(int)
                for random_walk in random_walks:
                    naturallanguageanswer = make_sentence(random_walk,edgelabels=knowledgegraph[1],sentence_type="knowledgegraph_random_walk")
                    sentences_synthesized[numrw] = naturallanguageanswer
                    numrw += 1
                pprint.pprint(sentences_synthesized)
                perplexity = PerplexityModel.from_str("bigrams-cord19")
                rankedsentences=defaultdict(int)
                for rw,sentences in sentences_synthesized.items():
                    for s in sentences:
                        meaningfulness=perplexity.compute_sentence(s)
                        answersfile.write(s)
                        rankedsentences[meaningfulness]=s
                        answersfile.write(" --- ")
                        answersfile.write(str(meaningfulness))
                        answersfile.write("\n")
                sortedrankedsentences=collections.OrderedDict(sorted(rankedsentences.items()))
                print("SpaCy REBEL KnowledgeGraph Random Walk - Bot generated answers ranked by perplexity:")
                pprint.pprint(sortedrankedsentences)
                break
            if wssummary is None or wsheading is True:
                print("ws:",ws)
                answertextgraphclassified=RecursiveGlossOverlap_Classifier.RecursiveGlossOverlap_Classify(ws)
                answertextgraph=RecursiveGlossOverlap_Classifier.RecursiveGlossOverlapGraph(ws)
            else:
                print("wikipedia search result summary - sliced:",wssummarysentences)
                answertextgraphclassified=RecursiveGlossOverlap_Classifier.RecursiveGlossOverlap_Classify(" ".join(wssummarysentences))
                answertextgraph=RecursiveGlossOverlap_Classifier.RecursiveGlossOverlapGraph(" ".join(wssummarysentences))
            print("Answer Textgraph ",cnt,":",answertextgraphclassified)
            question_dimension=(len(questiontextgraph[0].nodes()),len(questiontextgraph[0].nodes()))
            answer_dimension=(len(answertextgraph[0].nodes()),len(answertextgraph[0].nodes()))
            queryweights_question=np.full(question_dimension,0.5).tolist()
            keyweights_question=np.full(question_dimension,0.5).tolist()
            valueweights_question=np.full(question_dimension,0.5).tolist()
            queryweights_answer=np.full(answer_dimension,0.5).tolist()
            keyweights_answer=np.full(answer_dimension,0.5).tolist()
            valueweights_answer=np.full(answer_dimension,0.5).tolist()
            question_variables=np.full(question_dimension,0.5).tolist()
            answer_variables=np.full(answer_dimension,0.5).tolist()
            transformerattention_question=rlfg.rlfg_transformers_attention_model(questiontextgraph[0],queryweights_question,keyweights_question,valueweights_question,question_variables)
            transformerattention_answer=rlfg.rlfg_transformers_attention_model(answertextgraph[0],queryweights_answer,keyweights_answer,valueweights_answer,answer_variables)
            #answertextgraph=RecursiveGlossOverlap_Classifier.RecursiveGlossOverlap_Classify(searchresults)
            cnt+=1
            answertextgraphs.append(answertextgraph)
            row=0
            queryweightedges=defaultdict()
            keyweightedges=defaultdict()
            valueweightedges=defaultdict()
            for v1 in questiontextgraph[0].nodes():
                 column=0
                 for v2 in questiontextgraph[0].nodes():
                     queryweightedges[v1 + "-" + v2]=abs(transformerattention_question[0][row][column])
            for v1 in answertextgraph[0].nodes():
                 column=0
                 for v2 in answertextgraph[0].nodes():
                     keyweightedges[v1 + "-" + v2]=abs(transformerattention_answer[1][row][column])
                     valueweightedges[v1 + "-" + v2]=abs(transformerattention_answer[2][row][column])
                     column+=1
                 row+=1
            queryweightedgeslist=sorted(queryweightedges.items(),key=operator.itemgetter(1), reverse=True)
            keyweightedgeslist=sorted(keyweightedges.items(),key=operator.itemgetter(1), reverse=True)
            valueweightedgeslist=sorted(valueweightedges.items(),key=operator.itemgetter(1), reverse=True)
            print("queryweightedges:",queryweightedgeslist)
            print("keyweightedges:",keyweightedgeslist)
            print("valueweightedges:",valueweightedgeslist)
            keyweightedgeskeys=keyweightedges.keys()
            valueweightedgeskeys=valueweightedges.keys()
            print("keyweightedgeskeys:",keyweightedgeskeys)
            print("valueweightedgeskeys:",valueweightedgeskeys)
            if cnt == maxanswers:
                break
            naturallanguageanswer=""
            if sentence_type=="xtag_node34_triplets":
                for edge in queryweightedgeslist[:int(len(queryweightedges)/answerfraction)]:
                    edgevertices=edge[0].split("-")
                    if bothvertices_intersection==True:
                         if edge[0] in keyweightedgeskeys and edgevertices[0] != edgevertices[1]:
                            print("edge relevant to question in answer textgraph:",edge[0])
                            naturallanguageanswer += make_sentence(edgevertices,sentence_type="xtag_node34_triplets")
                    else:
                             if edgevertices[0] in answertextgraph[0].nodes() or edgevertices[1] in answertextgraph[0].nodes():
                                if edgevertices[0] != edgevertices[1]:
                                    print("edge relevant to question in answer textgraph:",edge[0])
                                    naturallanguageanswer += make_sentence(edgevertices,sentence_type="xtag_node34_triplets")
                print("Bot generated XTAG grammar answer from textgraph:",naturallanguageanswer)
            if sentence_type=="textgraph_random_walk":
                numrw=0
                sentences_synthesized=defaultdict(int)
                random_walks = list(nx.generate_random_paths(answertextgraph[0].to_undirected(),number_of_random_walks,path_length=number_of_words_per_sentence))
                corevertices = [x for x,y in answertextgraphclassified[0]] 
                for random_walk in random_walks:
                    print("random walk:",random_walk)
                    core_random_walk_found=False
                    if len(set(random_walk).intersection(set(corevertices))) > number_of_cores_per_random_walk: 
                           print("core_random_walk_found - random_walk:",random_walk)
                           print("core_random_walk_found - corevertices:",corevertices)
                           core_random_walk_found=True
                    if core_random_walk_found is True:
                        if number_of_words_per_sentence==2:
                             naturallanguageanswer = make_sentence(random_walk,sentence_type="xtag_node34_triplets")
                        else:
                             naturallanguageanswer = make_sentence(random_walk,sentence_type="textgraph_random_walk",standard_sentence_PoS_dict=std_sentence_PoS_dict,markblanks=blanks)
                        sentences_synthesized[numrw]=naturallanguageanswer
                    numrw+=1
                print("Bot generated random walk answer from textgraph:")
                pprint.pprint(sentences_synthesized)
                perplexity = PerplexityModel.from_str("bigrams-cord19")
                pyplexityrankedsentences=defaultdict(int)
                wordnetperplexityrankedsentences=defaultdict(int)
                for rw,sentences in sentences_synthesized.items():
                    for s in sentences:
                        meaningfulness=perplexity.compute_sentence(s)
                        wordnetperplexity=wordnet_perplexity(s)
                        print("WordNet perplexity of sentence - ",s,":",wordnetperplexity)
                        answersfile.write(s)
                        pyplexityrankedsentences[meaningfulness]=s
                        wordnetperplexityrankedsentences[wordnetperplexity]=s
                        answersfile.write(" --- ")
                        answersfile.write(str(meaningfulness))
                        answersfile.write("\n")
                sortedpyplexityrankedsentences=collections.OrderedDict(sorted(pyplexityrankedsentences.items()))
                sortedwnperplexityrankedsentences=collections.OrderedDict(sorted(wordnetperplexityrankedsentences.items()))
                print("WordNet-ConceptNet TextGraph Random Walk - Bot generated answers ranked by pyplexity perplexity:")
                pprint.pprint(sortedpyplexityrankedsentences)
                print("WordNet-ConceptNet TextGraph Random Walk - Bot generated answers ranked by wordnet perplexity:")
                pprint.pprint(sortedwnperplexityrankedsentences)
        return sentences_synthesized

def wordnet_perplexity(sentence):
    words = sentence.split(" ")
    wordnetperplexity=1
    for w in range(len(words)-1):
        w1_synsets = wn.synsets(words[w])
        w2_synsets = wn.synsets(words[w+1])
        if len(w1_synsets) > 0 and len(w2_synsets) > 0:
            bigram_wordnet_similarity = w1_synsets[0].wup_similarity(w2_synsets[0])
            wordnetperplexity = wordnetperplexity * bigram_wordnet_similarity
    return wordnetperplexity

def make_sentence(wordnetsynsets,sentence_type="xtag_node34_triplets",standard_sentence_PoS_dict={"ADJ":[],"PROPN":[],"NOUN":[],"AUX":[],"ADP":[],"ADV":[],"VERB":[],"DET":[],"PRON":[],"CCONJ":[],"NUM":[],"SYM":[],"X":[]},markblanks=False,edgelabels=None):
    from nltk.corpus import wordnet as wn
    print("make_sentence():wordsynsets = ",wordnetsynsets)
    if sentence_type == "xtag_node34_triplets":
        prevword=wordnetsynsets[0]
        sentence=""
        try:
             for nextword in wordnetsynsets[1:]:
                 lch=wn.synset(prevword+".n.01").lowest_common_hypernyms(wn.synset(nextword+".n.01"))
                 print("lch:",lch)
                 for lch_synset in lch:
                     lch_lemma_names=lch_synset.lemma_names()
                     for lch_lemma in lch_lemma_names:
                        if lch_lemma != prevword and lch_lemma != nextword:
                            wordnet_lch_relation = " " + lch_lemma + " " 
                            sentence += prevword + " is " + wordnet_lch_relation + " of " + nextword +"."
                 prevword=nextword
        except Exception:
             print("WordNet exception")
        return sentence
    if sentence_type == "textgraph_random_walk":
        spasee=spacy.load("en_core_web_sm")
        rwtexts=[]
        rwstring=" ".join(list(set(wordnetsynsets)))
        print("rwstring:",rwstring)
        spaseePOS=spasee(rwstring)
        print("=============================================================================================")
        print("Part of speech tagging of words in random walk which can be plugged into an XTAG grammar rule:")
        print("=============================================================================================")
        for tokenPOS in spaseePOS:
            print("tokenPOS:",tokenPOS.text, tokenPOS.lemma_, tokenPOS.pos_, tokenPOS.tag_, tokenPOS.dep_, tokenPOS.shape_, tokenPOS.is_alpha, tokenPOS.is_stop)
            standard_sentence_PoS_dict[tokenPOS.pos_].append(tokenPOS.text)
        allpossiblewords=[]
        print("standard_sentence_PoS_dict:",standard_sentence_PoS_dict)
        for pos,words in standard_sentence_PoS_dict.items():
            if markblanks is True and len(words) == 0:
                words.append("------")
        for pos,words in standard_sentence_PoS_dict.items():
            if len(words) > 0:
                allpossiblewords.append(words)
        print("allpossiblewords:",allpossiblewords)
        for product in itertools.product(*allpossiblewords):
            print("product:",product)
            rwtexts.append(" ".join(product))
        return rwtexts 
    if sentence_type == "knowledgegraph_random_walk":
        n=0
        rwtexts=[]
        print("Knowledge graph edges with relation labelled:",edgelabels)
        for n in range(len(wordnetsynsets)-2):
            try:
                headspan=str(wordnetsynsets[n])
                tailspan=str(wordnetsynsets[n+1])
                relation=edgelabels[(headspan,tailspan)]
                rwtext = headspan + " " + relation + " " + tailspan
                print("headspan:",headspan)
                print("tailspan:",tailspan)
                print("relation:",relation)
                print("rwtext:",rwtext)
                rwtexts.append(rwtext)
                n += 2
            except:
                print("Exception: Key Error")
                continue
        return rwtexts

if __name__ == "__main__":
    question = sys.argv[1]
    #WikipediaRLFGTransformersQuestionAnswering(question,bothvertices_intersection=True,sentence_type="xtag_node34_triplets")
    #WikipediaRLFGTransformersQuestionAnswering(question,bothvertices_intersection=False,sentence_type="xtag_node34_triplets")
    #WikipediaRLFGTransformersQuestionAnswering(question,wsheading=True,answerslice=0.01,bothvertices_intersection=False,sentence_type="textgraph_random_walk",number_of_words_per_sentence=50,std_sentence_PoS_dict={"ADJ":[],"PROPN":[],"NOUN":[],"AUX":[],"ADP":[],"ADV":[],"VERB":[],"DET":[],"PRON":[],"CCONJ":[],"NUM":[],"SYM":[],"X":[],"PUNCT":[]},number_of_cores_per_random_walk=3,number_of_random_walks=3,blanks=False)
    WikipediaRLFGTransformersQuestionAnswering(question,wsheading=True,answerslice=0.01,bothvertices_intersection=False,sentence_type="textgraph_random_walk",number_of_words_per_sentence=50,std_sentence_PoS_dict={"NUM":[],"ADJ":[],"PROPN":[],"NOUN":[],"PUNCT":[],"AUX":[],"ADP":[],"ADV":[],"VERB":[],"DET":[],"PRON":[],"CCONJ":[],"SYM":[],"X":[]},number_of_cores_per_random_walk=3,number_of_random_walks=3,blanks=False)
    #WikipediaRLFGTransformersQuestionAnswering(question,wsheading=False,answerslice=0.5,bothvertices_intersection=False,sentence_type="knowledgegraph_random_walk",number_of_words_per_sentence=50,std_sentence_PoS_dict={"NUM":[],"ADJ":[],"PROPN":[],"NOUN":[],"PUNCT":[],"AUX":[],"ADP":[],"ADV":[],"VERB":[],"DET":[],"PRON":[],"CCONJ":[],"SYM":[],"X":[]},number_of_cores_per_random_walk=3,number_of_random_walks=3,blanks=False)
    #OpenAIQuestionAnswering(question)
