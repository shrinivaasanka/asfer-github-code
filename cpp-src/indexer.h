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
#include <map>

#ifndef ASFERRULE_H
#include "asferrule.h"
#endif

#define INDEXER_H

using namespace std;
using namespace __gnu_cxx;

struct weighted_term
{
	std::string *token;
	float idf;
	friend bool operator<(const weighted_term& wt1, const weighted_term& wt2);
};


struct weighted_asferrule
{
	asferrule *asr;
	int tf;
	friend bool operator<(const weighted_asferrule& wa1, const weighted_asferrule& wa2);
};

typedef map< std::string, float> token_idf_map;

typedef pair< weighted_term, std::list<weighted_asferrule> > term_rulelist_pair;

typedef map< weighted_term, std::list<weighted_asferrule> > inv_index_type;

class asferindexer
{	
	private:
		 std::string rules_file;	
		 std::list<asferrule> rule_corpus;
		 inv_index_type inverted_index;

	public:
		inv_index_type& get_index();
		std::list<asferrule>& get_rule_corpus();
		token_idf_map token_idf;
		asferindexer(std::string);
		void create_index();
		void read_rule_corpus();
		std::list<string> get_tokens(asferruleVSR);
		void compute_document_length();
		void print_index();
		~asferindexer();
};



