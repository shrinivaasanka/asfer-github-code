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
#include <list>
#include <map>
#include <tr1/unordered_map>
#define ASFERRULE_H

using namespace std;
using namespace tr1;
using namespace __gnu_cxx;

//std::string hash fix
/*namespace __gnu_cxx {
  template<>
  struct hash<std::string>
  {
    hash<char*> h;
    size_t operator()(const std::string &s) const
    {
      return h(s.c_str());
    };
  };
}*/



struct tok_wei {
	int no_of_occurrences;
	float weight;
	int token_id;
};

typedef tok_wei token_weight;

typedef map<std::string, token_weight> asferruleVSR;

typedef std::tr1::unordered_map<std::string, int> token_id_uomap;

class asferrule
{
	private:
		token_id_uomap tokiduomap;
	public:
		static int next_token_id;
		int get_token_id(std::string token);
		std::string rule_string;
		float rule_length;
		asferruleVSR asferruleVSR_map;
		asferrule(string);
		bool operator==(const asferrule&);
		std::list<std::string>* tokenize();
		void make_VSR();
		void write_VSR(char* filename);
		~asferrule();
};
