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
#include "DecisionTreeClassifier.h"
#include <fstream>
#include <iostream>

extern "C"
{
#include "math.h"
#include "stdlib.h"
#include "stdio.h"
}

std::vector<attr_set*>* DecisionTreeClassifier::readTrainingSet()
{
	ifstream trainingset;
	ifstream attrvaluestxt;
	std::vector<char*> attr_names;
	std::vector<char*> attr_values;
	std::vector<attr_set*>* retvalue = new std::vector<attr_set*>;
	trainingset.open("decisiontree-training.txt", ifstream::in);
	attrvaluestxt.open("decisiontree-attrvalues.txt", ifstream::in);
	char line[256];
	trainingset.getline(line, 256);
	char* token = strtok(line, " ");
	while(token != NULL)
	{
		attr_names.push_back(strdup(token));
		token = strtok(NULL, " ");
	}
	while(trainingset.good())
	{
		attr_values.clear();
		trainingset.getline(line, 256);
		token = strtok(line, " ");
		while(token != NULL)
		{
			attr_values.push_back(strdup(token));
			token = strtok(NULL, " ");
		}
		if(attr_values.size() > 0)
		{
			attr_set* attrset = new attr_set;
			//printf("training example--------\n");
			std::vector<char*>::iterator it1 = attr_names.begin();
			std::vector<char*>::iterator it2 = attr_values.begin();
			while(it1 != attr_names.end() && it2 != attr_values.end())
			{
				//printf("readTrainingSet: inserting keyvalue pair [%s, %s]\n", *it1, *it2);
				string str_attrname(strdup(*it1));
				attrset->insert(attr_set::value_type(str_attrname, strdup(*it2)));
				it1++;
				it2++;
			}
			if(it1 == attr_names.end() && it2 == attr_values.end())
				retvalue->push_back(attrset);
		}
	}
	//read attribute values
	char line2[256];
	attrvaluestxt.getline(line2, 256);
	while(attrvaluestxt.good())
	{
		token = strtok(line2, "-");
		//printf("attrtoken - %s\n", token);
		string attrname(strdup(token));
		std::vector<char*>* valuevect = new std::vector<char*>;
		token = strtok(NULL, "-");
		char* valuestoken = strdup(token);
		char* valuetoken = strtok(valuestoken, ",");
		while(valuetoken != NULL)
		{
			valuevect->push_back(valuetoken);
			//printf("valuetoken - %s\n", valuetoken);
			valuetoken = strtok(NULL, ",");
		}
		attr_values_map[attrname] = valuevect;
		attrvaluestxt.getline(line2, 256);
	}

	return retvalue;
}

std::vector<attr_set*>* DecisionTreeClassifier::readTestSet()
{
	ifstream testset;
	ifstream attrvaluestxt;
	std::vector<char*> attr_names;
	std::vector<char*> attr_values;
	std::vector<attr_set*>* retvalue = new std::vector<attr_set*>;
	testset.open("decisiontree-test.txt", ifstream::in);
	attrvaluestxt.open("decisiontree-attrvalues.txt", ifstream::in);
	char line[256];
	testset.getline(line, 256);
	char* token = strtok(line, " ");
	while(token != NULL)
	{
		attr_names.push_back(strdup(token));
		token = strtok(NULL, " ");
	}
	while(testset.good())
	{
		attr_values.clear();
		testset.getline(line, 256);
		token = strtok(line, " ");
		while(token != NULL)
		{
			attr_values.push_back(strdup(token));
			token = strtok(NULL, " ");
		}
		if(attr_values.size() > 0)
		{
			attr_set* attrset = new attr_set;
			//printf("test example--------\n");
			std::vector<char*>::iterator it1 = attr_names.begin();
			std::vector<char*>::iterator it2 = attr_values.begin();
			while(it1 != attr_names.end() && it2 != attr_values.end())
			{
				//printf("readTestSet: inserting keyvalue pair [%s, %s]\n", *it1, *it2);
				string str_attrname(strdup(*it1));
				attrset->insert(attr_set::value_type(str_attrname, strdup(*it2)));
				it1++;
				it2++;
			}
			if(it1 == attr_names.end() && it2 == attr_values.end())
				retvalue->push_back(attrset);
		}
	}
	//read attribute values
	char line2[256];
	attrvaluestxt.getline(line2, 256);
	while(attrvaluestxt.good())
	{
		token = strtok(line2, "-");
		//printf("attrtoken - %s\n", token);
		string attrname(strdup(token));
		std::vector<char*>* valuevect = new std::vector<char*>;
		token = strtok(NULL, "-");
		char* valuestoken = strdup(token);
		char* valuetoken = strtok(valuestoken, ",");
		while(valuetoken != NULL)
		{
			valuevect->push_back(valuetoken);
			//printf("valuetoken - %s\n", valuetoken);
			valuetoken = strtok(NULL, ",");
		}
		attr_values_map[attrname] = valuevect;
		attrvaluestxt.getline(line2, 256);
	}

	return retvalue;
}

void DecisionTreeClassifier::decisionTree(const std::vector<attr_set*>* decisionset, char attrs[][256], int attrs_size, int node_id)
{
	bool attrsetSatisfiesValue = false;
	int k=0;
	char* strnodeid = 0;
	char* childnode = 0;
	char* parent = 0;
	int dsetsize = decisionset->size();
	int dsetpart = 0;
	char* class_id = belongToSameClass(decisionset); // returns class id if in same class else returns -1
	int parent_node_id = node_id;	
	if(strcmp(class_id, "invalid-class") != 0)
	{
		printf("node {%d} is made leaf node of class --- {%s} \n", node_id, class_id);
		for(std::tr1::unordered_map<string, char*>::iterator it5 = dectree.begin(); it5 != dectree.end(); it5++)
		{
			strnodeid = new char[256];
			sprintf(strnodeid, "%d", node_id);
			if(strcmp(it5->second, strnodeid) == 0)
			{
				//cout << "it5->first = " << it5->first << endl;
				dectree[it5->first] = strdup(class_id);
				//cout << "after leaf node creation ; dectree[" << it5->first << "] = " << dectree[it5->first] << endl;
				break;
			}
		}
	}
	else if(attrs_size == 0)
	{
		class_id = findMajorityClass(decisionset);
		//printf("all attributes visited - node {%d} is assigned class {%s} \n", node_id, class_id);
		for(std::tr1::unordered_map<string, char*>::iterator it5 = dectree.begin(); it5 != dectree.end(); it5++)
		{
			strnodeid = new char[256];
			sprintf(strnodeid, "%d", node_id);
			if(strcmp(it5->second, strnodeid) == 0)
			{
				dectree[it5->first] = strdup(class_id);
				break;
			}
		}
	}
	else
	{
		double p[attrs_size];
		double threshold = 0.000001;
	 	double cumulative_p = impurityEval1(decisionset);
		for(int i=0; i < attrs_size; i++)
		{
			p[i] = -1.0; 
			if(strcmp(attrs[i], "Class") != 0)
				p[i] = impurityEval2(attrs[i], decisionset);
		}

		int purest_attr_index = findImpurityReducingAttr(attrs_size, p, cumulative_p);
		if(cumulative_p - p[purest_attr_index] < threshold)
		{
			class_id = findMajorityClass(decisionset);
			//printf("entropy reduction below threshold - node {%d} is assigned majority class {%s} \n", node_id, class_id);
		}
		else
		{
			printf("node id {%d} is assigned as decision node for maximum entropy reducing attribute {%s} \n", node_id, attrs[purest_attr_index]);
			std::vector<char*>* possible_attr_values = getPossibleAttrValues(attrs[purest_attr_index]);

			for(std::tr1::unordered_map<string, char*>::iterator it5 = dectree.begin(); it5 != dectree.end(); it5++)
			{
				strnodeid = new char[256];
				sprintf(strnodeid, "%d", node_id);
				if(strcmp(it5->second, strnodeid) == 0)
				{
					//cout << "it5->first = " << it5->first << endl;
					dectree[it5->first] = strdup(attrs[purest_attr_index]);
					//cout << "after resetting " << ";dectree[" << it5->first << "] = " << dectree[it5->first] << endl;
					break;
				}
			}
			
			//std::vector<attr_set*>* decisionset_partitioned = NULL;
			std::vector<attr_set*>* decisionset_partitioned = new std::vector<attr_set*>(dsetsize);
			decisionset_partitioned->clear();
			char new_attrs[attrs_size-1][256];
			
			for(int i=0; i < possible_attr_values->size(); i++)
			{
				//for(std::vector<attr_set*>::const_iterator it1 = decisionset->begin(); it1 != decisionset->end(); it1++)
				while(k < dsetsize)
				{
					for(attr_set::iterator it = ((*decisionset)[k])->begin(); it != ((*decisionset)[k])->end(); it++)
					{
						if(strcmp((it->first).c_str(), attrs[purest_attr_index]) == 0 && strcmp(it->second, possible_attr_values->at(i)) == 0)
							attrsetSatisfiesValue = true;
					}
					if(attrsetSatisfiesValue == true)
						(decisionset_partitioned)->push_back((*decisionset)[k]);
					attrsetSatisfiesValue = false;
					k++;
				}
				
				//decisionset_partitioned = getDecisionSetPartitioned(decisionset, attrs[purest_attr_index], possible_attr_values->at(i));

				cout << "-----------------------------------------------" << endl;
				cout << "Creating branch node id {" << ++node_id << "} as a child node of " << parent_node_id << " for attribute value {" << possible_attr_values->at(i) << "} of attribute {" << attrs[purest_attr_index] << "}" << endl;
				cout << "-----------------------------------------------" << endl;

				//add to decision tree
				
				string parent(strdup(attrs[purest_attr_index]));
				if(!dectreeroot)
				{
					dectreeroot = new string(parent);
				}
				parent.append("=");
				parent.append(strdup(possible_attr_values->at(i)));
				childnode = new char[256];
				sprintf(childnode, "%d", node_id);
				dectree[parent] = childnode;
				int l=0; 
				for(int k1=0; k1 < attrs_size; k1++)
				{
					if(strcmp(attrs[k1], attrs[purest_attr_index]) != 0)
						strcpy(new_attrs[l++],attrs[k1]);
				}
				decisionTree(decisionset_partitioned, new_attrs, attrs_size-1, node_id);
				decisionset_partitioned->clear();
				k=0; l=0;
			}
		}
	}
}

int DecisionTreeClassifier::findImpurityReducingAttr(int attr_size, double *p, double cumulative_p)
{
	int maximum_i = 0;
	double maximum = 0.0;

	for(int i=0; i < attr_size; i++)
	{
		if(p[i] != -1.0 && (cumulative_p - p[i] > maximum)) //excluding "Class"
		{
			maximum_i = i;
			maximum = cumulative_p - p[i];
		}
	}
	return maximum_i;
}

double DecisionTreeClassifier::impurityEval1(const std::vector<attr_set*>* dec_set)
{
	double entropy = 0.0;
	double max = 0.0;
	double total = 0.0;
	double prob = 0.0;
	class_freq_map.clear();
	for(std::vector<attr_set*>::const_iterator it1=dec_set->begin(); it1 != dec_set->end(); it1++)
	{
		string str_class("Class");
		attr_set::iterator attr_it = (*it1)->find(str_class);
		if(attr_it != (*it1)->end())
		{
			string str_attr(attr_it->second);
			int freq =class_freq_map[str_attr];
			class_freq_map[str_attr] = ++freq;
		}
	}
	

	for(std::tr1::unordered_map<string, int>::iterator it2=class_freq_map.begin();it2 != class_freq_map.end(); it2++)
	{
		total += it2->second;
	}
	for(std::tr1::unordered_map<string, int>::iterator it3=class_freq_map.begin(); it3 != class_freq_map.end(); it3++)
	{
		prob = (double) it3->second / total;
		entropy -= ( prob * log2(prob));
	}

	return entropy;	
}

double DecisionTreeClassifier::impurityEval2(char* attr, const std::vector<attr_set*>* dec_set)
{
	int count[attr_values_map.size()];
	//std::vector<attr_set*>* curr_value_set = new std::vector<attr_set*>[attr_values_map.size()];	

	int i=0;
	double entropyperattr = 0.0;
	string str_attr(attr);
	std::vector<char*>* values = attr_values_map[str_attr];
	std::vector<attr_set*>* curr_value_set = new std::vector<attr_set*>[values->size()];	
	//cout << "impurityEval2 --- values->size() = " << values->size() << endl;
	for(std::vector<char*>::iterator it1= values->begin(); it1 != values->end(); it1++, i++)
	{
		//cout << "impurityEval2 --- attribute --- attr = " << attr << " ;value = " << *it1 << endl;
		for(std::vector<attr_set*>::const_iterator it2 = dec_set->begin(); it2 != dec_set->end(); it2++)
		{
			attr_set* attset = *it2;
			attr_set::iterator attrit = attset->find(str_attr);
			if(attrit != attset->end())
			{
				if(strcmp(attrit->second, *it1) == 0)
				{
					count[i]++;
					//cout << "adding to curr_value_set[" << i << "]" << endl;
					curr_value_set[i].push_back(attset);
				}
			}
		}
	}

	for(i=0; i < values->size(); i++)
	{
		entropyperattr -= ((double) curr_value_set[i].size() / (double) (dec_set->size())) * -1 * impurityEval1(&curr_value_set[i]);
	}
	return entropyperattr; 
}

int DecisionTreeClassifier::getNodeId()
{
	return node_id++;
}

std::vector<char*>* DecisionTreeClassifier::getPossibleAttrValues(char* attr)
{
	string str_attr(attr);
	std::tr1::unordered_map<string, std::vector<char*>*>::iterator it = attr_values_map.find(str_attr);
	if(it != attr_values_map.end())
	{
		//printf("attr name --- %s\n", attr);
		for(int i = 0; i < (it->second)->size(); i++)
			//printf("-------%s\n", (it->second)->at(i));
		return (it->second);	 
	}
}

std::vector<attr_set*>* DecisionTreeClassifier::getDecisionSetPartitioned(std::vector<attr_set*>* dec_set, char* attr, char* attr_value)
{
	std::vector<attr_set*>* ret = new std::vector<attr_set*>;
	for(std::vector<attr_set*>::iterator it = dec_set->begin(); it != dec_set->end(); it++)
	{
		if(attrsetSatisfiesValue((*it), attr, attr_value))
			ret->push_back((*it));
		
	}
	return ret;
}

inline bool DecisionTreeClassifier::attrsetSatisfiesValue(attr_set* attribute_set, char* attr, char* value)
{
	//printf("attrsetSatisfiesValue: attr = %s ; value = %s \n", attr, value);
	for(attr_set::iterator it = attribute_set->begin(); it != attribute_set->end(); it++)
	{
		if(strcmp((it->first).c_str(), attr) == 0 && strcmp(it->second, value) == 0)
		{
			//printf("attrsetSatisfiesValue returns true\n");
			return true;
		}
	}
	//printf("attrsetSatisfiesValue returns false\n");
	return false;
}

char* DecisionTreeClassifier::belongToSameClass(const std::vector<attr_set*>* dec_set)
{
	int i=0;
	char *prev_class_value = new char[256];
	attr_set* attset;
	//cout << "belongToSameClass--decision set size = " << dec_set->size() << endl;
	for(std::vector<attr_set*>::const_iterator it=dec_set->begin(); it != dec_set->end(); it++)
	{
		attset = (*it);
		attr_set::iterator attr_it = attset->find("Class");
		//printf("belongToSameClass: %s ------- %s \n", attr_it->first, attr_it->second);
		if(attr_it != attset->end())
		{
			if(strcmp(prev_class_value, attr_it->second) != 0 && i > 0)
				return "invalid-class";
			else
				strcpy(prev_class_value, attr_it->second);
			i++;
		}				
	}
	return prev_class_value;
}

char* DecisionTreeClassifier::findMajorityClass(const std::vector<attr_set*>* dec_set)
{
	char* major_class = new char[256];
	int freq = 0;
	attr_set* attset;
	for(std::vector<attr_set*>::const_iterator it1=dec_set->begin(); it1 != dec_set->end(); it1++)
	{
		attset = (*it1);
		string str_class("Class");
		attr_set::iterator attr_it = attset->find(str_class);
		if(attr_it != attset->end())
		{
			string str_attr(attr_it->second);
			freq = class_freq_map[str_attr];
			class_freq_map[str_attr] = freq++;
		}
	}			
	for(std::tr1::unordered_map<string,int>::iterator it2=class_freq_map.begin();it2 != class_freq_map.end(); it2++)
	{
		int max = 0;
		if(it2->second > max)
		{
			strcpy(major_class, (it2->first).c_str());
			max = it2->second;
		}
	}
	return major_class;
}

void DecisionTreeClassifier::doDecisionTreeClassification(std::vector<attr_set*>* testset)
{
	string *parent = dectreeroot;
	string *attrvaluepair = 0;
	char* child = dectree[*dectreeroot];
	bool classified = false;
	int i=0;
	cout << "DECISION TREE CLASSIFIER RESULTS " << endl;
	cout << "---------------------------------" << endl;
	for(std::vector<attr_set*>::iterator it=testset->begin(); it != testset->end(); it++, i++)
	{
		attr_set* attset = *it;
		while(!classified)
		{
			for(attr_set::iterator it2 = attset->begin(); it2 != attset->end(); it2++)
			{
				if(strcmp((it2->first).c_str(), parent->c_str()) == 0)
				{
					attrvaluepair = new string(it2->first);
					attrvaluepair->append("=");
					attrvaluepair->append(it2->second);
				}
			}
			//parent = new string(dectree[*attrvaluepair]);				
			child = dectree[*attrvaluepair];
			std::vector<char*>* classvalues = attr_values_map["Class"];
			for(std::vector<char*>::iterator it3=classvalues->begin(); it3 != classvalues->end(); it3++)
			{
				if(strcmp(*it3, child) == 0)
				{
					printf("test example %d belongs to class = %s \n", i, child);	
					classified = true;
				}
			}
			if(!classified)
				parent = new string(child);
		}
		classified = false;
		parent = dectreeroot;
	} 
}
