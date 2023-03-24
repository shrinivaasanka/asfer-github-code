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

from GoogleNews import GoogleNews
from newspaper import Article
import pandas
from textblob import TextBlob
import SentimentAnalyzer

def sentiment_analyzer(text,algorithm=None):
    if algorithm=="RGO_Belief_Propagation":
         outputfile = 'Opinion-RGO-BeliefPropagation-SentimentAnalysis.txt'
         output = open(outputfile, 'w')
         nxg=SentimentAnalyzer.SentimentAnalysis_RGO(text,output)
         print("==================================================================================")
         print("Sentiment Analysis (Belief Propagation of Sentiment in the RGO graph) of the opinion")
         print("==================================================================================")
         dfs_belief_propagated_posscore, dfs_belief_propagated_negscore, core_belief_propagated_posscore, core_belief_propagated_negscore = SentimentAnalyzer.SentimentAnalysis_RGO_Belief_Propagation(nxg)
         print("K-Core DFS belief_propagated_posscore:",float(dfs_belief_propagated_posscore))
         print("K-Core DFS belief_propagated_negscore:",float(dfs_belief_propagated_negscore))
         print("Core Number belief_propagated_posscore:",float(core_belief_propagated_posscore))
         print("Core Number belief_propagated_negscore:",float(core_belief_propagated_negscore))
    if algorithm=="RGO_Belief_Propagation_MRF":
         outputfile = 'Opinion-RGO-MRF-BeliefPropagation-SentimentAnalysis.txt'
         output = open(outputfile, 'w')
         nxg=SentimentAnalyzer.SentimentAnalysis_RGO(text,output)
         posscore,negscore,objscore=SentimentAnalyzer.SentimentAnalysis_RGO_Belief_Propagation_MarkovRandomFields(nxg)
         print("==================================================================================")
         print("Sentiment Analysis (Markov Random Fields Cliques Belief Propagation) of the opinion")
         print("==================================================================================")
         print("Positivity:",posscore)
         print("Negativity:",negscore)
         print("Objectivity:",objscore)
    if algorithm=="TextBlob":
         textblobsummary=TextBlob(text)
         print("==================================================================================")
         print("Sentiment Analysis (trivial - TextBlob) of the opinion")
         print("==================================================================================")
         print(textblobsummary.sentiment)
    if algorithm=="SentiWordNet":
         print("==================================================================================")
         print("Sentiment Analysis (trivial - SentiWordNet summation) of the opinion")
         print("==================================================================================")
         posscore,negscore,objscore=SentimentAnalyzer.SentimentAnalysis_SentiWordNet(text)
         print("Positivity:",posscore)
         print("Negativity:",negscore)
         print("Objectivity:",objscore)

def opinion_mining(query,fromdate,todate,maxpages=2,maxarticles=1):
    gn=GoogleNews(start=fromdate,end=todate)
    gn.search(query)
    opinion=[]
    summarizedopinion=""
    noofarticles=0
    for page in range(maxpages):
        gn.getpage(page)
        results=gn.result()
        df=pandas.DataFrame(results)
        for index in df.index:
            newsjson={}
            try:
                if noofarticles==maxarticles:
                    break
                noofarticles+=1
                article=Article(df['link'][index])
                article.download()
                article.parse()
                article.nlp()
                newsjson['Date']=df['date'][index]
                newsjson['Media']=df['media'][index]
                newsjson['Title']=article.title
                newsjson['Article']=article.text
                #print(article.text)
                newsjson['Summary']=article.summary
                sentiment_analyzer(article.summary,algorithm="SentiWordNet")
                sentiment_analyzer(article.summary,algorithm="TextBlob")
                sentiment_analyzer(article.summary,algorithm="RGO_Belief_Propagation")
                sentiment_analyzer(article.summary,algorithm="RGO_Belief_Propagation_MRF")
                sentiment_analyzer(article.summary)
                opinion.append(newsjson)
                summarizedopinion+= " " + article.summary
            except Exception as ex:
                print(ex)
    opiniondf=pandas.DataFrame(opinion)
    print(opiniondf)
    print("summarizedopinion:",summarizedopinion)
    return opiniondf

if __name__=="__main__":
    opinion_mining("Chennai Metropolitan Area Expansion","27/02/2023","01/03/2023")


