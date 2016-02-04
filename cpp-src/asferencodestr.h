/***************************************************************************************
ASFER - a ruleminer which gets rules specific to a query and executes them
Copyright (C) 2009-2013  Ka.Shrinivaasan

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

mail to: ka.shrinivaasan@gmail.com (Krishna iResearch)
*****************************************************************************************/

using namespace std;

#include <tr1/unordered_map>
#include <string>
#include <list>
#include <vector>

class asferencodestr
{
public:
	void pairwiseCompAndExtractPatterns(); //reads from asfer.enchoros file and populates a string array and does pairwise comparison
	string extractPattern(std::string str1, std::string str2);
	std::list<std::string> tokenize(std::string str);
	std::string strcomp(std::string prev, std::string next);
	void allCompAndExtractPatterns();
	void powerSetCompAndExtractPatterns();
	std::vector<std::string> getNextSet(std::vector<std::string> enchoro_vec, int i);
	void powerSetExtractPatterns(std::vector<std::string> subsetvec);
	std::string printSet(std::vector<std::string> subset);
	void pairwiseNeedlemanWunshSequenceAlignment();
	void computeWagnerFischerEditDistance();
	void clusterEncodedHoro(string clusteringAlogrithm);
	void longestCommonSubstring();
};
