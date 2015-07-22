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
#include <iostream>

using namespace std;

#define ASFERNEEDLEMANWUNSCH_SEQALIGN_H

/******************************************************************************************************
 * Implementation of Bioinformatics Dynamic Programming Sequence Alignment Algorithm(Needleman Wunsch)
 ****************************************************************************************************/


class asferneedlemanwunsch_seqalign
{
	//int similarity[12][12];
	int optimality[50][50];
	int penalty;
public:
	asferneedlemanwunsch_seqalign();
	int getIndex(char c);
	int getSimilarity(char x,char y);
	void computeOptimalityMatrix(string sq1, string sq2);
	void alignStringsNW(std::string sq1,std::string sq2);
	int findmaximum(int match, int delet, int insert);
};

using namespace std;
