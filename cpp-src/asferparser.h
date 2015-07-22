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
#include <string>

#ifndef ASFERRULE_H
#include "asferrule.h"
#endif

#ifndef INDEXER_H
#include "indexer.h"
#endif

#define ASFERPARSER_H

using namespace std;

/*

Parsing asferrule:
------------------
Each rule is of the form:
	condition == result;

condition grammar (could be anyone of the following):
 <m>th lord is in <n>th house (condition type1)
 <m>th lord is <planet> (condition type2)
 <planet> is in <m>th house (condition type3)
 <planet> is in <sign> sign (condition type4)
 <planet> is in <longitude> degree (condition type5)
 <planet> is conjunct <planet> (condition type6)

result grammar:
 <string>

where
 m = 1,2,3,...,12
 n = 1,2,3,...,12
 planet= sun, moon, mars, mercury, jupiter, venus, saturn, rahu, ketu
 sign = mesha, rishabha, mithuna, kataka, simha, kanya, tula, vrischika, dhanus, makara, kumbha, meena
 longitude = 1 to 30

example input horoscope sparse matrix representation
------------------------------
first house - lagna - leo

houses|	1  2  3  4  5  6  7  8  9  10  11  12
------
1                                  Sun   

2                              Mer            

3                                      Ven

4                            Ket            Mars

5                                      Jup

6      Sat

7      Sat Rahu

8                                      Jup

9                                           Mars

10                                     Ven

11                             Mer

12         Moon

list representation of input horoscope
--------------------------------------
first house = leo
1    2          3 4 5 6 7  8      9    10 11               12
Sat Moon/Rahu              Ketu  Merc Sun Jupiter/Venus   Mars

algorithm 
----------
get the input
for all conditions
{
	check the input with the condition
	if input matches the condition add result to output
}

output the summed up result

*/

struct Horoscope
{
	char* lagna;
	char* houses[12];
};

/*
<m>th lord is in house <n>              (condition type1)
<m>th lord is <planet>                  (condition type2)
<planet> is in house <m>                (condition type3)
<planet> is in sign <sign>              (condition type4)
<planet> is in degree <longitude>       (condition type5)
<planet> is conjunct <planet>           (condition type6)

*/


struct type1_param
{
  int mth_lord;
  int nth_house;
};

struct type2_param
{
  const char* planet;
  int mth_lord;
};

struct type3_param
{
  const char* planet;
  int mth_house;
};

struct type4_param
{
  const char* planet;
  const char* sign; 
};

struct type5_param
{
  const char* planet;
  float longitude;
};

struct type6_param
{
  const char* planet1;
  const char* planet2;
};


class asferparser
{
	public:
		asferparser();
		std::string* parseAndPredict(std::list<weighted_asferrule>& results, Horoscope& horo);
		std::string get_condition(asferrule* asr);
		std::string get_effect(asferrule* asr);
		bool condition_matches_horoscope(std::string condition, Horoscope horo);
		int get_condition_type(std::string condition);
		std::string get_first_token(std::string condition);
		std::string get_second_token(std::string condition);
		int get_int(std::string str);
		float get_float(std::string str);
		char* get_sign(const char* planet, Horoscope horo);
		int get_sign_index(char* sign);
		char* get_mth_lord(int mth, Horoscope horo);
		bool contains(const char* house, const char* planet);

		//overloaded check_rule() for each condition type
		bool check_rule(type1_param p, Horoscope horo);
		bool check_rule(type2_param p, Horoscope horo);
		bool check_rule(type3_param p, Horoscope horo);
		bool check_rule(type4_param p, Horoscope horo);
		bool check_rule(type5_param p, Horoscope horo);
		bool check_rule(type6_param p, Horoscope horo);
		
};
