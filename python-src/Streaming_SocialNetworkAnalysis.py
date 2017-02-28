#-------------------------------------------------------------------------------------------------------
#NEURONRAIN ASFER - Software for Mining Large Datasets
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------------
#Copyleft (Copyright+):
#Srinivasan Kannan
#(also known as: Shrinivaasan Kannan, Shrinivas Kannan)
#Ph: 9791499106, 9003082186
#Krishna iResearch Open Source Products Profiles:
#http://sourceforge.net/users/ka_shrinivaasan,
#https://github.com/shrinivaasanka,
#https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com,
#kashrinivaasan@live.com
#---------------------------------------------------------------------------------------------------------

import Streaming_AbstractGenerator
import SentimentAnalyzer

#algorithm="RGO_Belief_Propagation"
#algorithm="SentiWordNet"
algorithm="RGO_Belief_Propagation_MRF"

#inputf=open("StreamingData.txt","r")
#inputf=Streaming_AbstractGenerator.StreamAbsGen("USBWWAN_stream","USBWWAN")
#inputf=Streaming_AbstractGenerator.StreamAbsGen("file","file")
inputf=Streaming_AbstractGenerator.StreamAbsGen("Spark_Parquet","Spark_Streaming")
for i in inputf:
	if algorithm=="RGO_Belief_Propagation":
		outputfile = 'Output-SocialNetwork-RGO-BeliefPropagation-SentimentAnalysis.txt'
                output = open(outputfile, 'w')
                nxg=SentimentAnalyzer.SentimentAnalysis_RGO(i,output)
                print "====================================================================================================="
                print "Sentiment Analysis (Belief Propagation of Sentiment in the RGO graph) of the social network excerpt "
                print "====================================================================================================="
                dfs_belief_propagated_posscore, dfs_belief_propagated_negscore, core_belief_propagated_posscore, core_belief_propagated_negscore = SentimentAnalyzer.SentimentAnalysis_RGO_Belief_Propagation(nxg)
                print "K-Core DFS belief_propagated_posscore:",float(dfs_belief_propagated_posscore)
                print "K-Core DFS belief_propagated_negscore:",float(dfs_belief_propagated_negscore)
                print "Core Number belief_propagated_posscore:",float(core_belief_propagated_posscore)
                print "Core Number belief_propagated_negscore:",float(core_belief_propagated_negscore)
	if algorithm=="RGO_Belief_Propagation_MRF":
                outputfile = 'Output-SocialNetwork-RGO-BeliefPropagation-SentimentAnalysis.txt'
                output = open(outputfile, 'w')
                nxg=SentimentAnalyzer.SentimentAnalysis_RGO(i,output)
                posscore,negscore,objscore=SentimentAnalyzer.SentimentAnalysis_RGO_Belief_Propagation_MarkovRandomFields(nxg)
                print "==================================================================================================="
                print "Sentiment Analysis (Markov Random Fields Cliques Belief Propagation) of the social network excerpt "
                print "==================================================================================================="
                print "Positivity:",posscore
                print "Negativity:",negscore
                print "Objectivity:",objscore
	else:
                posscore,negscore,objscore=SentimentAnalyzer.SentimentAnalysis_SentiWordNet(i)
                print "=================================================================================="
                print "Sentiment Analysis (trivial - SentiWordNet summation) of the social network excerpt"
                print "=================================================================================="
                print "Positivity:",posscore
                print "Negativity:",negscore
                print "Objectivity:",objscore
