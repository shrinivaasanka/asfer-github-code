/*********************************************************************************************************
#-------------------------------------------------------------------------------------------------------
#NEURONRAIN ASFER - Software for Mining Large Datasets
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------------
#Copyleft (Copyright+):
#Srinivasan Kannan
#(also known as: Shrinivaasan Kannan, Shrinivas Kannan)
#Ph: 9791499106, 9003082186
#Krishna iResearch Open Source Products Profiles:
#http://sourceforge.net/users/ka_shrinivaasan,
#https://github.com/shrinivaasanka,
#https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com,
#kashrinivaasan@live.com
#---------------------------------------------------------------------------------------------------------
*********************************************************************************************************/

#include "asferencodestr.h"
#include "asferneedlemanwunsch_seqalign.h"
#include "asferstringdistance.h"
#include "asferkmeansclustering.h"
#include "asferkNNclustering.h"
#include <iostream>
#include <fstream>
#include <vector>
#include <bitset>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include "asferlongestcommonsubstring.h"

extern const char* strplanets[];

extern std::string asferroot;

std::list<string> asferencodestr::tokenize(std::string str)
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
	std::list<string> tokens;
	int char_pos = 0;
	int readlength = 0;
	int prev_pos = 0;
	char_pos = str.find_first_of("#");
	while(readlength < str.length())
	{
		std::string tok = str.substr(prev_pos, char_pos-prev_pos);
		prev_pos = char_pos;
		tokens.push_back(tok);
		readlength += tok.length();
		//readlength++;
		char_pos = str.find_first_of("#", char_pos+1);
	}
	//while(char_pos  != std::string::npos);
	return tokens;
}

void asferencodestr::powerSetCompAndExtractPatterns()
{
	std::vector<string> enchoro_vec;
	ifstream input;
	char line[256];
	string encstrpath(asferroot);
	encstrpath.append("/asfer.enterprise.encstr");
	input.open(encstrpath.c_str(), ifstream::in);
	while (!input.eof())
	{
		input.getline(line,256);
		cout<<"powerSetCompAndExtractPatterns(): line="<<line<<endl;
		string enchorostr(line);
		if(strlen(line) > 0)
			enchoro_vec.push_back(enchorostr);
	}
	int n=enchoro_vec.size();
	cout<<"powerSetCompAndExtractPatterns(): enchoro_vec.size()="<<enchoro_vec.size()<<endl;
	for(int i=1; i < (int)pow(2.0, (double)n); i++)
	{
		cout<<"powerSet "<<i<<endl;
		std::vector<std::string> nextSubSet=getNextSet(enchoro_vec, i);
		powerSetExtractPatterns(nextSubSet);
	}
}

std::vector<std::string> asferencodestr::getNextSet(std::vector<std::string> enchoro_vec, int i)
{
	std::vector<std::string> subset;
	int n=enchoro_vec.size();
	//compute next subset in the power set
	std::bitset<100> setbitmap(i);
	int indx=0;
	for(size_t t = 0; t < setbitmap.size(); t++)
	{
		if(setbitmap.test(t))
		{
			subset.push_back(enchoro_vec[indx]);
		}
		indx++;
	}
	cout<<"getNextSet(): enchoro_vec.size() = "<<enchoro_vec.size()<<endl;
	cout<<"getNextSet(): subset: "<<printSet(subset)<<endl;
	cout<<"getNextSet(): subset size ="<<subset.size()<<endl;
	return subset;
}

std::string asferencodestr::printSet(std::vector<std::string> subset)
{
	string subsetToStr;
	subsetToStr.append("{");
	for(std::vector<std::string>::iterator it=subset.begin(); it != subset.end(); it++)
	{
		subsetToStr.append(*it);
		subsetToStr.append(",");
	}
	subsetToStr.append("}");
	return subsetToStr;
}

void asferencodestr::powerSetExtractPatterns(std::vector<std::string> subsetvec)
{
	cout<<"================================================="<<endl;
	cout<<"powerSetExtractPatterns(): subset size = "<<subsetvec.size()<<endl;
	string prev = subsetvec[0];
	for(int next=1;next < subsetvec.size();next++)
	{
		//prev = strcomp(prev,subsetvec[next]);
		prev = extractPattern(prev,subsetvec[next]);
	}
	cout<<"powerSetExtractPatterns(): subset pattern ="<<prev<<endl;
	cout<<"================================================="<<endl;
}

void asferencodestr::allCompAndExtractPatterns()
{
	std::vector<string> enchoro_vec;
	ifstream input;
	char line[256];
	string encstrpath(asferroot);
	encstrpath.append("/asfer.enterprise.encstr");
	input.open(encstrpath.c_str(), ifstream::in);
	while (!input.eof())
	{
		input.getline(line,256);
		string enchorostr(line);
		enchoro_vec.push_back(enchorostr);
	}
	
	string prev = enchoro_vec[0];
	for(int next=1;next < enchoro_vec.size();next++)
	{
		//prev = strcomp(prev,enchoro_vec[next]);
		prev = extractPattern(prev,enchoro_vec[next]);
	}
	cout<<"allCompAndExtractPatterns(): prev ="<<prev<<endl;
	cout<<"================================================="<<endl;
}

std::string asferencodestr::strcomp(std::string prev, std::string next)
{
	string comStr;
	comStr.clear();
	int it1=0;
	int it2=0;
	while(it1 < prev.size() && it2 < next.size())
	{
		if(prev[it1]==next[it2])
		{
			comStr+=prev[it1];
		}
		it1++;
		it2++;
	}
	//cout<<"strcomp(): comStr ="<<comStr<<endl;
	return comStr;
}

void asferencodestr::pairwiseCompAndExtractPatterns()
{
		int MAXENCSTRLEN=28;
		std::vector<string> encstr_vec;
		ifstream input;
		char line[500];
		string encstrpath(asferroot);
		encstrpath.append("/asfer.enterprise.encstr");
		input.open(encstrpath.c_str(), ifstream::in);
		while (!input.eof())
		{
			input.getline(line,256);
			cout<<"line = "<<line<<endl;
			if(strcmp(line,"") != 0)
			{
				string encstr(line);
				encstr_vec.push_back(encstr);
			}
			else
				break;
		}

		for(int i=0;i < encstr_vec.size();i++)
		{
			for(int k=0; k < encstr_vec.size();k++)
			{
				cout<<"=================================================="<<endl;
				cout<<"pair ("<<encstr_vec[i]<<","<<encstr_vec[k]<<")"<<endl;
				string extPat = extractPattern(encstr_vec[i], encstr_vec[k]);
				cout<<"pair ("<<i<<","<<k<<") has the common pattern:"<<extPat<<endl;
				cout<<"=================================================="<<endl;

			}
		}

		cout<<"============================================================================================================================="<<endl;
		cout<<"For each of the pairs of encoded strings, distance between them is computed (by an algorithm described in Grafit Course Notes - course_material/ComputerScienceMiscellaneous/ComputerScienceMiscellaneous_CourseNotes.txt) and sum of these distances is printed"<<endl;
		cout<<"============================================================================================================================="<<endl;
		int number_of_ones=0;	
		long double sum_distance=0.0;
		long double sum_distance_bit=0.0;
		for(int i=0;i < MAXENCSTRLEN;i++)
		{
			//cout<<"bit index = "<<i<<endl;
			for(std::vector<string>::iterator it=encstr_vec.begin(); it != encstr_vec.end(); it++)
			{
				//cout<<"(*it)[i] = "<<(*it)[i]<<endl;
				if((*it)[i] == '1')
				{
					number_of_ones += 1;
				}
				sum_distance_bit = combination(MAXENCSTRLEN,2) - (combination(number_of_ones,2) + combination(MAXENCSTRLEN-number_of_ones,2)); 
				sum_distance += sum_distance_bit;
				//cout<<"sum_distance for bit index = "<<sum_distance<<endl;
				number_of_ones=0;
			}
		}
		cout<<"Sum of pairwise distance = "<<sum_distance<<endl;
		cout<<"========================================================="<<endl;
}

long double asferencodestr::combination(int N, int k)
{
	long double NCk = factorial((long double)N)/(factorial((long double)k)*factorial((long double)(N-k))); 
	//cout<<"combination(): NCk = "<<NCk<<endl;
	return NCk;
}

long double asferencodestr::factorial(long double n)
{
	long double m=1.0;
	long double fctl=1.0;
	while(m <= n)
	{
		fctl = fctl*m;
		m=m+1;
	}
	//cout<<"factorial(): fctl = "<<fctl<<endl;
	return fctl;
}

string asferencodestr::extractPattern(string str1, string str2)
{
	/*
	 * Presently a naive matching is implemented. Applying LCS, KMP and other algorithms can be optionally
	 * done if an indepth pattern mining is needed.
	 */
	int i=0,k=0;
	string comPattern;
	comPattern.clear();
	std::list<std::string> toklist1 = tokenize(str1);
	std::list<std::string> toklist2 = tokenize(str2);
	std::list<std::string>::iterator it1 = toklist1.begin();
	std::list<std::string>::iterator it2 = toklist2.begin();
	while( it1 != toklist1.end() && it2 != toklist2.end())
	{
		unsigned posit;
		string signComPatt;
		if(it1->size() > it2->size())
		{
			posit = it1->find(*it2);
			if(posit >= 0 && posit != std::string::npos)
				signComPatt = it1->substr(posit);
		}	
		else
		{
			posit = it2->find(*it1);
			if(posit >= 0 && posit != std::string::npos)
				signComPatt = it2->substr(posit);
		}
		
		if(posit >= 0 && posit != std::string::npos)
		{
			cout<<"appending to comPattern:"<<signComPatt<<endl;
			comPattern.append(signComPatt);
		}
		else
			comPattern.append("#0");
		it1++; 
		it2++;
	}
	return comPattern;
}

void asferencodestr::pairwiseNeedlemanWunshSequenceAlignment()
{
		asferneedlemanwunsch_seqalign nwseqalign;
		std::vector<string> enchoro_vec;
		ifstream input;
		char line[256];
		string encstrpath(asferroot);
		encstrpath.append("/asfer.enterprise.encstr");
		input.open(encstrpath.c_str(), ifstream::in);
		while (!input.eof())
		{
			input.getline(line,256);
			string enchorostr(line);
			enchoro_vec.push_back(enchorostr);
		}
		
		for(int i=0;i < enchoro_vec.size();i++)
		{
			for(int k=0; k < enchoro_vec.size();k++)
			{
				cout<<"=================================================="<<endl;
				cout<<"pair ("<<enchoro_vec[i]<<","<<enchoro_vec[k]<<")"<<endl;
				if(enchoro_vec[i].length() != 0 && enchoro_vec[k].length() != 0)
				{
					nwseqalign.computeOptimalityMatrix(enchoro_vec[i], enchoro_vec[k]);
					nwseqalign.alignStringsNW(enchoro_vec[i], enchoro_vec[k]);
				}
				cout<<"=================================================="<<endl;

			}
		}
}

void asferencodestr::computeWagnerFischerEditDistance()
{
	    int editdistance=0;
	    asferstringdistance asferdist;
            std::vector<string> enchoro_vec;
            ifstream input;
            char line[256];
            string encstrpath(asferroot);
            encstrpath.append("/asfer.enterprise.encstr");
            input.open(encstrpath.c_str(), ifstream::in);
            while (!input.eof())
            {
                   input.getline(line,256);
                   string enchorostr(line);
                   enchoro_vec.push_back(enchorostr);
            }

            for(int i=0;i < enchoro_vec.size();i++)
            {
                     for(int k=0; k < enchoro_vec.size();k++)
                     {
                                cout<<"=================================================="<<endl;
                                cout<<"pair ("<<enchoro_vec[i]<<","<<enchoro_vec[k]<<")"<<endl;
                                if(enchoro_vec[i].length() != 0 && enchoro_vec[k].length() != 0)
                                {
                                        editdistance = asferdist.editDistanceWagnerFischer(enchoro_vec[i], enchoro_vec[k]);
                                }
				cout<<"Edit Distance (Wagner-Fischer) :"<<editdistance<<endl;
                                cout<<"=================================================="<<endl;

                     }
            }

}

void asferencodestr::clusterEncodedHoro(string clusteringAlgorithm)
{
	if(clusteringAlgorithm == "KMeans")
	{
		asferkmeansclustering akmeans;
		string distancemetric("editdistance");
		akmeans.KMeansClustering(distancemetric);
	}
	else if(clusteringAlgorithm == "kNN")
	{
		asferknnclustering aknn;
		string distancemetric("editdistance");
		aknn.kNNClustering(distancemetric);
	}
}

void asferencodestr::longestCommonSubstring()
{
	std::vector<string> enchoro_vec;
	ifstream input;
	char line[256];
	string encstrpath(asferroot);
	encstrpath.append("/asfer.enterprise.encstr.clustered");
	input.open(encstrpath.c_str(), ifstream::in);
	while (!input.eof())
	{
		input.getline(line,256);
		string enchorostr(line);
		enchoro_vec.push_back(enchorostr);	
	}
	
	asferLCS asferlcs;
	for(int i=0; i < enchoro_vec.size(); i++)
	{
		for(int k=0; k < enchoro_vec.size(); k++)
		{
			string s1=enchoro_vec[i];
			string s2=enchoro_vec[k];
			cout<<"#############################################################"<<endl;	
			cout<<"asferencodestr::longestCommonSubstring()"<<endl;
			cout<<"==========================================="<<endl;
			string lcs = asferlcs.longestCommonSubstringRecursive(s1,s2);	
			cout<<"asferencodestr::longestCommonSubstring(): Longest Common Substring for "<<s1<<" and "<<s2<<":"<<lcs<<endl;
			cout<<"#############################################################"<<endl;	
		}
	}
	
}
