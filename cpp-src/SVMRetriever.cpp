/***************************************************************************************
ASFER - a ruleminer which gets rules specific to a query and executes them

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
Independent Open Source Developer, Researcher and Consultant
Ph: 9003082186, 9791165980
Open Source Products Profile(Krishna iResearch): http://sourceforge.net/users/ka_shrinivaasan
Personal website(research): https://sites.google.com/site/kuja27/
emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
---------------------------------------------------------------------------------------------------
*****************************************************************************************/
#ifndef SVMRETRIEVER_H
#include "SVMRetriever.h"
#endif

#include <fstream>
#ifndef ASFERRULE_H
#include "asferrule.h"
#endif

#ifndef INDEXER_H
#include "indexer.h"
#endif

extern "C"
{
#include "stdlib.h"
#include "string.h"
}

SVMRetriever::SVMRetriever(asferindexer* ai)
{
	index = ai;
}

std::list<weighted_asferrule>* SVMRetriever::get_rules(std::string query)
{
	create_class_models();
	write_test_dat();
	classify_corpus();
	char* query_class = classify_query(query);
	std::list<asferrule>* rules = find_relevant_rules_for_query_class(query_class);
	
	std::list<weighted_asferrule> weighted_rules;
	for(std::list<asferrule>::iterator it= rules->begin(); it != rules->end(); it++)
	{
		weighted_asferrule w;
		w.asr = &(*it);
		weighted_rules.push_back(w);
	}
	
	return &weighted_rules;	
}

std::list<asferrule>* SVMRetriever::find_relevant_rules_for_query_class(char* query_class)
{
	int threshold = 0;
	std::list<asferrule> rules;
	ifstream svm_output;
	char line[256];
	char* tail;
	char* svm_output_file = strcat("output_", query_class);
	svm_output.open(svm_output_file);
	std::list<asferrule>& corpus = index->get_rule_corpus();
	std::list<asferrule>::iterator corpus_it = corpus.begin();
	while(svm_output.good() && corpus_it != corpus.end())
	{
		svm_output.getline(line, 256);
		int relevance = strtol(line, &tail, 0);
		if(relevance > threshold)
			rules.push_back(*corpus_it);
		corpus_it++;
	}
	return &rules;
}

char* SVMRetriever::find_query_class()
{
	int maximum = -10000;
	char line[256];
	char* tail;
	char* query_class;
	char* classes[] = {"tanu", "dhana", "sahaja", "matru", "putra", "roga", "yuti", "rina", "dharma", "karma", "labha", "vyaya"};
	for(int i=0; i < 12; i++)
	{
		ifstream svm_output;
		char* svm_output_file = strcat("query_output_", classes[i]);
		svm_output.open(svm_output_file);
		svm_output.getline(line, 256);
		int relevance = strtol(line, &tail, 0);
		if(relevance > maximum)
		{
			maximum = relevance;
			query_class = classes[i];
		}
	}
	return query_class;

} 

void SVMRetriever::create_class_models()
{
	//12 hardcoded classes with training files for each
	system("svm_learn train_tanu.dat model_tanu.dat");
	system("svm_learn train_dhana.dat model_dhana.dat");
	system("svm_learn train_sahaja.dat model_sahaja.dat");
	system("svm_learn train_matru.dat model_matru.dat");
	system("svm_learn train_putra.dat model_putra.dat");
	system("svm_learn train_roga.dat model_roga.dat");
	system("svm_learn train_yuti.dat model_yuti.dat");
	system("svm_learn train_rina.dat model_rina.dat");
	system("svm_learn train_dharma.dat model_dharma.dat");
	system("svm_learn train_karma.dat model_karma.dat");
	system("svm_learn train_labha.dat model_labha.dat");
	system("svm_learn train_vyaya.dat model_vyaya.dat");
}

void SVMRetriever::write_test_dat()
{
	std::list<asferrule>& corpus = index->get_rule_corpus();
	for(std::list<asferrule>::iterator rule_it= corpus.begin(); rule_it != corpus.end(); rule_it++)
	{
		rule_it->make_VSR();
		rule_it->write_VSR("test.dat");
	}
}

void SVMRetriever::classify_corpus()
{
	//12 hardcoded classes with model files for each
	//each output_<class>.dat splits the rule corpus into relevant(+ve line) and non-relevant(-ve line) rules for that class

	system("svm_classify test.dat model_tanu.dat output_tanu.dat");
	system("svm_classify test.dat model_dhana.dat output_dhana.dat");
	system("svm_classify test.dat model_sahaja.dat output_sahaja.dat");
	system("svm_classify test.dat model_matru.dat output_matru.dat");
	system("svm_classify test.dat model_putra.dat output_putra.dat");
	system("svm_classify test.dat model_roga.dat output_roga.dat");
	system("svm_classify test.dat model_yuti.dat output_yuti.dat");
	system("svm_classify test.dat model_rina.dat output_rina.dat");
	system("svm_classify test.dat model_dharma.dat output_dharma.dat");
	system("svm_classify test.dat model_karma.dat output_karma.dat");
	system("svm_classify test.dat model_labha.dat output_labha.dat");
	system("svm_classify test.dat model_vyaya.dat output_vyaya.dat");
}

char* SVMRetriever::classify_query(std::string& query)
{
	asferrule query_rule(query);
	query_rule.make_VSR();
	query_rule.write_VSR("query.dat");
	system("svm_classify query.dat model_tanu.dat query_output_tanu.dat");
	system("svm_classify query.dat model_dhana.dat query_output_dhana.dat");
	system("svm_classify query.dat model_sahaja.dat query_output_sahaja.dat");
	system("svm_classify query.dat model_matru.dat query_output_matru.dat");
	system("svm_classify query.dat model_putra.dat query_output_putra.dat");
	system("svm_classify query.dat model_roga.dat query_output_roga.dat");
	system("svm_classify query.dat model_yuti.dat query_output_yuti.dat");
	system("svm_classify query.dat model_rina.dat query_output_rina.dat");
	system("svm_classify query.dat model_dharma.dat query_output_dharma.dat");
	system("svm_classify query.dat model_karma.dat query_output_karma.dat");
	system("svm_classify query.dat model_labha.dat query_output_labha.dat");
	system("svm_classify query.dat model_vyaya.dat query_output_vyaya.dat");
	char* qclass = find_query_class();
	return qclass;
}



