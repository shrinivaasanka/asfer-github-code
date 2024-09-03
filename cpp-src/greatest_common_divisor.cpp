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
#K.Srinivasan
#NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
#Personal website(research): https://acadpdrafts.readthedocs.io/en/latest/ 
#--------------------------------------------------------------------------------------------------------
*********************************************************************************************************/

using namespace std;
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

long long euclid_greatest_common_divisor(long long p,long long q);
long long euclid_greatest_common_divisor_multiple(long long *factors,int number_of_factors);

long long euclid_greatest_common_divisor_multiple(long long *factors,int number_of_factors)
{
	vector<int> gcds={};
	if (number_of_factors==1)
	{
		cout<<"number_of_factors:"<<number_of_factors<<endl;
		exit(1);
	}
	for(auto n=0; n < number_of_factors-1; n+=1)
	{
		cout<<"integer pair:"<<factors[n]<<" and "<<factors[n+1]<<endl;
		int pairwisegcd=euclid_greatest_common_divisor(factors[n],factors[n+1]);
		int count = std::count(gcds.begin(),gcds.end(),pairwisegcd);
		cout<<"pairwise GCD:"<<pairwisegcd<<endl;
		cout<<"count:"<<count<<endl;
		if(count==0)
			gcds.push_back(pairwisegcd);	
	}
	for(auto n: gcds)
		cout<<"gcd:"<<n<<endl;
	vector<int>::iterator minimum = std::min_element(gcds.begin(),gcds.end());
	cout<<"Multiple Greatest Common Divisor for list of factors:"<<*minimum<<endl;
	cout<<"List of factors:"<<endl;
	cout<<"[";
	for(int n=0;n < number_of_factors;n++)
		cout<<factors[n]<<" ";
	cout<<"]"<<endl;
	if (number_of_factors==1)
		exit;
	long long new_factors[gcds.size()];
	for(int n=0;n < gcds.size(); n++)
	{
		new_factors[n]=gcds[n];
		cout<<"new_factors:"<<new_factors[n]<<endl;
	}
	cout<<"----------------- Recursive call ----------------------------"<<endl;
	cout<<"gcds.size():"<<gcds.size()<<endl;
	euclid_greatest_common_divisor_multiple(new_factors,gcds.size());
}

long long euclid_greatest_common_divisor(long long p,long long q)
{
	cout<<"euclid_greatest_common_divisor():p="<<p<<";q="<<q<<endl;
	if(q==0)
		return p;
	return euclid_greatest_common_divisor(q, p%q);
}

int main(int argc, char* argv[])
{
	cout<<"--------------------------------------------"<<endl;
	cout<<"Multiple Integer Greatest Common Divisor"<<endl;
	cout<<"--------------------------------------------"<<endl;
	long long factors[]={99,18,63,27,36,45,72,54,90,117,108,81};
	euclid_greatest_common_divisor_multiple(factors,12);
	cout<<"--------------------------------------------"<<endl;
	cout<<"Euclid Greatest Common Divisor"<<endl;
	cout<<"--------------------------------------------"<<endl;
	long long p = stoll(argv[1]);
	cout<<"Factor p:"<<p<<endl;
	long long q = stoll(argv[2]);
	long long N = p*q;	
	cout<<"Factor q:"<<q<<endl;
	cout<<"Factors of integer N=pq found by Computational Geoemetric Factorization:"<<N<<endl;
	long long gcd = 2;
	while(gcd > 1)
	{
		gcd = euclid_greatest_common_divisor(p,q);
		cout<<"Greatest Common Divisor of "<<p<<" and "<<q<<" is (which is also a factor of "<<N<<"):"<<gcd<<endl;
		p=p/gcd;
		q=q/gcd;
	}
}
