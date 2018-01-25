/*********************************************************************************************************
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
#K.Srinivasan
#NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
#Personal website(research): https://sites.google.com/site/kuja27/
#--------------------------------------------------------------------------------------------------------
*********************************************************************************************************/

using namespace std;
#include <iostream>
#include <tr1/unordered_map>
#include <fstream>
#include "indexer.h"
#include "asferclassifiers.h"
#include "asferdataset_test.h"
#include "SVMRetriever.h"

#ifndef ASFERPARSER_H
#include "asferparser.h"
#endif

#include "retriever.h"
#include "asferencodestr.h"

#include "asferKnuthMorrisPrattStringMatch.h"

#include "asferpythonembedding.cpp"


extern "C" {
#include "string.h"
}

int asferrule::next_token_id = 0;

void read_asfer_config();


const char* strplanets[] = {"Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"};

std::string asferroot;
unordered_map<string,bool> config_map;

int main(int argc, char* argv[])
{
	string basepath("/home/shrinivaasanka/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/cpp-src");
	asferroot=basepath;
	std::cout<<"AStro inFER - Inference Software for Large Datasets " << std::endl;
	std::cout<<"-----------------------------------------------------" << std::endl;

	read_asfer_config();

	if(config_map["doClassification"])
	{
		doNaiveBayesAndDecisionTreeClassification();	
	}

	if(config_map["doTestDataSet"])
	{
		test_asferdataset();
	}

	if(config_map["parseDatasetAndPredict"])
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
		input.open("/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/KrishnaiResearch_OpenSource/GitHub/asfer-github-code/cpp-src/asfer.query", ifstream::in);
	
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
		if(config_map["doSVMRetrieve"])
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
	asferencodestr aestr;
	if(config_map["extractPatterns"])
	{
		cout<<"###########################################"<<endl;
		cout<<"pairwise and powerset pattern extraction"<<endl;
		cout<<"###########################################"<<endl;
		aestr.pairwiseCompAndExtractPatterns();
		aestr.allCompAndExtractPatterns();
		aestr.powerSetCompAndExtractPatterns();
	}
	if(config_map["doSequenceAlignment"])
	{
		cout<<"###########################################"<<endl;
		cout<<"Needleman Wunsch String Alignment"<<endl;
		cout<<"###########################################"<<endl;
		aestr.pairwiseNeedlemanWunshSequenceAlignment();
	}
	if(config_map["doDistance"])
	{
		cout<<"###########################################"<<endl;
		cout<<"Wagner-Fischer Edit Distance"<<endl;
		cout<<"###########################################"<<endl;
		aestr.computeWagnerFischerEditDistance();
	}

	if(config_map["doClustering"])
	{
		cout<<"############################################################"<<endl;
		cout<<"Clustering - Unsupervised - KMeans"<<endl;
		cout<<"############################################################"<<endl;
		aestr.clusterEncodedHoro("KMeans");
		cout<<"############################################################"<<endl;
		cout<<"Clustering -  Supervised - kNN"<<endl;
		cout<<"############################################################"<<endl;
		aestr.clusterEncodedHoro("kNN");
	}

	if(config_map["doLCS"])
	{
		aestr.longestCommonSubstring();
	}

	if(config_map["doStringMatch"])
	{
		asferKMPStringMatch akmpsm;
		string s1("KnuthMorrisPratt");
		string s2("Morri");
		int substrloc=akmpsm.KMPMatch(s1,s2);
		cout<<"############################################################"<<endl;
		cout<<"Knuth Morris Pratt String Match location for ["<<s1<<"] and ["<<s2<<"]:"<<substrloc<<endl;
		cout<<"############################################################"<<endl;
	}	

	if(config_map["doEmbedPython"])
	{
		asferpythonembedding ape;
		ape.execute_python_script(argv[1]);
	}

	if(config_map["enableCloudPerfectForwarding"])
        {
                cout<<"KingCobra - Cloud Perfect Forwarding C++ std::move client-server binaries invoked"<<endl;
                execl("/bin/sh", "sh", "-c", "/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/linux-4.1.5/drivers/kcobra/kingcobra_cloud_perfect_forwarding.sh", (char *) 0);
        }

}

void read_asfer_config()
{
        config_map["parseDatasetAndPredict"]=false;
	config_map["doClassification"]=false;
	config_map["doSVMRetrieve"]=false;
	config_map["doSequenceAlignment"]=false;
	config_map["doTestDataSet"]=false;
	config_map["doDistance"]=false;
	config_map["extractPatterns"]=false;
	config_map["doClustering"]=false;
	config_map["doLCS"]=false;
	config_map["doStringMatch"]=false;
	config_map["doEmbedPython"]=false;
	config_map["enableCloudPerfectForwarding"]=false;
	ifstream config;
	char line[256];
	config.open("./asfer.conf", ifstream::in);
	config.getline(line, 256);
	while(line != NULL && !config.eof())
	{
		string config_key(strtok(line, "="));
		string config_value(strtok(NULL, ";"));
		cout<<config_key<<":"<<config_value<<endl;
		config.getline(line, 256);
		config_map[config_key]=(config_value=="true")?true:false;
	}
}
