/***************************************************************************************
# -------------------------------------------------------------------------------------------------------
# NEURONRAIN ASFER - Software for Mining Large Datasets
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------------------------------
# K.Srinivasan
# NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
# Personal website(research): https://acadpdrafts.readthedocs.io/en/latest/ 
# --------------------------------------------------------------------------------------------------------
#####################################################################################
 Old CPP test code written in 2006 for deriving error probability of majority voting
 and used 3 years ago in January 2010 during MSc thesis at IIT Chennai
 for deriving error probability of majority voting 
(Full report with results for Classification based on indegrees, TDT, Summarization, Citation graph Maxflow and 
Interview Algorithm based on Recursive Gloss Overlap Definition Graph: 
http://sourceforge.net/projects/acadpdrafts/files/MScThesis-Writeup-Complete.pdf/download)

For publications:
 1. http://arxiv.org/abs/1006.4458
 2. http://www.nist.gov/tac/publications/2010/participant.papers/CMI_IIT.proceedings.pdf
and other publication drafts related to majority voting and derandomization of BP* classes in 
https://acadpdrafts.readthedocs.io/en/latest/ (especially CJT derandomization gadget in section 1152)
#####################################################################################
*/

/*
Updated draft for Majority Voting Error Probability based on hypergeometric functions has been uploaded at:
1.https://sites.google.com/site/kuja27/CircuitForComputingErrorProbabilityOfMajorityVoting_2014.pdf?attredirects=0&d=1
(and)
2.https://sites.google.com/site/kuja27/CircuitForComputingErrorProbabilityOfMajorityVoting_2014.tex?attredirects=0&d=1

Special case of convergence of the series when p=0.5 
----------------------------------------------------
P(good) = (2n)!/(4^n) { 1/(n+1)!(n-1)! + 1/(n+2)!(n-2)! + ... + 1/(n+n)!(n-n)!}
has been derived and shown to be 0.5 in the handwritten notes uploaded at:
http://sourceforge.net/p/asfer/code/HEAD/tree/cpp-src/miscellaneous/MajorityVotingErrorProbabilityConvergence.JPG
But when the individual terms above differ in exponents of the probability terms (i.e there is no uniformity) ,the convergence has to be established only through hypergeometric functions.

Special case of convergence of the series when p=1:
---------------------------------------------------
1= 0 + 0 + 0 + ...+ (2n)C(cn) (1)^n (0)^(0) = 1
Thus with zero error both pseudorandom choice and majority vote yield P(good)= 100%.
*/

using namespace std;
#include <iostream>
#include <fstream>
#include <cmath>

extern "C"
{
#include <stdio.h>
}

long double factorial(long double);
long double power_of_4(long double);
long double condorcet_jury_theorem(long double n,long double p,long double c2,long double c3,long double c4);
bool iterative=false;

int main()
{
/*
P(good) = (2n)!/(4^n) { 1/(n+1)!(n-1)! + 1/(n+2)!(n-2)! + ... + 1/(n+n)!(n-n)!}
*/
	if(iterative)
	{
		long double n = 0.0, i=0.0;
		long double prevsum = 0.0, sum = 0.0, prevsumdiff = 0.0, sumdiff = 0.0, term1 = 0.0;
		for(n = 0.0; n <= 30000.0; n++)
		{
			term1 = factorial(2*n) / power_of_4(n);
			for (i=1.0; i <= n ; i++)
				sum = sum + (1.0 / (factorial(n+i) * factorial(n-i)));
			sum = term1 * sum;
			cout << "Probability of good choice for population of " << 2*n << "=" << sum*100.0 <<endl;
			sumdiff = sum - prevsum;
			cout << "prob - prevprob = " << sumdiff << endl;
			cout << "Convergence test: (sum - prevsum)/prevsum = " << sumdiff/prevsum << endl;
			prevsum = sum;
			prevsumdiff = sumdiff;
			sum =0.0;
		}
	}
	else
	{
		long double n;
		long double p;
		long double c2;
		long double c3;
		long double c4;
		cout<<"n:"<<endl;
		cin>>n;
		cout<<"p:"<<endl;
		cin>>p;	
		cout<<"c2 (0 to 1):"<<endl;
		cin>>c2;
		cout<<"c3 (0 to 1):"<<endl;
		cin>>c3;
		cout<<"c4 (0 to 1):"<<endl;
		cin>>c4;
		condorcet_jury_theorem(n,p,c2,c3,c4);
	}

}

long double condorcet_jury_theorem(long double n,long double p,long double c2,long double c3,long double c4)
{
	long double c1 = sqrt((2*n + 1)/3.14159265358979323846)*(1 + 1/(16*pow(n,2)) + c2/(pow(n,3))); 
	cout<<"c1 computed:"<<c1<<endl;
	long double cjt = 0.5 + c1*(p-0.5) + c3*pow(p-0.5,3) + c4*(p-0.5,5);
	cout << "Condorcet Jury Theorem asymptotic approximation for n="<<n<<" and p="<<p<<":"<<cjt<<endl;
	return cjt;
}

long double factorial(long double n)
{
	if (n==0.0)
		return 1.0;
	else
		return (long double) n*factorial(n-1);
}

long double power_of_4(long double n)
{
	long double power = 1.0 ;
	long double i;
	for (i=n;i > 0.0;i--)
		power = power * 4.0;
	return power;
}
