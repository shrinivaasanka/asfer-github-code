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

#Code derived from REBEL relation extraction boiler plate code documentation at https://huggingface.co/Babelscape/rebel-large

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import matplotlib.pyplot as plt 
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import spacy
import spacy_component 

def extract_triplets(text):
    triplets = []
    relation, subject, relation, object_ = '', '', '', ''
    text = text.strip()
    current = 'x'
    for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").split():
        if token == "<triplet>":
            current = 't'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
                relation = ''
            subject = ''
        elif token == "<subj>":
            current = 's'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
            object_ = ''
        elif token == "<obj>":
            current = 'o'
            relation = ''
        else:
            if current == 't':
                subject += ' ' + token
            elif current == 's':
                object_ += ' ' + token
            elif current == 'o':
                relation += ' ' + token
    if subject != '' and relation != '' and object_ != '':
        triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
    return triplets

def create_SpaCy_knowledge_graph(text):
    spacyrebel = spacy.load("en_core_web_sm")
    print("spacy-rebel loaded.....")
    spacyrebel.add_pipe("rebel", after="senter", config={
        'device':-1, 
        'model_name':'Babelscape/rebel-large'}
    )
    print("spacy-rebel add_pipe().....")
    doc = spacyrebel(text)
    print("doc:",doc)
    doc_list = spacyrebel.pipe([text])
    print("text:",text)
    print("doc_list:",doc_list)
    knowledgegraph=nx.DiGraph()
    edgelabels={}
    for value, rel_dict in doc._.rel.items():
         print(f"{value}: {rel_dict}")
         knowledgegraph.add_edge(rel_dict["head_span"],rel_dict["tail_span"],label=rel_dict["relation"]) 
         edgelabels[(str(rel_dict["head_span"]),str(rel_dict["tail_span"]))]=str(rel_dict["relation"])
    write_dot(knowledgegraph, "KnowledgeGraph.dot")
    lambda_functions_from_knowledge_graph(edgelabels)
    #nx.draw_networkx_edge_labels(knowledgegraph,pos=nx.spring_layout(knowledgegraph),edge_labels=edgelabels)
    #plt.show()
    return (knowledgegraph,edgelabels)

def create_REBEL_knowledge_graph(text):
    # Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained("Babelscape/rebel-large")
    model = AutoModelForSeq2SeqLM.from_pretrained("Babelscape/rebel-large")
    gen_kwargs = {
     "max_length": 256,
     "length_penalty": 0,
     "num_beams": 3,
     "num_return_sequences": 3,
    }

    # Tokenizer text
    model_inputs = tokenizer(text, max_length=256, padding=True, truncation=True, return_tensors = 'pt')

    # Generate
    generated_tokens = model.generate(
      model_inputs["input_ids"].to(model.device),
      attention_mask=model_inputs["attention_mask"].to(model.device),
      **gen_kwargs,
    )

    # Extract text
    decoded_preds = tokenizer.batch_decode(generated_tokens, skip_special_tokens=False)

    # Extract triplets
    for idx, sentence in enumerate(decoded_preds):
       print(f'Prediction triplets sentence {idx}:{sentence}')
       triplets=extract_triplets(sentence)

    knowledgegraph=nx.DiGraph()
    edgelabels={}
    for t in triplets:
         knowledgegraph.add_edge(t["head"],t["tail"],label=t["type"]) 
         edgelabels[(t["head"],t["tail"])]=t["type"]
    write_dot(knowledgegraph, "KnowledgeGraph.dot")
    lambda_functions_from_knowledge_graph(edgelabels)
    #nx.draw_networkx_edge_labels(knowledgegraph,pos=nx.spring_layout(knowledgegraph),edge_labels=edgelabels)
    #plt.show()
    return (knowledgegraph,edgelabels)

def lambda_functions_from_knowledge_graph(edgelabels):
    lambdafunctions = []
    for edge,relation in edgelabels.items():
        operand1 = edge[0]
        operand2 = edge[1]
        operator = relation 
        lambdafunction = operator + "(" + operand1 + "," + operand2 + ")" 
        lambdafunctions.append(lambdafunction)
    print("lambda functions:",lambdafunctions)
    return lambdafunctions

if __name__=="__main__":
    #create_REBEL_knowledge_graph("This is an example sentence for knowledge graph extraction")
    create_SpaCy_knowledge_graph("A large language model (LLM) is a computational model capable of language generation or other natural language processing tasks. As language models, LLMs acquire these abilities by learning statistical relationships from vast amounts of text during a self-supervised and semi-supervised training process.")
