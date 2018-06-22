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
#-----------------------------------------------------------------------------------------------------------------------------------

from LSHIndex import LSHIndex
from ThoughtNetIndex import ThoughtNetIndex
from RecursiveLambdaFunctionGrowth import RecursiveLambdaFunctionGrowth
import sys
from pprint import pprint
import operator
import json

if __name__=="__main__":
	lsh_intrinsic_merit_ranking={}
	thoughtnet_intrinsic_merit_ranking={}
	lshindex=LSHIndex(50,50)
	thoughtnetindex=ThoughtNetIndex()
	rlfg=RecursiveLambdaFunctionGrowth()
	print "#############################################################"
	print "QueryAndRank: Querying Locality Sensitive Hashing Index for - ",sys.argv[1]
	print "#############################################################"
        crawled=open("/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/webspider/WebSpider-HTML.out","r")
        for sentence in crawled:
                lshindex.add(sentence)
	lshresults=lshindex.query_nearest_neighbours(sys.argv[1])
	print lshresults
	if lshresults is not None:
		for r in lshresults:
			intrinsic_merit_dict=rlfg.grow_lambda_function3(r[0].replace(u'\xa0', ' ').encode('utf-8'))
			print intrinsic_merit_dict
			lsh_intrinsic_merit_ranking[float(json.dumps(intrinsic_merit_dict["graph_tensor_neuron_network_intrinsic_merit"]))]=r
	lshindex.delete_index()
	print "#############################################################"
	print "QueryAndRank: Querying ThoughtNet Index for - ",sys.argv[1]
	print "#############################################################"
	thoughtnetresults=thoughtnetindex.query_index(sys.argv[1])
	print thoughtnetresults
	for r in thoughtnetresults:
		intrinsic_merit_dict=rlfg.grow_lambda_function3(r.replace(u'\xa0', ' ').encode('utf-8'))
		print intrinsic_merit_dict
		thoughtnet_intrinsic_merit_ranking[float(json.dumps(intrinsic_merit_dict["graph_tensor_neuron_network_intrinsic_merit"]))]=r
	sorted_lsh_intrinsic_merit_ranking=sorted(lsh_intrinsic_merit_ranking.items(),key=operator.itemgetter(0), reverse=True)
	sorted_thoughtnet_intrinsic_merit_ranking=sorted(thoughtnet_intrinsic_merit_ranking.items(),key=operator.itemgetter(0), reverse=True)
	print "==========================================================================="
	print "LSH Intrinsic Merit Ranking" 
	print "==========================================================================="
	pprint(sorted_lsh_intrinsic_merit_ranking)
	print "==========================================================================="
	print "ThoughtNet Intrinsic Merit Ranking" 
	print "==========================================================================="
	pprint(sorted_thoughtnet_intrinsic_merit_ranking)

