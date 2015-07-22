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

#ifndef ASFERNEEDLEMANWUNSCH_SEQALIGN_H
#include "asferneedlemanwunsch_seqalign.h"
#endif

int similarity[12][12]={{10,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1},
						{-1,10,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1},
						{-1,-1,10,-1,-1,-1,-1,-1,-1,-1,-1,-1},
						{-1,-1,-1,10,-1,-1,-1,-1,-1,-1,-1,-1},
						{-1,-1,-1,-1,10,-1,-1,-1,-1,-1,-1,-1},
						{-1,-1,-1,-1,-1,10,-1,-1,-1,-1,-1,-1},
						{-1,-1,-1,-1,-1,-1,10,-1,-1,-1,-1,-1},
						{-1,-1,-1,-1,-1,-1,-1,10,-1,-1,-1,-1},
						{-1,-1,-1,-1,-1,-1,-1,-1,10,-1,-1,-1},
						{-1,-1,-1,-1,-1,-1,-1,-1,-1,10,-1,-1},
						{-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,10,-1},
						{-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,10}};


asferneedlemanwunsch_seqalign::asferneedlemanwunsch_seqalign()
{
	penalty=3;
}

int asferneedlemanwunsch_seqalign::getIndex(char c)
{
	switch(c)
	{
	case '0':
		return 0;
	case '1':
		return 1;
	case '2':
		return 2;
	case '3':
		return 3;
	case '4':
		return 4;
	case '5':
		return 5;
	case '6':
		return 6;
	case '7':
		return 7;
	case '8':
		return 8;
	case '9':
		return 9;
	case 'a':
		return 10;
	case '#':
		return 11;
	}
}

int asferneedlemanwunsch_seqalign::getSimilarity(char x,char y)
{
	return similarity[getIndex(x)][getIndex(y)];
}

int asferneedlemanwunsch_seqalign::findmaximum(int match, int delet, int insert)
{
	int max;
	max= (match > delet) ? match : delet;
	max= (max > insert) ? max : insert;
	return max;
}

void asferneedlemanwunsch_seqalign::computeOptimalityMatrix(string s1,string s2)
{
	/************************************************************************
	 * Compute Optimiality
	for i=0 to length(A)
	  F(i,0) ← d*i
	for j=0 to length(B)
	  F(0,j) ← d*j
	for i=1 to length(A)
	  for j=1 to length(B)
	  {
	    Match ← F(i-1,j-1) + S(Ai, Bj)
	    Delete ← F(i-1, j) + d
	    Insert ← F(i, j-1) + d
	    F(i,j) ← max(Match, Insert, Delete)
	  }
	***********************************************************************/
	for(int i=0; i < 50; i++)
	{
		for(int j=0; j < 50; j++)
		{
			optimality[i][j] = 0;
		}
	}
	
	int match, delet, insert;
	for(int i=0; i < s1.length(); i++)
		optimality[i][0] = penalty * i;
	for(int j=0; j < s2.length(); j++)
		optimality[0][j] = penalty * j;
	for(int i=1; i < s1.length(); i++)
	{
		for(int j=1; j < s2.length(); j++)
		{
			match = optimality[i-1][j-1] + getSimilarity(s1[i], s2[j]);
			delet = optimality[i-1][j] + penalty;
			insert = optimality[i][j-1] + penalty;
			optimality[i][j]=findmaximum(match,delet,insert);
		}
	}
	
}

void asferneedlemanwunsch_seqalign::alignStringsNW(string s1, string s2)
{
	double similarity=0.0;
	/***********************************************************************
	 * Find Sequence Alignment from Optimality Matrix
	 * 
	AlignmentA ← ""
	AlignmentB ← ""
	i ← length(A)
	j ← length(B)
	while (i > 0 or j > 0)
	{
	  if (i > 0 and j > 0 and F(i,j) == F(i-1,j-1) + S(Ai, Bj))
	  {
	    AlignmentA ← Ai + AlignmentA
	    AlignmentB ← Bj + AlignmentB
	    i ← i - 1
	    j ← j - 1
	  }
	  else if (i > 0 and F(i,j) == F(i-1,j) + d)
	  {
	    AlignmentA ← Ai + AlignmentA
	    AlignmentB ← "-" + AlignmentB
	    i ← i - 1
	  }
	  else (j > 0 and F(i,j) == F(i,j-1) + d)
	  {
	    AlignmentA ← "-" + AlignmentA
	    AlignmentB ← Bj + AlignmentB
	    j ← j - 1
	  }
	}
	****************************************************************************************/
	string alignmentS1;
	string alignmentS2;
	int i = s1.length()-1;
	int j = s2.length()-1;
	while (i > 0 || j > 0)
	{
		if(i > 0 && j > 0 && (optimality[i][j] == optimality[i-1][j-1] + getSimilarity(s1[i],s2[j])))
		{
			alignmentS1 += s1[i];
			alignmentS2 += s2[j];
			i--;
			j--;
			similarity++;
		}
		else if (i > 0 && (optimality[i][j] == optimality[i-1][j] + penalty))
		{
			alignmentS1 += s1[i];
			alignmentS2 += "-";
			i--;
		}
		else if (j > 0 && (optimality[i][j] == optimality[i][j-1] + penalty))
		{
			alignmentS1 += "-";
			alignmentS2 += s2[j];
			j--;
		}
	}
	cout<<"======================================================================="<<endl;
	cout<<"NeedlemanWunsch Pairwise Alignment for:"<<s1<<" and "<<s2<<endl;
	cout<<"[Alignment1-MirrorReflected] :"<<alignmentS1<<endl;
	cout<<"[Alignment2-MirrorReflected] :"<<alignmentS2<<endl;
	cout<<"NeedlemanWunsch Percentage Similarity between ["<<s1<<"] and ["<<s2<<"] [aligned/S1_size]:"<<100.0*similarity/alignmentS1.length()<<endl;
	cout<<"NeedlemanWunsch Percentage Similarity between ["<<s1<<"] and ["<<s2<<"] [aligned/S2_size]:"<<100.0*similarity/alignmentS2.length()<<endl;
	cout<<"======================================================================="<<endl;
}
