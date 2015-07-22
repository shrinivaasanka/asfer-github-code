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
#include <list>
#include <vector>
#include <tr1/unordered_map>
#include <string>

extern "C"
{
#include "string.h"
#include "stdlib.h"
}

using namespace std;
using namespace tr1;

typedef unordered_map<std::string, char*> attr_set;
class DecisionTreeClassifier
{
private:
	std::tr1::unordered_map<std::string, int> class_freq_map;
	std::tr1::unordered_map<std::string, std::vector<char*>*> attr_values_map;
	std::tr1::unordered_map<std::string, char*> dectree;
	string* dectreeroot;
public:
	int node_id;
	DecisionTreeClassifier() { node_id = 0; dectreeroot = 0; }
	int getNodeId();
	double impurityEval1(const std::vector<attr_set*>* decisionset);
	double impurityEval2(char* attr, const std::vector<attr_set*>* decisionset);
	char* belongToSameClass(const std::vector<attr_set*>*);
	char* findMajorityClass(const std::vector<attr_set*>*);
	int findImpurityReducingAttr(int attrsize, double *p, double cumul_p);
	std::vector<char*>* getPossibleAttrValues(char* attr);
	std::vector<attr_set*>* getDecisionSetPartitioned(std::vector<attr_set*>*, char*,char*);
	inline bool attrsetSatisfiesValue(attr_set* attribute_set, char* attr, char* value);
	void decisionTree(const std::vector<attr_set*>* decisionset, char attrs[][256], int attrs_size, int node_id);
	std::vector<attr_set*>* readTrainingSet();
	std::vector<attr_set*>* readTestSet();
	void doDecisionTreeClassification(std::vector<attr_set*>*);
};
