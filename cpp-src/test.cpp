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
#include <unordered_map>
#include <string>
#include <vector>
#include <cstdio>
#include <iostream>

using namespace std;

struct obj{
	int x;
};


void testfunc();

/*
int main()
{
	testfunc();
}
*/

void testfunc()
{
	string nullstring("");
	if(nullstring == "")
		cout<<"nullstring equals quoteunquote"<<endl;
	unordered_map<string, int> map;
	unordered_map<int, string> map2;
	string s1("int");
	string s2("float");
	map[s1] = 1 ;
	int x = map[s1];
	map[s1] = x++;
	printf("map[s1] = %d \n", map[s1]);

	map2[1]="x1";
	printf("map2[1] = %s \n", map2[1].c_str());

	std::vector<obj*>* intlist = new std::vector<obj*>;
	std::vector<obj*>* intlist2 = new std::vector<obj*>;
	int one = 1;
	int two = 2;
	obj objone;
	obj objtwo;
	objone.x = 1;
	objtwo.x = 62;
	intlist->push_back(&objone);
	intlist->push_back(&objtwo);
	for(int i=0; i < intlist->size(); i++)
	{
		printf("%d\n", *(intlist->at(i)));
		intlist2->push_back(intlist->at(i));
	}
	for(std::vector<obj*>::iterator it2 = intlist2->begin(); it2 != intlist2->end(); it2++)
	{
		printf("%d\n", (*it2)->x);
	}

}
