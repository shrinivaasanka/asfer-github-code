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
#include "asferrule.h"
#include <fstream>
#include <iostream>

extern "C"
{
#include "math.h"
}

asferrule::asferrule(string r)
{
	rule_string = r;
}

std::list<string>* asferrule::tokenize()
{
/*
 char* house_copy = strdup(house); 
  char* token;
  token = strtok(house_copy, "/");
  while(house_copy != NULL)
  {
    if(strcmp(token, planet) == 0)
      return true;
    token = strtok(NULL, "/");
  }
  return false;

*/
	std::list<string> *tokens = new std::list<string>;
	int char_pos = 0;
	int readlength = 0;
	int prev_pos = 0;
	char_pos = rule_string.find_first_of(" ");
	while(readlength < rule_string.length())
	{
		std::string tok = rule_string.substr(prev_pos, char_pos-prev_pos);
		prev_pos = char_pos;
		tokens->push_back(tok);
		readlength += tok.length();
		//readlength++;
		char_pos = rule_string.find_first_of(" ", char_pos+1);
	}
	//while(char_pos  != std::string::npos);
	return tokens;
}

int asferrule::get_token_id(std::string token)
{
	token_id_uomap::iterator it = tokiduomap.find(token);
	if(it != tokiduomap.end())
		return it->second;
	else
	{
		tokiduomap.insert(token_id_uomap::value_type(token, asferrule::next_token_id));
		int ret = asferrule::next_token_id;
		asferrule::next_token_id++;
		return ret;
	}
}

void asferrule::make_VSR()
{
	cout << "make_VSR()" << endl;
	std::list<string> *tokens = tokenize();
	for(std::list<string>::iterator tok_it = tokens->begin(); tok_it != tokens->end(); tok_it++)
	{
		cout << *tok_it << endl;
		asferruleVSR::iterator vsr_it = asferruleVSR_map.find(*tok_it);
		if(vsr_it == asferruleVSR_map.end())
		{
			token_weight w;
			w.no_of_occurrences = 1;
			w.weight = 1.0;
			w.token_id = get_token_id(*tok_it);
			asferruleVSR_map[*tok_it] = w;
		}
		else
		{
			(vsr_it->second).no_of_occurrences++;
		}
	}
	
	float modulus = 0;
	for(asferruleVSR::iterator vsrit = asferruleVSR_map.begin(); vsrit != asferruleVSR_map.end(); vsrit++)
	{
		modulus += vsrit->second.no_of_occurrences * vsrit->second.no_of_occurrences;
	}
	modulus = sqrtf(modulus);	
	for(asferruleVSR::iterator vsrit = asferruleVSR_map.begin(); vsrit != asferruleVSR_map.end(); vsrit++)
	{
		vsrit->second.weight = vsrit->second.no_of_occurrences / modulus;
	}
	
}

void asferrule::write_VSR(char* test_filename) // needed for SVM retriever
{
	ofstream test_dat;
	char line[256];
	test_dat.open(test_filename); 
	test_dat<<"0 ";
	for(asferruleVSR::iterator it = asferruleVSR_map.begin(); it != asferruleVSR_map.end(); it++)
	{
		test_dat<< it->second.token_id << ":" << it->second.weight << " "; 
	}	
}

bool asferrule::operator==(const asferrule& asr)
{
	if(rule_string.compare(asr.rule_string) == 0)
		return true;
	else
		return false;
}

asferrule::~asferrule()
{
}
