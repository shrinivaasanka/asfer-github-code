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
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from empath import Empath
from pytrends.request import TrendReq
from bs4 import BeautifulSoup 
import requests
from collections import defaultdict

def sentiment_analyzer(text,algorithm=None):
    vote=0.0
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
         vote=(float(dfs_belief_propagated_posscore) - float(dfs_belief_propagated_negscore) + float(core_belief_propagated_posscore) - float(core_belief_propagated_negscore),{"dfs_bp_pos":float(dfs_belief_propagated_posscore) , "dfs_bp_pos":float(dfs_belief_propagated_negscore) , "core_bp_pos":float(core_belief_propagated_posscore) , "core_bp_neg":float(core_belief_propagated_negscore)})
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
         vote=(posscore-negscore+objscore,{"pos":posscore,"neg":negscore,"obj":objscore})
    if algorithm=="TextBlob":
         textblobsummary=TextBlob(text)
         print("==================================================================================")
         print("Sentiment Analysis (trivial - TextBlob) of the opinion")
         print("==================================================================================")
         print(textblobsummary.sentiment)
         vote=(textblobsummary.sentiment.polarity+textblobsummary.sentiment.subjectivity,{"polarity":textblobsummary.sentiment.polarity,"subjectivity":textblobsummary.sentiment.subjectivity})
    if algorithm=="SentiWordNet":
         print("==================================================================================")
         print("Sentiment Analysis (trivial - SentiWordNet summation) of the opinion")
         print("==================================================================================")
         posscore,negscore,objscore=SentimentAnalyzer.SentimentAnalysis_SentiWordNet(text)
         print("Positivity:",posscore)
         print("Negativity:",negscore)
         print("Objectivity:",objscore)
         vote=(posscore-negscore+objscore,{"pos":posscore,"neg":negscore,"obj":objscore})
    if algorithm=="VADER":
         senti=SentimentIntensityAnalyzer()
         sentiscores=senti.polarity_scores(text)
         votescores=0
         print("VADER sentiment:",sentiscores)
         vote=(sentiscores['pos']-sentiscores['neg']+sentiscores['neu']+sentiscores['compound'],sentiscores)
    if algorithm=="empath":
         empathsenti=Empath()
         empathdict=empathsenti.analyze(text,normalize=True)
         maxvaluecategory=max(empathdict,key=empathdict.get)
         print("Empath sentiment:",maxvaluecategory)
         vote=(empathdict[maxvaluecategory],empathdict)
    return vote

def opinion_mining(query,fromdate,todate,maxpages=2,maxarticles=10,articlefraction=0.2,UseNeuronRainSentimentAnalyzer=False):
    gn=GoogleNews(start=fromdate,end=todate)
    gn.search(query)
    opinion=[]
    summarizedopinion=""
    noofarticles=0
    populationsample=0
    totalvotes=0
    multipolarvotes=[]
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
                articleslice=int(articlefraction*len(article.summary))
                print("articleslice:",article.summary[:articleslice])
                votesw=sentiment_analyzer(article.summary[:articleslice],algorithm="SentiWordNet")
                votetb=sentiment_analyzer(article.summary[:articleslice],algorithm="TextBlob")
                votergobp=sentiment_analyzer(article.summary[:articleslice],algorithm="RGO_Belief_Propagation")
                votergobpmrf=sentiment_analyzer(article.summary[:articleslice],algorithm="RGO_Belief_Propagation_MRF")
                votevader=sentiment_analyzer(article.summary[:articleslice],algorithm="VADER")
                voteempath=sentiment_analyzer(article.summary[:articleslice],algorithm="empath")
                multipolarvotes.append((votesw,votetb,votergobp,votergobpmrf,votevader,voteempath))
                populationsample+=1
                if UseNeuronRainSentimentAnalyzer:
                    voteensemble=float(votesw[0]+votetb[0]+votergobp[0]+votergobpmrf[0]+votevader[0]+voteempath[0])/6.0
                else:
                    voteensemble=float(votetb[0]+votevader[0]+voteempath[0])/3.0
                totalvotes+=voteensemble
                opinion.append(newsjson)
                summarizedopinion+= " " + article.summary[:articleslice]
            except Exception as ex:
                print(ex)
    opiniondf=pandas.DataFrame(opinion)
    print(opiniondf)
    print("summarizedopinion:",summarizedopinion)
    print("Opinion mining - multipolar electronic voting machine ballots - votes array for the query [",query,"] for population of size ",populationsample,":",multipolarvotes)
    print("Opinion mining - polled votes (average of objective-subjective(positive and negative) scores) on the query [",query,"] for population of size ",populationsample,":",totalvotes)
    return opiniondf

def opinion_mining_from_google_trends(query=None,fromdate='01/01/2023',todate='01/03/2023',maxtrends=2,region='IN'):
    pytrends = TrendReq(hl='en-US',tz=360)
    if query is not None:
        pytrends.build_payload(kw_list=[query])
    #df1=pytrends.trending_searches(pn='india')
    #print("trending google searches:",df1.head())
    df2=pytrends.realtime_trending_searches(pn=region)
    print("trending realtime google searches:",df2.head())
    #for q in df1.values.tolist()[:maxtrends]:
    #    print("query:",q[0])
    #    opinion_mining(q[0],"01/03/2023","29/03/2023",maxarticles=5)
    for q in df2.values.tolist()[:maxtrends]:
        print("query:",q[0])
        opinion_mining(q[0],fromdate,todate,maxarticles=2)

def opinion_mining_from_url(url):
    print("---------------------------------------------------------------------------------------------------")
    print("Opinion mined from URL (specialized to capture Tweets in https://twitter.com/i/trends format):",url)
    print("---------------------------------------------------------------------------------------------------")
    r = requests.get(url)    
    bs=BeautifulSoup(r.text,"html.parser")
    text=bs.get_text()
    tweetdict=defaultdict()
    numberoftweets=-1
    for line in text.split("\n"):
        linetoks=line.split()
        if "Tweets" in linetoks:
            print("Number of tweets:",linetoks[0])
            numberoftweets=linetoks[0]
        if "Tweet" in linetoks:
            print("Trending tweet:",linetoks[1])
            tweetdict[linetoks[1]]=numberoftweets
            numberoftweets=-1
            sentiment_analyzer(linetoks[1],algorithm="VADER")
        if "Trending" in linetoks and "since" in linetoks:
            print("-----------------",line)
    print("Votes for tweets - tweetdict:",tweetdict)

if __name__=="__main__":
    #opinion_mining("Chennai Metropolitan Area Expansion","27/02/2023","01/03/2023")
    #opinion_mining("Stock market volatility","01/01/2023","01/03/2023")
    opinion_mining_from_google_trends(fromdate="01/06/2023",todate="09/06/2023")
    opinion_mining_from_url("https://trendlistz.com/india")
    #opinion_mining_from_url("https://twitter.com/i/trends")
    #opinion_mining("Karnataka assembly elections Congress","01/01/2023","01/04/2023")
    #opinion_mining("Karnataka assembly elections BJP","01/01/2023","01/04/2023")


