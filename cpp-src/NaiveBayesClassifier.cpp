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
#include <set>
#include <fstream>
#include "NaiveBayesClassifier.h"

std::list<int>* NaiveBayesClassifier::getArticlesOfSingleClass(const char* cl)
{
	std::list<int>* articles = new std::list<int>; 
	ifstream topicstxt;
	char line[256];
	topicstxt.open("topics.txt", ifstream::in);
	topicstxt.getline(line, 256);
	while(topicstxt.good())
	{
		char* token = strtok(line, "~");
		char* tail;
		char* clas = strdup(token);
		if(strcmp(clas, cl) == 0)
		{
			token = strtok(NULL, "~");
			int article_id = strtol(token, &tail, 0);
			if(ifInTrainingSet(article_id)) // so that only those articles which are in training set are added
			{
				articles->push_back(article_id);
			}
		}
		topicstxt.getline(line, 256);
		free(clas);
	}
	topicstxt.close();
	return articles;

}

bool NaiveBayesClassifier::ifInTrainingSet(int article_id)
{
	ifstream trainingset;
	trainingset.open("training-set.txt", ifstream::in);
	char line[256];
	char *tail;
	trainingset.getline(line, 256);
	while(trainingset.good())
	{
		int ar_id = strtol(line, &tail, 0);
		if(ar_id == article_id)
			return true;
		trainingset.getline(line, 256);
	}
	trainingset.close();
	return false;
}

std::list<tok_occur*>* NaiveBayesClassifier::getTokensInArticle(int articleid)
{
	ifstream wordstxt;
	std::list<tok_occur*>* tokens = new std::list<tok_occur*>;
	char line[256];
	wordstxt.open("words.txt", ifstream::in);
	wordstxt.getline(line, 256);
	int i=0;
	char* tail;
	while(wordstxt.good())
	{
		char* token = strtok(line, "~"); //word
		tok_occur* tok_occ = new tok_occur();
		tok_occ->word = strdup(token); 
		token = strtok(NULL, "~");		//articleid and occurrences
		int ar_id = strtol(token, &tail, 0);
		token = strtok(NULL, "~");
		tok_occ->occur = strtol(token, &tail, 0);
		if(ar_id == articleid)
			tokens->push_back(tok_occ);
		wordstxt.getline(line, 256);
	}
	wordstxt.close();
	return tokens;
}

int NaiveBayesClassifier::getOccurrences(const char* token, std::list<int>* articlesofsingleclass)
{
	int occurrences = 0;
	for(std::list<int>::iterator ar_it = articlesofsingleclass->begin(); ar_it != articlesofsingleclass->end(); ar_it++)
	{
		occurrences += getOccurrencesInArticle(token, *ar_it);
	}
	return occurrences;
}

int NaiveBayesClassifier::getOccurrencesInArticle(const char* token, int articleid)
{
	ifstream wordstxt;
	ofstream wordstxtbak;
	wordstxt.open("words.txt", ifstream::in);
	wordstxtbak.open("words.txt.bak", ofstream::out);
	char line[256];
	wordstxt.getline(line, 256);
	char *tok, *word, *ar_id_str, *occur_str, *tail;
	int occurrences = 0;
	while(wordstxt.good())
	{
		tok = strtok(line, "~");
		word = strdup(tok);
		tok = strtok(NULL, "~");
		ar_id_str = strdup(tok);
		tok = strtok(NULL, "~");
		occur_str = strdup(tok);
		int ar_id = strtol(ar_id_str, &tail, 0);
		if(strcmp(word, token) == 0 && articleid == ar_id)
		{
			occurrences += strtol(occur_str, &tail, 0);
		}
		wordstxt.getline(line, 256);
		free(word);
		free(ar_id_str);
		free(occur_str);
	}
	wordstxt.close();
	return occurrences;	
		
}

int NaiveBayesClassifier::getVocabularySize()
{
	ifstream wordfreqtxt;
	wordfreqtxt.open("word-frequency.txt", ifstream::in);
	char line[256];
	wordfreqtxt.getline(line, 256);
	int size = 0;
	while(wordfreqtxt.good())
	{
		wordfreqtxt.getline(line, 256);
		size++;
	}
	wordfreqtxt.close();
	return size;
}

int NaiveBayesClassifier::getTotalOccurrences(std::list<int>* articlesofsingleclass)
{
	ifstream wordstxt;
	char line[256];
	int occurrences = 0;

	for(std::list<int>::iterator it = articlesofsingleclass->begin(); it != articlesofsingleclass->end(); it++)
	{
		wordstxt.open("words.txt", ifstream::in);
		wordstxt.getline(line, 256);
		char* tail;
		while(wordstxt.good())
		{
			char* token = strtok(line, "~"); //word
			char* word = strdup(token); 
			token = strtok(NULL, "~");		//articleid and occurrences
			char* ar_id_str = strdup(token);
			int ar_id = strtol(ar_id_str, &tail, 0);
			token = strtok(NULL, "~");
			char* occur_str = strdup(token);
			int occur = strtol(occur_str, &tail, 0); 
			if(ar_id == (*it) && ifInTrainingSet(ar_id)) // articles only in training set
				occurrences += occur;
			wordstxt.getline(line, 256);
			free(word);
			free(ar_id_str);
			free(occur_str);
		}
		wordstxt.close();
	}
	wordstxt.close();
	return occurrences;
}



void NaiveBayesClassifier::doNBMultinomialClassification(std::list<int>& corpus) //test set is corpus
{

	std::set<comparefunctor> topics; //classes
	ifstream topicstxt;
	topicstxt.open("topics.txt", ifstream::in);
	char line[256];
	topicstxt.getline(line, 256);
	char *token;
	double maxprobability = 0.0;
	double Pr_dgivenc = 0.0;
	double Pr_cgivend = 0.0;
	double Pr_tigivenc = 0.0;
	double Pr_c = 0.0;
	char* maxtopic = 0;
	double productofpr_tigivenc = 1.0;
	while(topicstxt.good())
	{
		token = strtok(line, "~");
		topics.insert(strdup(token));
		topicstxt.getline(line, 256);
	}

	std::list<int>* trset = readTrainingSet();
	for(std::list<int>::iterator it = corpus.begin(); it != corpus.end(); it++)
	{ 
		//find probability of article being present in all classes
		int cnt=0;
		for(std::set<comparefunctor>::iterator topic_it = topics.begin(); topic_it != topics.end(); topic_it++,cnt++)
		{
			if (cnt==0)
			{
				maxtopic = strdup(topic_it->str);
				cnt++;
			}
			std::list<int>* ar_c = getArticlesOfSingleClass(topic_it->str); //a priori probability
			Pr_c = (double) ar_c->size() / trset->size(); 
			std::list<tok_occur*>* ar_tokens = getTokensInArticle(*it);
			for(std::list<tok_occur*>::iterator token_it = ar_tokens->begin(); token_it != ar_tokens->end(); token_it++)
			{
				printf("token = %s \n", (*token_it)->word);
				double occurrences = getOccurrences((*token_it)->word, ar_c);
				double totaloccurrences = getTotalOccurrences(ar_c);
				double vocabularysize = getVocabularySize();
				double numerator = (double) (occurrences + 1.0); //laplace smoothing
				double denominator = (double) (totaloccurrences + vocabularysize);
				for(int i=0; i < (*token_it)->occur; i++)
					productofpr_tigivenc = (double) (productofpr_tigivenc * numerator) / denominator;
			}
			Pr_dgivenc = (double) Pr_c * productofpr_tigivenc;
			printf("topic = %s \n", topic_it->str);
			printf("maxprobability = %lf\n",maxprobability);
			printf("Pr_dgivenc = %lf\n",Pr_dgivenc);
			if(Pr_dgivenc > maxprobability)
			{
				maxprobability = Pr_dgivenc;
				maxtopic = strdup(topic_it->str);					
				printf("maxtopic = %s \n", maxtopic);
			}
			
			//delete lists
			for(std::list<tok_occur*>::iterator del_it = ar_tokens->begin(); del_it != ar_tokens->end(); del_it++)
			{
				delete ((*del_it)->word);
			}
			delete ar_tokens;
			delete ar_c;
			Pr_dgivenc = 0.0;
			Pr_cgivend = 0.0;
			Pr_tigivenc = 0.0;
			Pr_c = 0.0;
			productofpr_tigivenc = 1.0;
		} 
		printf("article id %d is NaiveBayesMultiNomial-Classified in topic %s \n", *it, maxtopic);
		maxtopic = 0;
		maxprobability = 0.0;
	}				
	topicstxt.close();
}


std::list<int>* NaiveBayesClassifier::readTrainingSet()
{
	ifstream trainingset;
	trainingset.open("training-set.txt", ifstream::in);
	char line[256];
	std::list<int>* corpus = new std::list<int>;
	char *tail;
	trainingset.getline(line, 256);
	while(trainingset.good())
	{
		int article_id = strtol(line, &tail, 0);
		corpus->push_back(article_id);
		trainingset.getline(line, 256);
	}
	trainingset.close();
	return corpus;		
}

