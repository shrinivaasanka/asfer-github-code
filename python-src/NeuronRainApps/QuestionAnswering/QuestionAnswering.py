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
#import spacy
import itertools
import pprint
#from pyplexity import PerplexityModel
import collections
#from KnowledgeGraph import create_SpaCy_knowledge_graph
from nltk.corpus import wordnet as wn
from nltk.parse.dependencygraph import conll_data2, DependencyGraph
from nltk.parse.projectivedependencyparser import ProjectiveDependencyParser, ProbabilisticProjectiveDependencyParser
from nltk.corpus import dependency_treebank
from nltk.corpus import treebank,brown,conll2000
from collections import defaultdict
from nltk import ConditionalFreqDist
import csv
from WordNetPath import path_between

def OpenAIQuestionAnswering(question):
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    chat_completion = client.chat.completions.create(messages=[{ "role": "user", "content": question, } ], model="gpt-3.5-turbo")
    print("chat completion:",chat_completion)

def WikipediaRLFGTransformersQuestionAnswering(question,questionfraction=1,maxanswers=1,keywordsearch=False,wsheading=True,answerslice=1,answerfraction=1,bothvertices_intersection=True,sentence_type="xtag_node34_triplets",number_of_random_walks=10,number_of_words_per_sentence=5,number_of_cores_per_random_walk=5,std_sentence_PoS_dict={"ADJ":[],"PROPN":[],"NOUN":[],"AUX":[],"ADP":[],"ADV":[],"VERB":[],"DET":[],"PRON":[],"CCONJ":[],"NUM":[],"SYM":[],"X":[]},blanks=False,perplexity_algorithm="WordNet",treenode_type="PoS",sentence_tuple_array=False,sentence_PoS_array=None,randomwalk_to_sentence_template_ratio=10,user_defined_PoS2Vocabulary_dict=None):
    import RecursiveGlossOverlap_Classifier
    import spacy
    from pyplexity import PerplexityModel
    from RecursiveLambdaFunctionGrowth import RecursiveLambdaFunctionGrowth
    from collections import defaultdict
    from KnowledgeGraph import create_SpaCy_knowledge_graph
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
                             naturallanguageanswer = make_sentence(random_walk,sentence_type="xtag_node34_triplets",treenode_type=treenode_type)
                        else:
                             if sentence_tuple_array:
                                if float(len(random_walk))/float(len(sentence_PoS_array)) < randomwalk_to_sentence_template_ratio: 
                                    naturallanguageanswer = make_sentence2(random_walk,sentence_PoS_tuple_array=sentence_PoS_array,treenode_type="tag",user_defined_PoS2Vocabulary_dict=user_defined_PoS2Vocabulary_dict)
                             else:
                                naturallanguageanswer = make_sentence(random_walk,sentence_type="textgraph_random_walk",standard_sentence_PoS_dict=std_sentence_PoS_dict,markblanks=blanks,treenode_type=treenode_type)
                        sentences_synthesized[numrw]=naturallanguageanswer
                    numrw+=1
                print("Bot generated random walk answer from textgraph:")
                pprint.pprint(sentences_synthesized)
                if perplexity_algorithm=="pyplexity":
                    perplexity = PerplexityModel.from_str("bigrams-cord19")
                    pyplexityrankedsentences=defaultdict(list)
                if perplexity_algorithm=="WordNet":
                    wordnetperplexityrankedsentences=defaultdict(list)
                for rw,sentences in sentences_synthesized.items():
                    for s in sentences:
                        if perplexity_algorithm=="pyplexity":
                             meaningfulness=perplexity.compute_sentence(s)
                        if perplexity_algorithm=="WordNet":
                             wordnetperplexity=wordnet_perplexity(s)
                             print("WordNet perplexity of sentence - ",s,":",wordnetperplexity)
                        answersfile.write(s)
                        if perplexity_algorithm=="pyplexity":
                            pyplexityrankedsentences[meaningfulness].append(s)
                        if perplexity_algorithm=="WordNet":
                            wordnetperplexityrankedsentences[wordnetperplexity].append(s)
                        answersfile.write(" --- ")
                        if perplexity_algorithm=="pyplexity":
                            answersfile.write(str(meaningfulness))
                        if perplexity_algorithm=="WordNet":
                            answersfile.write(str(wordnetperplexity))
                        answersfile.write("\n")
                if perplexity_algorithm=="pyplexity":
                    sortedpyplexityrankedsentences=dict(collections.OrderedDict(sorted(pyplexityrankedsentences.items())))
                    print("WordNet-ConceptNet TextGraph Random Walk - Bot generated answers ranked by pyplexity perplexity:")
                    pprint.pprint(sortedpyplexityrankedsentences)
                if perplexity_algorithm=="WordNet":
                    sortedwnperplexityrankedsentences=dict(collections.OrderedDict(sorted(wordnetperplexityrankedsentences.items())))
                    print("WordNet-ConceptNet TextGraph Random Walk - Bot generated answers ranked by wordnet perplexity:")
                    pprint.pprint(sortedwnperplexityrankedsentences)
                NounPhrases=[]
                VerbPhrases=[]
                psg_sentences=[]
                spasee=spacy.load("en_core_web_sm")
                if perplexity_algorithm=="pyplexity":
                    for perplexity,sentence in sortedpyplexityrankedsentences.items():
                         sentenceclassified=False
                         print("sentence:",sentence)
                         spaseePOS=spasee(sentence)
                         for tokenPOS in spaseePOS:
                            print("tokenPOS:",tokenPOS.text, tokenPOS.lemma_, tokenPOS.pos_, tokenPOS.tag_, tokenPOS.dep_, tokenPOS.shape_, tokenPOS.is_alpha, tokenPOS.is_stop)
                            if not sentenceclassified:
                                 if tokenPOS.pos_ == "VERB":
                                     VerbPhrases.append(sentence)
                                     sentenceclassified=True
                         if not sentenceclassified: 
                            NounPhrases.append(sentence)
                            sentenceclassified=True
                    print("Phrase Structure Grammar (PSG) sentences from Noun Phrase-Verb Phrase combinations:")
                    print("Noun Phrases:",NounPhrases)
                    print("Verb Phrases:",VerbPhrases)
                    if len(NounPhrases) > 0  and len(VerbPhrases) > 0:
                         for nounphrase in list(set(NounPhrases)):
                             for verbphrase in list(set(VerbPhrases)):
                                print("PSG NP-VP Sentence:" + nounphrase + " " + verbphrase) 
                                psg_sentences.append(nounphrase + " " + verbphrase)
                    print("PSG NP-VP sentences synthesized:",psg_sentences)
        return (sentences_synthesized,psg_sentences)

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

def make_sentence2(randomwalkvertices,sentence_PoS_tuple_array=[],treenode_type="tag",max_synth_sentences=1000,user_defined_PoS2Vocabulary_dict=None,max_words_per_PoS=1000):
    import spacy
    spasee=spacy.load("en_core_web_sm")
    rwtexts=[]
    rwstring=" ".join(list(set(randomwalkvertices)))
    print("rwstring:",rwstring)
    spaseePOS=list(spasee(rwstring))
    print("=============================================================================================")
    print("Part of speech tagging of words in random walk which can be plugged into a grammar rule:")
    print("=============================================================================================")
    remainingsentence=0
    #for tokenPOS in spaseePOS:
    while len(spaseePOS) > 0:
        print("spacy PoS:",spaseePOS)
        print("remainingsentence:",remainingsentence)
        tokenPOS=spaseePOS[0]
        print("tokenPOS:",tokenPOS.text, tokenPOS.lemma_, tokenPOS.pos_, tokenPOS.tag_, tokenPOS.dep_, tokenPOS.shape_, tokenPOS.is_alpha, tokenPOS.is_stop)
        if treenode_type=="PoS":
            for t in sentence_PoS_tuple_array:
                print("t:",t)
                if t[0] == tokenPOS.pos_ and t[1] == []:
                    t[1].append(tokenPOS.text) 
                    break
                else:
                    if t[0] == tokenPOS.pos_:
                       t[1].append(tokenPOS.text)
                       break
        if treenode_type=="tag":
            for t in sentence_PoS_tuple_array:
                print("t:",t)
                if t[0] == tokenPOS.tag_ and t[1] == []:
                    t[1].append(tokenPOS.text)
                    break
                else:
                    if t[0] == tokenPOS.tag_:
                        t[1].append(tokenPOS.text)
                        break
        remainingsentence+=1
        spaseePOS=spaseePOS[1:]
    print("make_sentence2(): sentence_PoS_tuple_array = ",sentence_PoS_tuple_array)
    allpossiblesentences=[]
    rwtexts=[]
    for t in sentence_PoS_tuple_array:
        if t[1] == []:
            allpossiblesentences.append([t[0]]) 
            #allpossiblesentences.append(["---"]) 
        else:
            allpossiblesentences.append(t[1]) 
    print("allpossiblesentences:",allpossiblesentences)
    for product in itertools.product(*allpossiblesentences):
        print("product:",product)
        rwtexts.append(" ".join(product))
    wsj = treebank.tagged_words()
    cfd2 = ConditionalFreqDist((tag, word) for (word, tag) in wsj)
    filledrwtexts=[]
    PennTreebankPoS={"CC":"Coordinating conjunction",
            "CD":"Cardinal number",
            "DT":"Determiner",
            "EX":"Existential there",
            "FW":"Foreign word",
            "IN":"Preposition or subordinating conjunction",
            "JJ":"Adjective",
            "JJR":"Adjective, comparative",
            "JJS":"Adjective, superlative",
            "LS":"List item marker",
            "MD":"Modal",
            "NN":"Noun, singular or mass",
            "NNS":"Noun, plural",
            "NNP":"Proper noun, singular",
            "NNPS":"Proper noun, plural",
            "PDT":"Predeterminer",
            "POS":"Possessive ending",
            "PRP":"Personal pronoun",
            "PRP$":"Possessive pronoun",
            "RB":"Adverb",
            "RBR":"Adverb, comparative",
            "RBS":"Adverb, superlative",
            "RP":"Particle",
            "SYM":"Symbol",
            "TO":"to",
            "UH":"Interjection",
            "VB":"Verb, base form",
            "VBD":"Verb, past tense",
            "VBG":"Verb, gerund or present participle",
            "VBN":"Verb, past participle",
            "VBP":"Verb, non-3rd person singular present",
            "VBZ":"Verb, 3rd person singular present",
            "WDT":"Wh-determiner",
            "WP":"Wh-pronoun",
            "WP$":"Possessive wh-pronoun",
            "WRB":"Wh-adverb"}
    number_of_sentences_synthesized=0
    for rwtext in rwtexts:
        if number_of_sentences_synthesized > max_synth_sentences:
            break
        filledrwtext=[]
        for rwtexttok in rwtext.split(" "):
            if user_defined_PoS2Vocabulary_dict is not None:
                print("rwtexttok:",rwtexttok)
                if rwtexttok in user_defined_PoS2Vocabulary_dict.keys():
                    closest_possible_tokens=get_closest_possible_tokens(rwtext.split(" "),user_defined_PoS2Vocabulary_dict[rwtexttok],max_words_per_PoS)
                    print("make_sentence2(): closest_possible_tokens = ",closest_possible_tokens)
                    filledrwtext.append(closest_possible_tokens)
                else:
                    filledrwtext.append(["---"])
            else:
                if rwtexttok in PennTreebankPoS.keys():
                    filledrwtext.append(list(cfd2[rwtexttok]))
                else:
                    filledrwtext.append([rwtexttok])
                    #filledrwtext.append(["---"])
        for x in filledrwtext:
            if x==[]:
                x.append("---")
        print("make_sentence2(): filledrwtext (without cartesian product) = ",filledrwtext)
        for product in itertools.product(*filledrwtext):
            #print("make_sentence2(): filled sentence template = "," ".join(product))
            filledrwtexts.append(" ".join(product))
            number_of_sentences_synthesized+=1
            if number_of_sentences_synthesized > max_synth_sentences:
                 break
    print("make_sentence2():filledrwtexts:",filledrwtexts)
    return filledrwtexts 

def get_closest_possible_tokens(rwtexttoks, vocabulary, max_words_per_PoS=1000,maximum_radius=10):
    closest_words_dict=defaultdict()
    print("get_closest_possible_tokens(): rwtexttoks = ",rwtexttoks)
    for rwtexttok in rwtexttoks:
        if rwtexttok in vocabulary:
            print("get_closest_possible_tokens(): rwtexttok = ",rwtexttok)
            for word in vocabulary[:max_words_per_PoS]:
                path=path_between(word,rwtexttok)
                if len(path) > 0 and len(path) < maximum_radius:
                    print("distance between ",word," and ",rwtexttok,":",len(path))
                    closest_words_dict[word]=len(path)
    print("closest_words_dict:",closest_words_dict)
    return list(closest_words_dict.keys())

def make_sentence(wordnetsynsets,sentence_type="xtag_node34_triplets",standard_sentence_PoS_dict={"ADJ":[],"PROPN":[],"NOUN":[],"AUX":[],"ADP":[],"ADV":[],"VERB":[],"DET":[],"PRON":[],"CCONJ":[],"NUM":[],"SYM":[],"X":[]},markblanks=False,edgelabels=None,enable_frege_projective_dependency_grammar=True,treenode_type="PoS"):
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
        if enable_frege_projective_dependency_grammar is True:
            conll_data=dependency_treebank.parsed_sents()
            conll_sentences=[]
            lexicon=[]
            for conll_sent in conll_data:
                conll_sentences.append(conll_sent.to_conll(3))
                #print("Penn Treebank conll sentence:",conll_sent.to_conll(3))
            graphs = [DependencyGraph(entry) for entry in conll_sentences if entry]
            print("Penn TreeBank - Number of dependency graphs trained:",len(graphs))
            for g in graphs:
                print("Penn Treebank Frege dependency graph as tree:",g.tree())
                lexicon += g.tree().leaves() 
            pdp = ProbabilisticProjectiveDependencyParser()
            #pdp = ProjectiveDependencyParser(g)
            print("Training the Probabilistic Projective Dependency Parser with Penn TreeBank dependency graphs....")
            pdp.train(graphs)
            dependencysentwords=[]
            print("dependency lexicon (gathered from leaves of Penn TreeBank):",lexicon)
            for w in wordnetsynsets:
                if w in lexicon:
                    dependencysentwords.append(w)
            print("dependencysentwords:",list(set(dependencysentwords)))
            pdpsentence=list(pdp.parse(list(set(dependencysentwords))))
            print("Most Probable Frege Projective Dependency Grammar sentence (might return nothing) :",pdpsentence)
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
            if treenode_type=="PoS":
                standard_sentence_PoS_dict[tokenPOS.pos_].append(tokenPOS.text)
            if treenode_type=="tag":
                standard_sentence_PoS_dict[tokenPOS.tag_].append(tokenPOS.text)
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

def create_sentence_PoS_dict_from_treebank(datasets=["wsj_0001.mrg","wsj_0002.mrg","wsj_0002.mrg","wsj_0003.mrg","wsj_0004.mrg","wsj_0005.mrg","wsj_0006.mrg"],returnasarray=False):
    list_of_sentence_PoS_dicts=[]
    list_of_sentence_PoS_tuple_arrays=[]
    for dataset in datasets:
        print("Dataset:",dataset)
        tbsents=treebank.parsed_sents(dataset)
        for t in tbsents:
            sentence_PoS_tuples=[]
            tpos=t.pos()
            print("tpos:",tpos)
            for pos in tpos:
              if pos[1] not in ['.', ',']:
                  sentence_PoS_tuples.append([pos[1],[]])
            sentence_PoS_dict=defaultdict(list)
            for k,v in sentence_PoS_tuples:
              sentence_PoS_dict[k]=v
            print("sentence_PoS_dict:",sentence_PoS_dict)
            print("-----------------")
            list_of_sentence_PoS_dicts.append(sentence_PoS_dict)
            list_of_sentence_PoS_tuple_arrays.append(sentence_PoS_tuples)
    print("List of sentence_PoS_dicts:",list_of_sentence_PoS_dicts)
    if returnasarray is False:
        return list_of_sentence_PoS_dicts
    else:
        return list_of_sentence_PoS_tuple_arrays

if __name__ == "__main__":
    question = sys.argv[1]
    #WikipediaRLFGTransformersQuestionAnswering(question,bothvertices_intersection=True,sentence_type="xtag_node34_triplets")
    #WikipediaRLFGTransformersQuestionAnswering(question,bothvertices_intersection=False,sentence_type="xtag_node34_triplets")
    #WikipediaRLFGTransformersQuestionAnswering(question,wsheading=True,answerslice=0.01,bothvertices_intersection=False,sentence_type="textgraph_random_walk",number_of_words_per_sentence=50,std_sentence_PoS_dict={"ADJ":[],"PROPN":[],"NOUN":[],"AUX":[],"ADP":[],"ADV":[],"VERB":[],"DET":[],"PRON":[],"CCONJ":[],"NUM":[],"SYM":[],"X":[],"PUNCT":[]},number_of_cores_per_random_walk=3,number_of_random_walks=3,blanks=False)
    
    print("----------------------- sentence synthesis (manual sentence_PoS_dict) --------------------")
    WikipediaRLFGTransformersQuestionAnswering(question,wsheading=True,answerslice=0.01,bothvertices_intersection=False,sentence_type="textgraph_random_walk",number_of_words_per_sentence=50,std_sentence_PoS_dict={"NUM":[],"ADJ":[],"PROPN":[],"NOUN":[],"PUNCT":[],"AUX":[],"ADP":[],"ADV":[],"VERB":[],"DET":[],"PRON":[],"CCONJ":[],"SYM":[],"X":[]},number_of_cores_per_random_walk=3,number_of_random_walks=3,blanks=False,treenode_type="PoS")

    conll2000_tagged_words=conll2000.tagged_words()
    print("conll2000_tagged_words:",conll2000_tagged_words)
    conll2000_corpus_PoS2Vocabulary_dict = ConditionalFreqDist((tag, word) for (word, tag) in conll2000_tagged_words)

    kaggle_corpus_PoS2Vocabulary_dict=defaultdict(list)
    with open('words_pos.csv', newline='') as wordsposcsv:
        wordsposreader = csv.reader(wordsposcsv, delimiter=',')
        for row in wordsposreader:
            print("row:",row)
            kaggle_corpus_PoS2Vocabulary_dict[row[2]].append(row[1])
    print("kaggle PoS corpus:",kaggle_corpus_PoS2Vocabulary_dict)

    print("----------------------- sentence synthesis (sentence_PoS_dict retrieved from treebank) --------------------")
    list_of_sentence_PoS_dicts=create_sentence_PoS_dict_from_treebank(datasets=["wsj_0092.mrg"])
    for sentencePoSdict in list_of_sentence_PoS_dicts[:1]:
        print("sentencePoSdict:",sentencePoSdict)
        #WikipediaRLFGTransformersQuestionAnswering(question,wsheading=True,answerslice=0.01,bothvertices_intersection=False,sentence_type="textgraph_random_walk",number_of_words_per_sentence=50,std_sentence_PoS_dict=sentencePoSdict,number_of_cores_per_random_walk=3,number_of_random_walks=3,blanks=False,treenode_type="tag",user_defined_PoS2Vocabulary_dict=conll2000_corpus_PoS2Vocabulary_dict)
        WikipediaRLFGTransformersQuestionAnswering(question,wsheading=True,answerslice=0.01,bothvertices_intersection=False,sentence_type="textgraph_random_walk",number_of_words_per_sentence=50,std_sentence_PoS_dict=sentencePoSdict,number_of_cores_per_random_walk=5,number_of_random_walks=3,blanks=False,treenode_type="tag",user_defined_PoS2Vocabulary_dict=kaggle_corpus_PoS2Vocabulary_dict)
        print("---------------------------------------------")

    print("----------------------- sentence synthesis (sentence_PoS_array retrieved from treebank) --------------------")
    list_of_sentence_PoS_arrays=create_sentence_PoS_dict_from_treebank(datasets=["wsj_0090.mrg"],returnasarray=True)
    for sentencePoSarray in list_of_sentence_PoS_arrays[:1]:
        print("sentencePoSarray:",sentencePoSarray)
        #WikipediaRLFGTransformersQuestionAnswering(question,wsheading=True,answerslice=0.01,bothvertices_intersection=False,sentence_type="textgraph_random_walk",number_of_words_per_sentence=10,std_sentence_PoS_dict={},number_of_cores_per_random_walk=5,number_of_random_walks=5,blanks=False,treenode_type="tag",sentence_tuple_array=True, sentence_PoS_array=sentencePoSarray, randomwalk_to_sentence_template_ratio=3,user_defined_PoS2Vocabulary_dict=conll2000_corpus_PoS2Vocabulary_dict)
        WikipediaRLFGTransformersQuestionAnswering(question,wsheading=True,answerslice=0.01,bothvertices_intersection=False,sentence_type="textgraph_random_walk",number_of_words_per_sentence=50,std_sentence_PoS_dict={},number_of_cores_per_random_walk=5,number_of_random_walks=5,blanks=False,treenode_type="tag",sentence_tuple_array=True, sentence_PoS_array=sentencePoSarray, randomwalk_to_sentence_template_ratio=3,user_defined_PoS2Vocabulary_dict=kaggle_corpus_PoS2Vocabulary_dict)
        print("---------------------------------------------")

    #WikipediaRLFGTransformersQuestionAnswering(question,wsheading=False,answerslice=0.5,bothvertices_intersection=False,sentence_type="knowledgegraph_random_walk",number_of_words_per_sentence=50,std_sentence_PoS_dict={"NUM":[],"ADJ":[],"PROPN":[],"NOUN":[],"PUNCT":[],"AUX":[],"ADP":[],"ADV":[],"VERB":[],"DET":[],"PRON":[],"CCONJ":[],"SYM":[],"X":[]},number_of_cores_per_random_walk=3,number_of_random_walks=3,blanks=False)
    #OpenAIQuestionAnswering(question)
