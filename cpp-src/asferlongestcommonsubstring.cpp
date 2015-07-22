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


/*
Recursive algorithm for longestCommonSubstring:
-----------------------------------------------
	LCSuffix(x,y) = LCSuffix(x-1,y-1) + 1 append to LCS if s1(x) == s2(y) 
	LCSuffix(x,y) = LCSuffix(x-1,y-1) + 0 else

	LCSubstring = argmax(all LCSuffixes)
*/



#include <string>
#include <iostream>
#include "asferlongestcommonsubstring.h"

using namespace std;
int lcs=0;
string lcs_str="";
string nullstring="";

string asferLCS::longestCommonSubstringRecursive(string str1, string str2)
{
	int str1len=str1.length();
	int str2len=str2.length();
	int max_lcslen=0;
	string maxlcsstr;
	
	for(int i=1; i <= str1len; i++)
	{
		for(int k=1; k <= str2len; k++)
		{
			cout<<"asferLCS::longestCommonSubstringRecursive():========================== "<<endl;
			lcs_str="";
			string ret=longestCommonSuffixRecursive(str1.substr(0,i), str2.substr(0,k));	
			cout<<"asferLCS::longestCommonSubstringRecursive(): LCSuffix =  "<<ret<<", length="<<ret.length()<<endl;
			if(ret.length() > max_lcslen)
			{
				cout<<"asferLCS::longestCommonSubstringRecursive(): ret.length =  "<<ret.length()<<", max_lcslen = "<<max_lcslen<<endl;
				max_lcslen=ret.length();
				maxlcsstr=ret;
			}
			cout<<"asferLCS::longestCommonSubstringRecursive():========================== "<<endl;
		}
	}
	cout<<"asferLCS::longestCommonSubstringRecursive(): argmax(all suffixes) = "<<maxlcsstr<<" of length = "<<max_lcslen<<endl;;
	return maxlcsstr;
}
 
string asferLCS::longestCommonSuffixRecursive(string string1, string string2)
{

	cout<<"asferLCS::longestCommonSuffixRecursive(): string1="<<string1<<"; string2="<<string2<<endl;

	if(string1.length() > 0 && string2.length() > 0)
	{
		if(string1.length() == 1 && string2.length() == 1 && string1 == string2)
		{
			lcs_str = string1;
			cout<<"asferLCS::longestCommonSuffixRecursive(): Longest Common Suffix so far :"<<lcs_str<<endl;
			return lcs_str;
		}	

		if(string1[string1.length()-1] == string2[string2.length()-1])
		{
			lcs+=1;
			lcs_str = longestCommonSuffixRecursive(string1.substr(0,string1.length()-1), string2.substr(0,string2.length()-1)) + string1[string1.length()-1];
			cout<<"asferLCS::longestCommonSuffixRecursive(): Longest Common Suffix so far :"<<lcs_str<<endl;
			return lcs_str;
		}
		else
		{
			return lcs_str;
		}
	}
	else
		return nullstring;
}
