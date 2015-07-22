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

#include <iostream>
#include <fstream>
#include <list>
#include "NaiveBayesClassifier.h"
#include "DecisionTreeClassifier.h"

using namespace std;

void doNaiveBayesAndDecisionTreeClassification()
{

	NaiveBayesClassifier nb_classifier;
	std::list<int> testset;
	ifstream testsettxt;
	cout << "---------------------------------------" << endl;
	cout << "1 -- NAIVE BAYESIAN CLASSIFIER running" << endl;
	cout << "---------------------------------------" << endl;

	testsettxt.open("test-set.txt", ifstream::in);
	char line[256];
	char *tail;
	testsettxt.getline(line, 256);
	while(testsettxt.good())
	{
		int article_id = strtol(line, &tail, 0);
		testset.push_back(article_id);
		testsettxt.getline(line, 256);
	}

	cout << "NAIVE BAYESIAN CLASSIFIER RESULTS" << endl;
	cout << "---------------------------------" << endl;
	nb_classifier.doNBMultinomialClassification(testset);
	cout << "---------------------------------------" << endl;
	cout << "2 -- DECISION TREE CLASSIFIER running" << endl;
	cout << "---------------------------------------" << endl;

	DecisionTreeClassifier dt_classifier;
	ifstream dttrainingset;
	ifstream dttestset;
	const std::vector<attr_set*>* decisionset = dt_classifier.readTrainingSet();
	dttrainingset.open("decisiontree-training.txt", ifstream::in);
	dttestset.open("decisiontree-test.txt", ifstream::in);
	dttrainingset.getline(line, 256);
	char* line2 = strdup(line);
	char* token = strtok(line, " ");
	int no_of_attrs=0;
	while(token != NULL)
	{
		no_of_attrs++;
		token = strtok(NULL, " ");
	}
	char attr_names[no_of_attrs][256];
	token = strtok(line2, " ");
	int i=0;
	while(token != NULL && i < no_of_attrs)
	{
		strcpy(attr_names[i], token);
		i++;
		token = strtok(NULL, " ");
	}	
	dt_classifier.decisionTree(decisionset, attr_names, no_of_attrs, dt_classifier.getNodeId());
	std::vector<attr_set*>* testsetvec = dt_classifier.readTestSet();
	dt_classifier.doDecisionTreeClassification(testsetvec);
}
