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
#include <list>
#include <string>
#include <map>
#include <iostream>

#ifndef INDEXER_H
#include "indexer.h"
#endif

#define VSRETRIEVER_H

using namespace std;

typedef std::map<weighted_asferrule, float> result_type;

class VSRetriever
{
	private:
		asferindexer *index;
	public:
		result_type results;
		VSRetriever(asferindexer* ai);
		bool already_added_to_results(weighted_asferrule& wa);
		std::list<weighted_asferrule>* get_rules(std::string& query);
		float find_idf(std::string* tok);
		void print_results(result_type& results);
};

