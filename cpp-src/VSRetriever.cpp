/*********************************************************************************************************
---------------------------------------------------------------------------------------------------------
ASFER - Inference Software for Large Datasets - component of iCloud Platform
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

---------------------------------------------------------------------------------------------------------
Copyright (C):
Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
Ph: 9789346927, 9003082186, 9791165980
Krishna iResearch Open Source Products Profiles:
http://sourceforge.net/users/ka_shrinivaasan, https://www.openhub.net/accounts/ka_shrinivaasan
Personal website(research): https://sites.google.com/site/kuja27/
ZODIAC DATASOFT: https://github.com/shrinivaasanka/ZodiacDatasoft
emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
---------------------------------------------------------------------------------------------------------
*********************************************************************************************************/

#include "VSRetriever.h"
#ifndef ASFERRULE_H
#include "asferrule.h"
#endif



extern "C"
{
#include "math.h"
}

VSRetriever::VSRetriever(asferindexer* ai)
{
	index = ai;
}

std::list<weighted_asferrule>* VSRetriever::get_rules(std::string& query)
{

	asferrule *asferquery = new asferrule(query);
	inv_index_type& inv_index = index->get_index();
	asferquery->make_VSR();
	//for each token in query 
	for(asferruleVSR::iterator it=asferquery->asferruleVSR_map.begin(); it != asferquery->asferruleVSR_map.end(); it++)
	{
		//Below line commented due to compiler error in gcc-g++ version 4.8.2 
		//which was compiling in older 4.4.x versions
		//instantiating a new string object
 
		//std::string *itfirst = &((std::string)it->first);
		std::string *itfirst = new std::string((std::string)it->first);
		float idf = find_idf(itfirst);
		it->second.weight = it->second.no_of_occurrences * idf;
		//lookup the query token in index
		for(inv_index_type::iterator index_it = inv_index.begin(); index_it != inv_index.end(); index_it++)
		{
			//if this index token is equal to query token
			std::string& token_str =  *(index_it->first.token);
			if(token_str[0] == ' ')
				token_str = (token_str.erase(0,1));
			if((*itfirst)[0] == ' ')
				itfirst = &(itfirst->erase(0,1));
			if(itfirst->compare(token_str) == 0)
			{
				cout << *itfirst << " == " << token_str << endl;
				//iterate through rules list for this token 
				for(std::list<weighted_asferrule>::iterator rule_it = index_it->second.begin(); rule_it != index_it->second.end(); rule_it++)
				{
					float score = rule_it->tf * index_it->first.idf * it->second.weight;
					//add the rule to results if not added already
					if(!already_added_to_results(*rule_it))
					{
						results[*rule_it] = 0.0; 
					}
					else
					{
						for(result_type::iterator it = results.begin(); it != results.end(); it++)
						{
							if(*(rule_it->asr) == *(it->first.asr)) //this should kick off operator== in asferrule
							{	
								it->second += score; // check this later
								break;
							}
						}
					}
				} 
			}
		} 
	} 

	//query length 
	float query_length;
	for(asferruleVSR::iterator it2=asferquery->asferruleVSR_map.begin(); it2 != asferquery->asferruleVSR_map.end(); it2++)
	{
		query_length += it2->second.weight * it2->second.weight;
	}
	query_length = sqrt(query_length);

	//normalization
	for(result_type::iterator result_it2 = results.begin(); result_it2 != results.end(); result_it2++)
	{
		result_it2->second = result_it2->second / (query_length * result_it2->first.asr->rule_length);
	}
	
	print_results(results);

	//todo - sorting 
	std::list<weighted_asferrule> *result_rules = new std::list<weighted_asferrule>;
	for(result_type::iterator result_it3 = results.begin(); result_it3 != results.end(); result_it3++)
		result_rules->push_back(result_it3->first);
	return result_rules;
}

void VSRetriever::print_results(result_type& results)
{
	cout << "Results:" << endl;
	for(result_type::iterator result_it = results.begin(); result_it != results.end(); result_it++)
	{
		cout <<"=================Rule ==" << result_it->first.asr->rule_string << endl;
	}
}

bool VSRetriever::already_added_to_results(weighted_asferrule& wa)
{
	for(result_type::iterator it = results.begin(); it != results.end(); it++)
	{
		if(*(wa.asr) == *(it->first.asr)) //this should kick off operator== in asferrule
			return true;
	}
	return false;
}

float VSRetriever::find_idf(std::string* tok)
{
	for(token_idf_map::iterator it = index->token_idf.begin(); it != index->token_idf.end(); it++)
	{
		if(tok->compare(it->first) == 0)
			return it->second;
	}
}
