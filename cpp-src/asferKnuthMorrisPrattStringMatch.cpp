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

/******************************************************
Knuth-Morris-Pratt String Match Algorithm:
(Pseudocode below - Reference: http://en.wikipedia.org/wiki/Knuth-Morris-Pratt_algorithm)
-----------------------------------------
table precomputation for T[]:
-----------------------------
   an integer, pos ← 2 (the current position we are computing in T)
   an integer, cnd ← 0 (the zero-based index in W of the next 
character of the current candidate substring)

    (the first few values are fixed but different from what the algorithm 
might suggest)
    let T[0] ← -1, T[1] ← 0

    while pos < length(W) do
        (first case: the substring continues)
        if W[pos-1] = W[cnd] then
            let cnd ← cnd + 1, T[pos] ← cnd, pos ← pos + 1

        (second case: it doesn't, but we can fall back)
        else if cnd > 0 then
            let cnd ← 0, T[pos] ← cnd, pos ← pos + 1

        (third case: we have run out of candidates.  Note cnd = 0)
        else
            let T[pos] ← 0, pos ← pos + 1
--------------------------------------------------
 m=0, i=0
 while m + i < length(S) do
        if W[i] = S[m + i] then
            if i = length(W) - 1 then
                return m
            let i ← i + 1
        else
            if T[i] > -1 then
                let m ← m + i - T[i], i ← T[i]
            else
                let i ← 0, m ← m + 1
            
******************************************************/

#include <string>
#include "asferKnuthMorrisPrattStringMatch.h"

using namespace std;

int asferKMPStringMatch::KMPMatch(string s,string w)
{
	int pos=2;
	int cnd=0;
	int m=0;
	int i=0;
	int t[s.length()];
	t[0]=-1;
	t[1]=0;

	while(pos < w.length())
	{
        	if (w[pos-1] == w[cnd])
		{
            		cnd = cnd + 1;
			t[pos] = cnd;
			pos = pos + 1;
		}
        	else if (cnd > 0)
		{
            		cnd = 0; 
			t[pos] = cnd; 
			pos = pos + 1;
		}		
        	else
		{
            		t[pos] = 0; 
			pos = pos + 1;
		}
	}

	while( m + i < s.length())
	{
		if(w[i] == s[m+i])
		{
			if(i == w.length()-1)
				return m;
			i++;
		}
		else
		{
			if(t[i] > -1)
			{
				m = m + i - t[i];
				i = t[i];
			}
			else
			{
				i=0;
				m++;
			}
		}
	}
	//substring not found
	return -1;
}
