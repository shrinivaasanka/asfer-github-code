/*****************************************************************************************
--------------------------------------------------------------------------------------------------
ASFER - Inference Software for Large Datasets - component of iCloud Platform
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
---------------------------------------------------------------------------------------------------
Copyright (C):
Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
Ph: 9789346927, 9003082186, 9791165980
Krishna iResearch Open Source Products Profiles:
http://sourceforge.net/users/ka_shrinivaasan, https://www.openhub.net/accounts/ka_shrinivaasan
Personal website(research): https://sites.google.com/site/kuja27/
ZODIAC DATASOFT: https://github.com/shrinivaasanka/ZodiacDatasoft
emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
--------------------------------------------------------------------------------------------------
*****************************************************************************************/
#include <iostream>
#include <fstream>
#include "indexer.h"
#include "asferclassifiers.h"
#include "asferdataset_test.h"
#include "SVMRetriever.h"

#ifndef ASFERPARSER_H
#include "asferparser.h"
#endif

#include "retriever.h"
#include "asferencodehoro.h"

#include "asferKnuthMorrisPrattStringMatch.h"

#include "asferpythonembedding.cpp"


extern "C" {
#include "string.h"
}

int asferrule::next_token_id = 0;

bool parseDatasetAndPredict=false;
bool doClassification=false;
bool doSVMRetrieve=false;
bool doSequenceAlignment=false;
bool doTestDataSet=false;
bool doDistance=false;
bool extractPatterns=false;
bool doClustering=false;
bool doLCS=false;
bool doStringMatch=true;
bool doEmbedPython=true;

const char* strplanets[] = {"Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"};

std::string asferroot;

int main(int argc, char* argv[])
{
	string basepath("/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea22/home/kashrinivaasan/KrishnaiResearch_OpenSource/asfer-code/cpp-src");
	asferroot=basepath;
	std::cout<<"AStro inFER - Inference Software for Large Datasets " << std::endl;
	std::cout<<"-----------------------------------------------------" << std::endl;

	if(doClassification)
	{
		doNaiveBayesAndDecisionTreeClassification();	
	}

	if(doTestDataSet)
	{
		test_asferdataset();
	}

	if(parseDatasetAndPredict)
	{	
		asferindexer asindex ("asfer.rules");
	
		//index creation in-memory 
		//todo - create in-disk index and read into memory
		asindex.read_rule_corpus();
		asindex.create_index();
		asindex.print_index();
	
		//query and horoscope processing - query and horoscope are given in file asfer.query
		//asfer.query consists of 3 lines
		//	<lagna>
		//	<house1> <house2> ... <house12> (planet/planet/... per house)
		//	<query>

		ifstream input;
		Horoscope horo;
		char line[256];
		input.open("/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea22/home/kashrinivaasan/KrishnaiResearch_OpenSource/asfer-code/cpp-src/asfer.query", ifstream::in);
	
		input.getline(line, 256);
		horo.lagna = strdup(line);
		input.getline(line, 256);
		char* token = strtok(line, " ");
		int i=0;
		while(line != NULL && i < 12)
		{
			horo.houses[i] = strdup(token);
			token = strtok(NULL, " ");
			i++;
		}
			
		input.getline(line, 256);
		std::string query(line);
	
		retriever *retr = new retriever(&asindex);
		std::string* algo;
		if(doSVMRetrieve)
		{
			algo = new std::string("svm");
		}
		else
		{
			algo = new std::string("vectorspace");
		}
		std::list<weighted_asferrule>* results = retr->get_rules(query, *algo);
		asferparser asparser;
		std::string* prediction = asparser.parseAndPredict(*results, horo);
	
		cout<< "prediction" << endl;
		cout<< "----------" << endl;
		cout<< *prediction << endl;
	}
	asferencodehoro aehoro;
	if(extractPatterns)
	{
		cout<<"###########################################"<<endl;
		cout<<"pairwise and powerset pattern extraction"<<endl;
		cout<<"###########################################"<<endl;
		aehoro.pairwiseCompAndExtractPatterns();
		aehoro.allCompAndExtractPatterns();
		aehoro.powerSetCompAndExtractPatterns();
	}
	if(doSequenceAlignment)
	{
		cout<<"###########################################"<<endl;
		cout<<"Needleman Wunsch String Alignment"<<endl;
		cout<<"###########################################"<<endl;
		aehoro.pairwiseNeedlemanWunshSequenceAlignment();
	}
	if(doDistance)
	{
		cout<<"###########################################"<<endl;
		cout<<"Wagner-Fischer Edit Distance"<<endl;
		cout<<"###########################################"<<endl;
		aehoro.computeWagnerFischerEditDistance();	
	}

	if(doClustering)
	{
		cout<<"############################################################"<<endl;
		cout<<"Clustering - Unsupervised - KMeans"<<endl;
		cout<<"############################################################"<<endl;
		aehoro.clusterEncodedHoro("KMeans");
		cout<<"############################################################"<<endl;
		cout<<"Clustering -  Supervised - kNN"<<endl;
		cout<<"############################################################"<<endl;
		aehoro.clusterEncodedHoro("kNN");
	}

	if(doLCS)
	{
		aehoro.longestCommonSubstring();
	}

	if(doStringMatch)
	{
		asferKMPStringMatch akmpsm;
		string s1("KnuthMorrisPratt");
		string s2("Morri");
		int substrloc=akmpsm.KMPMatch(s1,s2);
		cout<<"############################################################"<<endl;
		cout<<"Knuth Morris Pratt String Match location for ["<<s1<<"] and ["<<s2<<"]:"<<substrloc<<endl;
		cout<<"############################################################"<<endl;
	}	

	if(doEmbedPython)
	{
		asferpythonembedding ape;
		ape.execute_python_script(argv[1]);
	}
}
