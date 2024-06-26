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

long long euclid_greatest_common_divisor(long long p,long long q)
{
	cout<<"euclid_greatest_common_divisor():p="<<p<<";q="<<q<<endl;
	if(q==0)
		return p;
	return euclid_greatest_common_divisor(q, p%q);
}

int main(int argc, char* argv[])
{
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
