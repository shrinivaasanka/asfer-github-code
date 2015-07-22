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
using namespace std;

#include <list>


extern "C"
{
#include "string.h"
#include "stdlib.h"
}

struct comparefunctor{
	const char* str;

	comparefunctor(const char* s):str(s) 
	{}

	bool operator() (const comparefunctor& cf1, const comparefunctor& cf2) const
	{
		if(strcmp(cf1.str, cf2.str) < 0)
			return true;
		else
			return false;
	}
	
	bool operator<(const comparefunctor& comfunc) const
	{
		if(strcmp(str, comfunc.str) < 0)
			return true;
		else
			return false;
	}
};

struct tok_occur{
	int occur;
	const char* word;
};

class NaiveBayesClassifier
{
public:
	std::list<int>* getArticlesOfSingleClass(const char* cl); // function to get all articles of class c/.c - true for c and false for .c
	std::list<tok_occur*>* getTokensInArticle(int articleid); // get tokens in article , read words.txt

	int getOccurrences(const char* token, std::list<int>* articlesofsingleclass); // function to get total occurrences of ti in single class c (sum of all occurrences of ti in articles of c); loop through the list of articles in class c and for each article id invoke getOccurrencesInArticle()

	int getOccurrencesInArticle(const char* token, int articleid); //read from words.txt
	int getVocabularySize(); // size of words.txt
	int getTotalOccurrences(std::list<int>* articlesofsingleclass); // sum of occurrences of all ti in class c
	void doNBMultinomialClassification(std::list<int>& corpus);
	bool ifInTrainingSet(int articleid);
	std::list<int>* readTrainingSet(); 

};


