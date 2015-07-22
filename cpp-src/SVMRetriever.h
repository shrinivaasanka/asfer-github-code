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

/*
SVMRetrieve algorithm:
---------------------
predetermine classes - profession, marriage, mundane etc.,

//manual
for each class
	create a training file training_<class>.dat with VSR representation for +1/-1 and send it through svm_learn to obtain model_<class>.dat
	svm_learn training_<class>.dat model_<class>.dat
endfor

//to implement
for each rule
	write the VSR representation of the rule from make_VSR() into file test.dat (corpus to classify)
endfor


for each class
	svm_classify test.dat model_<class>.dat output_<class>.dat
	This would give rules relevant to a class versus the rest
endfor

for each class
	svm_classify query.dat model_<class>.dat query_output_<class>.dat
	query.dat contains VSR for the query //to implement
	This would classify the query into one of the classes
endfor

output the rules whose class is same as the query class
*/

#include <string>
#include <list>

#ifndef INDEXER_H
#include "indexer.h"
#endif

#define SVMRETRIEVER_H



class SVMRetriever
{
	private:
		asferindexer* index; 
	public:
		SVMRetriever(asferindexer*);
		void create_class_models();
		void write_test_dat();
		std::list<weighted_asferrule>* get_rules(std::string query);
		std::list<asferrule>* find_relevant_rules_for_query_class(char* query_class);
		char* find_query_class();
		void classify_corpus();
		char* classify_query(std::string& query);
};



