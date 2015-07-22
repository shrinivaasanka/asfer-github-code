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

#include "asferstringdistance.h"

using namespace std;

/***************************************************************************************************
 * Implementation of String Distance Metrics 
****************************************************************************************************/

/* 
Wagner-Fischer Edit Distance Dynamic Programming Algorithm
*/
int asferstringdistance::editDistanceWagnerFischer(string s1, string s2)
{
	int dist[256][256];
	for(int i=0; i <= s1.length(); i++)
		dist[i][0]=i;
	for(int k=0; k <= s2.length(); k++)
		dist[0][k]=k;

	int i=1;
	int k=1;
	string::iterator it1=s1.begin();
	string::iterator it2=s2.begin();
	it1++;
	it2++;
	while(it1 != s1.end())
	{
		while(it2 != s2.end())
		{
			//cout<<"*it1="<<*it1<<"; *it2="<<*it2<<endl;
			if(*it1 == *it2)
			{
				dist[i][k] = dist[i-1][k-1];
				//cout<<"dist["<<i<<"]["<<k<<"] = "<<dist[i][k]<<endl;
			}
			else
			{
				//cout<<"find_min"<<endl;
				dist[i][k] = find_min(dist[i][k-1]+1,dist[i-1][k-1]+1,dist[i-1][k]+1);
				//cout<<"after find_min, dist["<<i<<"]["<<k<<"] = "<<dist[i][k]<<endl;
			}
			it2++;
			i++;
		}
		it1++;
		k++;
		i=1;
		it2=s2.begin();
	}
	cout<<"============================================================="<<endl;
	cout<<"Levenshtein Edit Distance between ["<<s1<<"] and ["<<s2<<"] :"<<dist[s2.length()-1][s1.length()-1]-2<<endl;
	cout<<"============================================================="<<endl;
	return dist[s2.length()-1][s1.length()-1]-2;
}

int asferstringdistance::find_min(int p, int q, int r)
{
	int min=-1;
	if(p < q)
		min = p;
	else
		min = q;
	
	if(r < min)	
		min = r;
	return min;
}
