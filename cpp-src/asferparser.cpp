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
#ifndef ASFERPARSER_H
#include "asferparser.h"
#endif

extern "C"
{
#include "string.h"
#include "stdlib.h"
}

char* sign_lords[] = {"Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"};

char* signs[] = {"Mesha", "Rishabha", "Mithuna", "Kataka", "Simha", "Kanya", "Tula", "Vrishchika", "Dhanus", "Makara", "Kumbha", "Meena"};

asferparser::asferparser()
{
}

std::string* asferparser::parseAndPredict(std::list<weighted_asferrule>& results, Horoscope& horo)
{
    std::string *prediction =new std::string;
    for(std::list<weighted_asferrule>::iterator it = results.begin(); it != results.end(); it++)
    {
      std::string condition = get_condition(it->asr);
      std::string effect = get_effect(it->asr);
      
      if(condition_matches_horoscope(condition, horo))
	{
      *prediction += "\n";
	  *prediction += effect;
	}
    }

    return prediction;
}

std::string asferparser::get_condition(asferrule* asr)
{
  int splitter = asr->rule_string.find_first_of("==", 0);
  std::string cond = asr->rule_string.substr(0, splitter);
  return cond;
}

std::string asferparser::get_effect(asferrule* asr)
{
  int splitter = asr->rule_string.find_first_of("==", 0);
  std::string effect = asr->rule_string.substr(splitter+2, asr->rule_string.size());
  return effect;
}

bool asferparser::condition_matches_horoscope(std::string condition, Horoscope horo)
{
  int cond_type = get_condition_type(condition);
  bool rule_satisfied = false;
  string annotated_token1 = get_first_token(condition);
  string annotated_token2 = get_second_token(condition);
  switch(cond_type)
  {
  case 1:
    type1_param param1;
    param1.mth_lord = get_int(annotated_token1);
    param1.nth_house = get_int(annotated_token2);
    rule_satisfied = check_rule(param1, horo);
    break;
  case 2:
    type2_param param2;
    param2.planet = annotated_token2.data();
    param2.mth_lord = get_int(annotated_token1);
    rule_satisfied = check_rule(param2, horo);
    break;
  case 3:
    type3_param param3;
    param3.planet = annotated_token1.data();
    param3.mth_house = get_int(annotated_token2);
    rule_satisfied = check_rule(param3, horo);
    break;
  case 4:
    type4_param param4;
    param4.planet = annotated_token1.data();
    param4.sign = annotated_token2.data();
    rule_satisfied = check_rule(param4, horo);
    break;
  case 5:
    type5_param param5;
    param5.planet = annotated_token1.data();
    param5.longitude = get_float(annotated_token2);
    rule_satisfied = check_rule(param5, horo);
    break;
  case 6:
    type6_param param6;
    param6.planet1 = annotated_token1.data();
    param6.planet2 = annotated_token2.data();
    rule_satisfied = check_rule(param6, horo);
    break;
  }
  return rule_satisfied;

}


std::string asferparser::get_first_token(std::string cond)
{
  int start_angle_bracket = cond.find_first_of("<", 0);
  int end_angle_bracket = cond.find_first_of(">", 0);
  std::string first_token = cond.substr(start_angle_bracket+1, end_angle_bracket-start_angle_bracket-1);
  return first_token;
}

std::string asferparser::get_second_token(std::string cond)
{
  int start_angle_bracket = cond.find_last_of("<", cond.length()-1);
  int end_angle_bracket = cond.find_last_of(">", cond.length()-1);
  std::string second_token = cond.substr(start_angle_bracket+1, end_angle_bracket-start_angle_bracket-1);
  return second_token;
}

int asferparser::get_condition_type(std::string cond)
{
  int first_angle_close = cond.find_first_of(">", 0);
  int last_angle_open = cond.find_last_of("<", cond.length()-1);
  std::string relation = cond.substr(first_angle_close + 1, last_angle_open - first_angle_close - 1);
  if(relation.compare("th lord is in ") == 0)
    return 1;
  else if(relation.compare("th lord is ") == 0)
    return 2;
  else if(relation.compare(" is in house ") == 0)
    return 3;
  else if(relation.compare(" is in sign ") == 0)
    return 4;
  else if(relation.compare(" is in degree ") == 0)
    return 5;
  else if(relation.compare(" is conjunct ") == 0)
    return 6;
}

bool asferparser::contains(const char* house, const char* planet)
{
  char* house_copy = strdup(house); 
  char* token;
  token = strtok(house_copy, "/");
  while(token != NULL)
  {
    if(strcmp(token, planet) == 0)
      return true;
    token = strtok(NULL, "/");
  }
  return false;
  
}

bool asferparser::check_rule(type1_param p, Horoscope horo)
{
  char* mth_lord = get_mth_lord(p.mth_lord, horo);
  if(contains(horo.houses[p.nth_house-1], mth_lord))
    return true;
  else
    return false;
       
}

bool asferparser::check_rule(type2_param p, Horoscope horo)
{
  char* mth_lord = get_mth_lord(p.mth_lord, horo);
  if(strcmp(mth_lord, p.planet) == 0)
    return true;
  else
    return false;
}

bool asferparser::check_rule(type3_param p, Horoscope horo)
{
  if(contains(horo.houses[p.mth_house-1], p.planet))
    return true;
  else
    return false;
}

bool asferparser::check_rule(type4_param p, Horoscope horo)
{
  const char* in_sign = get_sign(p.planet, horo);
  if(strcmp(in_sign, p.sign)==0)
    return true;
  else
    return false;
}

bool asferparser::check_rule(type5_param p, Horoscope horo)
{
  return false;
}

bool asferparser::check_rule(type6_param p, Horoscope horo)
{
  for(int i=0 ;i < 12; i++)
  {
    if(contains(horo.houses[i], p.planet1) && contains(horo.houses[i], p.planet2))
       return true;
  }
  return false;
}

char* asferparser::get_mth_lord(int mth, Horoscope horo)
{
  int sign_index = get_sign_index(horo.lagna);
  return sign_lords[(sign_index + mth - 1)%12];
}

int asferparser::get_sign_index(char* sign)
{
  for(int i=0; i < 12; i++)
  {
    if(strcmp(sign, signs[i]) == 0)
       return i;
  }
}


char* asferparser::get_sign(const char* planet, Horoscope horo)
{
  for(int i=0; i < 12; i++)
  {
    if(contains(horo.houses[i], planet))
    {
      int lagna_index = get_sign_index(horo.lagna);
      return signs[(lagna_index + i) % 12];
    }
  }
}

int asferparser::get_int(std::string str)
{
  char *tail;
  int value = strtol(str.c_str(), &tail, 0);
  return value;
}

float asferparser::get_float(std::string str)
{
  char* tail;
  float value = strtof(str.c_str(), &tail);
  return value;
}



  
