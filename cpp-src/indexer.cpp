/***************************************************************************************
ASFER - a ruleminer which gets rules specific to a query and executes them
Copyright (C) 2009-2010  Ka.Shrinivaasan

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

mail to: ka.shrinivaasan@gmail.com
*****************************************************************************************/
#ifndef INDEXER_H
#include "indexer.h"
#endif

#include <iostream>
#include <fstream>

extern "C"
{
#include "math.h"
}

using namespace std;



asferindexer::asferindexer(std::string rfile)
{
	rules_file = rfile;
	inverted_index.clear();
}

inv_index_type& asferindexer::get_index()
{
	return inverted_index;
}

std::list<asferrule>& asferindexer::get_rule_corpus()
{
	return rule_corpus;
}

void asferindexer::read_rule_corpus()
{
	ifstream rfs;
	char line[256];
	rfs.open("/root/workspace/asfer-eclipse/cpp-src/asfer.rules", ifstream::in);
	if(rfs) {
		while(!rfs.eof())
		{
			rfs.getline(line, 256);
			string linestring(line);
			asferrule ar(linestring);
			rule_corpus.push_back(ar);
		}
	}
}

void asferindexer::create_index()
{
	for(std::list<asferrule>::iterator corpus_iter = rule_corpus.begin(); corpus_iter != rule_corpus.end(); corpus_iter++)
	{
		asferrule rule = *corpus_iter;
		rule.make_VSR(); //VSR - vector space representation in std::map
		asferruleVSR& rule_vector = rule.asferruleVSR_map;
		//std::list<string> rule_vector_tokens = get_tokens(rule_vector);

		for(asferruleVSR::iterator rule_vsr_iter = rule_vector.begin(); rule_vsr_iter != rule_vector.end(); rule_vsr_iter++)
		{
			weighted_term wt;
			wt.token = new std::string(rule_vsr_iter->first);
			wt.idf = 0.0;
			//inv_index_type::iterator index_iter = inverted_index.find(wt);
			inv_index_type::iterator index_iter;
			for(index_iter = inverted_index.begin(); index_iter != inverted_index.end(); index_iter++)
			{
				if((*index_iter).first.token->compare(*(wt.token)) == 0)
					break;
			} 
			
			if(index_iter == inverted_index.end())
			{
				std::list<weighted_asferrule> rulelist;
				weighted_asferrule wa;
				wa.asr = &(*corpus_iter);
				wa.tf = rule_vsr_iter->second.no_of_occurrences;
				rulelist.push_back(wa);
				//inverted_index.insert(term_rulelist_pair(wt, rulelist));
				inverted_index[wt] = rulelist;
			}
			else
			{
				weighted_asferrule wa;
				wa.asr = &(*corpus_iter);
				wa.tf = rule_vsr_iter->second.no_of_occurrences;
				index_iter->second.push_back(wa);
			} 
		}
	}
	
	//compute IDF
	int rule_corpus_size = rule_corpus.size();
	for(inv_index_type::iterator ind_it = inverted_index.begin(); ind_it != inverted_index.end(); ind_it++)
	{
		token_idf[*(ind_it->first.token)] = rule_corpus_size / (ind_it->second.size());

	}
	 
	//document length 
	compute_document_length();
}		

void asferindexer::print_index()
{
	for(inv_index_type::iterator token_it = inverted_index.begin(); token_it != inverted_index.end(); token_it++)
	{
		cout << "Term == " << *(token_it->first.token) <<endl;
		for(std::list<weighted_asferrule>::iterator rule_it = token_it->second.begin(); rule_it != token_it->second.end(); rule_it++)
		{
			cout << "==========Rule == " << rule_it->asr->rule_string <<endl;
		}
	}
}

void asferindexer::compute_document_length()
{
	for(inv_index_type::iterator index_it2 = inverted_index.begin(); index_it2 != inverted_index.end(); index_it2++)
	{
		int idf = index_it2->first.idf;
		for(std::list<weighted_asferrule>::iterator rule_it2 = index_it2->second.begin(); rule_it2 != index_it2->second.end(); rule_it2++)
		{
			rule_it2->asr->rule_length += idf * idf * rule_it2->tf * rule_it2->tf;
		}
	}
	for(std::list<asferrule>::iterator corpus_it = rule_corpus.begin(); corpus_it != rule_corpus.end(); corpus_it++)
	{
		corpus_it->rule_length = sqrtf(corpus_it->rule_length);
	}
}

std::list<string> asferindexer::get_tokens(asferruleVSR rule_vsr)
{
	std::list<string> tokens;
	for(asferruleVSR::iterator it = rule_vsr.begin(); it != rule_vsr.end(); it++)
	{
		tokens.push_back(it->first);
	}
	return tokens;
}

bool operator<(const weighted_term& wt1, const weighted_term& wt2)
{
		int i = wt1.token->compare(*(wt2.token));
		if(i >= 0)
		{
			return false;
		}
		else
			return true;
}

bool operator<(const weighted_asferrule& wa1, const weighted_asferrule& wa2)
{
	int i = wa1.asr->rule_string.compare(wa2.asr->rule_string);
	if(i >= 0)
		return false;	
	else
		return true;
}

asferindexer::~asferindexer()
{

}

