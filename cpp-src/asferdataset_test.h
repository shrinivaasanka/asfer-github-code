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

#include <fstream>
#include <iostream>

extern "C"
{
#include "string.h"
#include "stdlib.h"
}

void test_asferdataset();

using namespace std;

void test_asferdataset()
{
	ifstream wordstxt;
	ofstream wordstxtbak;
	char line[256];
	wordstxt.open("words.txt", ifstream::in);
	wordstxtbak.open("words.txt.bak",ofstream::out);
	wordstxt.getline(line, 256);
	char* tail;
	while(wordstxt.good())
	{
		char* line2 = strdup(line);
		char* token = strtok(line, "~"); //word
		char* word = strdup(token); 
		token = strtok(NULL, "~");		//articleid and occurrences
		char* ar_id_str = strdup(token);
		int ar_id = strtol(ar_id_str, &tail, 0);
		token = strtok(NULL, "~");
		if(token)
			wordstxtbak << line2 << endl;
		wordstxt.getline(line, 256);
		free(word);
		free(ar_id_str);
		
	}

	wordstxt.close();
}	
