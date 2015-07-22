#-------------------------------------------------------------------------------------------------------------------------------------
#ASFER - AstroInfer - a classification,inference and predictive modelling software for mining patterns in Massive Data Sets, at present
#                       specialized for Astronomy DataSets
# 
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
#
#-----------------------------------------------------------------------------------------------------------------------------------
#Copyright (C): 
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Independent Open Source Developer, Researcher and Consultant
#Ph: 9003082186, 9791165980
#Open Source Products Profile(Krishna iResearch): http://sourceforge.net/users/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
#-----------------------------------------------------------------------------------------------------------------------------------

#Partitions the parsed datasets which contain date-time-long-lat data based on classifier output grepped
#by the invoker shell script - asfer_dataset_segregator.sh -  and writes the names of parsed dataset files into
#text files with names of regular expression "EventClassDataSet_<class>.txt"

f=open("./datasets_classified.txt","r")
alldatasets=open("./articlesdataset.txt","r")
allparseddatasets=open("./pygen_parsedarticlesdataset.txt","r")
class2datasetsdict={}
articleid2datasetdict={}
dataset2parseddatasetdict={}
for line in allparseddatasets:
	linetoks=line.split()
	dataset2parseddatasetdict[linetoks[0]]=linetoks[1]
articleid=1
for line in alldatasets:
	articleid2datasetdict[str(articleid)]=line
	articleid=articleid+1
print articleid2datasetdict

for line in f:
	linetoks=line.split()
	class2datasetsdict[linetoks[7]]=[]
f=open("./datasets_classified.txt","r")
for line in f:
	linetoks=line.split()
	class2datasetsdict[linetoks[7]]=class2datasetsdict[linetoks[7]]+ [linetoks[2]]
print class2datasetsdict
for k,v in class2datasetsdict.items():
	f=open("EventClassDataSet_"+k+".txt", "w")
	for value in v:
		f.write(dataset2parseddatasetdict[articleid2datasetdict[value].strip()]+"\n")

