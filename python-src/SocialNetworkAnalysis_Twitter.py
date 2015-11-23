#-------------------------------------------------------------------------------------------------------
#ASFER - Software for Mining Large Datasets 
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
#Copyright (C):
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Ph: 9789346927, 9003082186, 9791165980
#Krishna iResearch Open Source Products Profiles: 
#http://sourceforge.net/users/ka_shrinivaasan, https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#ZODIAC DATASOFT: https://github.com/shrinivaasanka/ZodiacDatasoft
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
#--------------------------------------------------------------------------------------------------------

#Get Twitter Streaming Data - python-twitter - https://github.com/bear/python-twitter

import twitter
import pprint
import json
import Queue
import operator
import networkx as nx
import matplotlib.pyplot as plt
import SentimentAnalyzer

class SNA_Twitter:
	def __init__(self):
		#OAuth Authentication
		self.userq=Queue.Queue()	
		self.no_of_vertices=0
		self.tng=nx.DiGraph()
		self.api=twitter.Api(consumer_key="VLJl4Z0Wod88kE9nDTxF4sUxF",consumer_secret="Z3lzXjOLrTlOVmm5LXWHDf4MumeSG7Ln4TYSUIM00pdCuCzCTB",access_token_key="14233931-y4scOFQjzPICrCka5g79Tk9XGYWdn0433j49XkBzI",access_token_secret="i3poXTKyKotGQNlNk7sbqidraUb0qczEq2VHDREN35MsJ")
		print self.api.VerifyCredentials()
		for k in self.api.GetFollowers():
			self.userq.put(k)
			self.no_of_vertices+=1


	#build a graph recursively using a depth-first queue of followers
	def buildGraphFromTwitterFollowing(self):
		while True:
			twitter_id=self.userq.get()
		        #print "======================================"
			twitter_id_dict=json.loads(twitter_id.AsJsonString())
			#print twitter_id_dict["name"]
		        #print i.AsJsonString()
		        #pprint.pprint(i.GetCreatedAt())
		        #pprint.pprint(i.GetGeo())
		        #pprint.pprint(i.GetLocation())
		        #pprint.pprint(i.GetText())
			for f in self.api.GetFollowers(twitter_id):
				try:
					follower_id_dict=json.loads(f.AsJsonString())
					#print follower_id_dict["name"]
					self.tng.add_edge(twitter_id_dict["name"],follower_id_dict["name"])
					self.userq.put(f)	
					self.no_of_vertices+=1
				except:
					pass
			if self.no_of_vertices > 50:
				break
			print "======================================"
		nx.shell_layout(self.tng)
		nx.draw_networkx(self.tng)
		print "==========================================================================================="
		print "Bonacich Power Centrality of the Social Network (Twitter) Crawled - computed using PageRank"
		print "(a degree centrality based on social prestige)"
		print "==========================================================================================="
		print sorted(nx.pagerank(self.tng).items(),key=operator.itemgetter(1),reverse=True)
		print "==========================================================================================="
		print "Eigen Vector Centrality"
		print "==========================================================================================="
		print nx.eigenvector_centrality(self.tng)
		plt.show()

	#do Sentiment Analysis on tweets
	def followersTweetsSentimentAnalyzer(self):
		self.no_of_vertices=0
		print "================================"
		print "followersTweetsSentimentAnalyzer()"
		print "================================"
		while True:
			twitter_id=self.userq.get()
			if twitter_id is None:
				break
			print twitter_id.GetId()
			for f in self.api.GetFollowers(twitter_id):
				self.userq.put(f)	
				self.no_of_vertices+=1
				if self.no_of_vertices > 50:
					break
				jsontweet=json.loads(f.AsJsonString())
				try:
					statustext=jsontweet["status"]["text"]
				except KeyError:
					continue
				if statustext:
					print "==========================================="
					print "Sentiment analysis of twitter text:",statustext
					posscore,negscore,objscore=SentimentAnalyzer.SentimentAnalysis_SentiWordNet(statustext)
					print "Positivity:",posscore
					print "Negativity:",negscore
					print "Objectivity:",objscore

	#do Tweet Stream Sentiment Analysis
	def tweetStreamSentimentAnalyzer(self,query,algorithm):
		print "========================================="
		print "tweetStreamSentimentAnalyzer()"
		print "========================================="
		search=self.api.GetStreamFilter(track=[query])
		for i in search:
			print "tweet: ",i["text"]
                        if algorithm=="RGO_Belief_Propagation":
				outputfile = 'Output-Tweet-RGO-BeliefPropagation-SentimentAnalysis.txt'
				output = open(outputfile, 'w')
                                nxg=SentimentAnalyzer.SentimentAnalysis_RGO(i["text"],output)
                                print "=================================================================================="
                                print "Sentiment Analysis (Belief Propagation of Sentiment in the RGO graph) of the tweet"
                                print "=================================================================================="
                                dfs_belief_propagated_posscore, dfs_belief_propagated_negscore, core_belief_propagated_posscore, core_belief_propagated_negscore = SentimentAnalyzer.SentimentAnalysis_RGO_Belief_Propagation(nxg)
                                print "K-Core DFS belief_propagated_posscore:",float(dfs_belief_propagated_posscore)
                                print "K-Core DFS belief_propagated_negscore:",float(dfs_belief_propagated_negscore)
                                print "Core Number belief_propagated_posscore:",float(core_belief_propagated_posscore)
                                print "Core Number belief_propagated_negscore:",float(core_belief_propagated_negscore)
                        else:
                                posscore,negscore,objscore=SentimentAnalyzer.SentimentAnalysis_SentiWordNet(i["text"].encode("utf-8"))
                                print "=================================================================================="
                                print "Sentiment Analysis (trivial - SentiWordNet summation) of the tweet"
                                print "=================================================================================="
                                print "Positivity:",posscore
                                print "Negativity:",negscore
                                print "Objectivity:",objscore

#tweet_type: 0 for streams, 1 for followers
tweet_type=0
snat=SNA_Twitter()
snat.buildGraphFromTwitterFollowing()
if tweet_type:
	snat.followersTweetsSentimentAnalyzer()
else:
	#snat.tweetStreamSentimentAnalyzer("Chennai","RGO_Belief_Propagation")
	#snat.tweetStreamSentimentAnalyzer("elections","RGO_Belief_Propagation")
	snat.tweetStreamSentimentAnalyzer("Computer Science","RGO_Belief_Propagation")
