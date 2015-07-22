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

/*
 * indices for planets:
 * -------------------
 * 0 - for unoccupied
 * 1 - Sun
 * 2 - Moon
 * 3 - Mars
 * 4 - Mercury
 * 5 - Jupiter
 * 6 - Venus
 * 7 - Saturn
 * 8 - Rahu
 * 9 - Ketu
 * 
 * Format of example asfer.horos file
 * --------------------------
 * Encoded horoscopes for similar events - each line in the file denotes an encoded chart for an event of particular class
 * --------------------------
 * 0#1#2#0#0#9#0#7#6#34#5#8
 * enc2 
 * enc3 
 * ... 
 */

using namespace std;

#include <tr1/unordered_map>
#include <string>
#include <list>
#include <vector>

class asferencodehoro
{
public:
	std::string decodeHoros(std::string encHoro); //reads an encoded horoscope and outputs decoded plaintext horoscope
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
