/*****************************************************************************************
#-------------------------------------------------------------------------------------------------------
#ASFER - Software for Mining Large Datasets
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
#-----------------------------------------------------------------------------------------------------------
*****************************************************************************************/

/*
	IMPORTANT CAUTIONARY DISCLAIMER:
	-------------------------------
	This code is purely an academic research exercise. The author is NOT RESPONSIBLE for any unauthorized, unlawful execution and usage
	of this code with criminal intent.
*/

using namespace std;
#include <iostream>
#include <fstream>

extern "C"
{
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <sys/time.h>
}

long double factorial(long double);
long double power_of_x(long double, long double);
long double sum_of_logs(long double);
long double stirling_upperbound(long double);
int binary_search_int(int n,int xleft, int yleft, int xright, int yright);
int binary_search_int_arrayless(int n,int xleft, int yleft, int xright, int yright);
long double binary_search_dble(long double n,long double xleft,long  double yleft, long double xright, long double yright);

static long double factor=-1.0;

const int PADDING=0;


int mergedtiles[512];
int coordinates[512];
/*
int mergedtiles[256];
int coordinates[256];
*/
int next=0;

int main()
{
/*
Textual Function Plotter Code for Computation of Upperbound for Discrete Hyperbolic Factorization with Stirling Formula - using Rectangular Binary or Interpolation Search (10 September 2013) - http://sourceforge.net/projects/acadpdrafts/files/DiscreteHyperbolicFactorization_UpperboundDerivedWithStirlingFormula_2013-09-10.pdf/download

Complete LatexPDF draft version uploaded at: http://sourceforge.net/projects/acadpdrafts/files/DiscreteHyperbolicPolylogarithmicSieveForIntegerFactorization_updated_rectangular_interpolation_search_and_StirlingFormula_Upperbound.pdf/download
*/
	long double n = 0.0, i=0.0;
	long double prevlogsumoflogs=0.0;
	long double prevsum = 0.0, sum = 0.0, prevsumdiff = 0.0, sumdiff = 0.0, term1 = 0.0;
	//for(n = 2.0; n <= 5000000.0; n++)
	for(n = 511.0; n <= 511.0; n++)
	{
		struct timeval tv_start;
		gettimeofday(&tv_start,NULL);
		//term1 = power_of_x(n,sqrt(n)-1)/(factorial(sqrt(n)-1.0)*factorial(sqrt(n))) ;
		cout<<"=========================================================="<<endl;
		//cout<<"term1 = "<<term1<<"; log(n^(sqrt(n)-1)/sqrt(n)!(sqrt(n)-1)!)/loglogn = "<<log2l(term1)/log2l(log2l(n))<<endl;
		cout<<"Factorization begins at: "<<tv_start.tv_sec<<" secs and "<<tv_start.tv_usec<<" microsecs "<<endl;
		system("date");
		fflush(stdout);
		//cout<<"Factorization of n="<<n<<"; Stirling upperbound for sum of logs ---------- ="<<stirling_upperbound(n)<<endl;

		/*
		Sum of log/n*(n+1) and its Stirling Upperbound	log(n^(n-1)/n!*(n-1)!) and its intriguingly widening gap with log(n)
		- Ka.Shrinivaasan 8November2013
		Added a roundoff for negative values in sum_of_logs()
		- Ka.Shrinivaasan 12November2013
		*/
		double sumoflogs=sum_of_logs(n);
		cout<<"Factorization of n="<<n<<"; log(N) ="<<log2l(n)<<";(log(N))^3="<<log2l(n)*log2l(n)*log2l(n)<<"; Theoretically derived upperbound == sum of logs which is total binary search time on all discretized tiles (with roundoff for negative values) :"<<sumoflogs<<endl;
		cout<<"Factorization of n="<<n<<"; Stirling Upperbound (without roundoff for negative values) == "<<stirling_upperbound(n)<<endl;
		//cout<<"Factorization of n="<<n<<"; sum of logs as single log ----- log2l(n^(n-1)/n!*(n-1)!) ="<<log2l(term1)<<endl;
		//cout<<"Factorization of n, log2l(n)="<<log2l(n)<<endl;
		struct timeval tv_end;
		gettimeofday(&tv_end,NULL);
		cout<<"Factorization ends at: "<<tv_end.tv_sec<<" secs and "<<tv_end.tv_usec<<" microsecs "<<endl;
		cout<<"Factorization of n="<<n<<" takes time duration:"<<tv_end.tv_sec-tv_start.tv_sec<<" secs and "<<tv_end.tv_usec-tv_start.tv_usec<<" microsecs "<<endl;
		cout<<"Factorization of n="<<n<<", log(timeduration)/log(log(N)) [approximately could be the exponent of number of bits i.e polylog in input size divided by some constant ]:"<<log2l((double)(tv_end.tv_usec-tv_start.tv_usec))/log2l(log2l(n))<<endl;
		cout<<"Factorization of n="<<n<<", log(sumoflogs)/log(log(N)) [approximately could be the exponent of number of bits i.e polylog in input size divided by some constant ]:"<<log2l(sumoflogs)/log2l(log2l(n))<<endl;
		cout<<"Factorization of n="<<n<<"; sumoflogs diff convergence test: present term - prev term:"<<log2l(sumoflogs)/log2l(log2l(n))-prevlogsumoflogs<<endl;
		cout<<"Factorization of n="<<n<<"; sumoflogs/(log(n))^3 convergence test:"<<sumoflogs/(log2l(n)*log2l(n)*log2l(n))<<endl;
		cout<<"Factorization of n="<<n<<"; sumoflogs diff ratio with prev term convergence test: (present term - prev term)/prev term:"<<(log2l(sumoflogs)/log2l(log2l(n))-prevlogsumoflogs)/prevlogsumoflogs<<endl;
		cout<<"Factorization of n="<<n<<"; sumoflogs D'Alembert's convergence test: present term/prev term:"<<(log2l(sumoflogs)/log2l(log2l(n)))/prevlogsumoflogs<<endl;
		prevlogsumoflogs=log2l(sumoflogs)/log2l(log2l(n));
		system("date");
		fflush(stdout);
		cout<<"=========================================================="<<endl;
	}
	//binary_search_int(232,2,11,15,11);
	//cout<<"Binary search for factors of 35 as :["<<factor<<",5]<<"<<endl; 

	for(int mt=0; mt < 512; mt++)
	{
		cout<<"mergedtiles = "<<mergedtiles[mt]<<endl;
		cout<<"coordinates = "<<coordinates[mt]<<endl;
	}
}


long double factorial(long double n)
{
	long double fact_of_n=1.0;
	for(long double i=1.0; i<=n; i++)
	{
		fact_of_n=fact_of_n*i;
	}
	return fact_of_n;
}

long double sum_of_logs(long double n)
{
	long double sumoflogs=0.0;
	long double temp=0.0;
	long double xtile_start=n/2.0;
	long double xtile_end=n;
	long double xtile_sum=n/2.0;
	long double y=1.0;
	do
	{
		if(log2l(n/(y*(y+1.0))) < 0)
			temp = 0.0; // tile has length 1
		else
			temp = log2l(n/(y*(y+1.0)));
		//cout<<"########"<<endl;
		//cout<<"tesselation from 1 to N="<<n<<"  ------ discretized tile for log(deltai) at i="<<i<<" : "<<temp<<endl;
		//cout<<"binary_search_int("<<(int)n<<","<<(int)tile_sum<<","<<(int)i<<","<<(int)(tile_sum+(n/(i*(i+1.0))))<<","<<(int)i<<")"<<endl;
		//cout<<"tesselation from 1 to N="<<n<<"  ------ discretized tile for log(deltai) at i="<<y<<" ranges from "<<xtile_start<<" to "<<xtile_end<<endl;
		cout<<"binary_search_int("<<(int)n<<","<<(int)xtile_start<<","<<(int)y<<","<<(int)(xtile_end)<<","<<(int)y<<")"<<endl;
		factor=binary_search_int((int)n,(int)(xtile_start)-PADDING,(int)y,(int)(xtile_end)+PADDING,(int)y);
		//cout<<"binary_search_int_arrayless("<<(int)n<<","<<(int)xtile_start<<","<<(int)y<<","<<(int)(xtile_end)<<","<<(int)y<<")"<<endl;
		//factor=binary_search_int_arrayless((int)n,(int)(xtile_start)-PADDING,(int)y,(int)(xtile_end)+PADDING,(int)y);
		//cout<<"binary_search_dble("<<n<<","<<xtile_start<<","<<y<<","<<(xtile_end)<<","<<y<<")"<<endl;
		//factor=binary_search_dble(n,xtile_start,y,xtile_end,y);
		xtile_end=xtile_start;
		xtile_start=xtile_end-(n/((y+1.0)*(y+2.0)));
		//cout<<"########"<<endl;
		xtile_sum += (n/(y*(y+1.0)));
		sumoflogs += temp;
	}
	while(y++ < (n));

	return sumoflogs;
}

int binary_search_int_arrayless(int N, int xleft, int yleft, int xright, int yright)
{
	/*
	For DiscreteHyperbolicFactorization tile search always yleft==yright
	- Ka.Shrinivaasan 8November2013
	*/

	//cout<<"(int)((xleft+xright)/2):"<<(int)((xleft+xright)/2)<<"; array[(int)((xright-xleft)/2)]:"<<array[(int)((xright-xleft)/2)]<<endl;
	
	if ((xleft+(int)(xright-xleft/2))*yleft == N)
	{
		cout<<"binary_search_int_arrayless(): N="<<N<<" (a "<<log2l(N)<<" bit number); Factor is "<<xleft+(int)(xright-xleft)/2<<"; Factor*(yright or yleft)="<<(xleft+((int)((xright-xleft)/2)))<<"*"<<yright<<"="<<(xleft+((int)((xright-xleft)/2)))*yright<<endl;
		return xleft+(int)((xright-xleft)/2);
	}
	else 
	{
		if ((xleft+(int)(floor((xright-xleft)/2)))*yleft > N)
		{
			//binary_search_int_arrayless(N, xleft, yleft, xleft+(int)(floor((xright-xleft)/2)), yright);
			binary_search_int(N, xleft, yleft, xleft+(int)((xright-xleft)/2), yright);
		}
		else
		{
			//binary_search_int_arrayless(N, xleft+(int)(floor((xright-xleft)/2))+1, yleft, xright, yright);
			binary_search_int(N, xleft+(int)((xright-xleft)/2)+1, yleft, xright, yright);
		}
	}
}

int binary_search_int(int N, int xleft, int yleft, int xright, int yright)
{
	int array[(xright-xleft)+1];
	//cout<<"binary_search_int(): xleft = "<<xleft<<"; xright = "<<xright<<endl;
	//cout<<"binary_search_int(): tile searched is [";
	int i;
	for(i=0;i <= (xright-xleft); i++)
	{
		mergedtiles[next]=(xleft+i)*yleft;
		next++;
		array[i]=(xleft+i)*yleft;
		coordinates[next]=yleft;
		//cout<<array[i]<<",";
	}
	//cout<<"]"<<endl;
	//cout<<"sizeof tile:"<<sizeof(array)<<endl;
	if(i==0 || sizeof(array) == 4)
		return xright;
	i=0;
	//cout<<"(int)((xleft+xright)/2):"<<(int)((xleft+xright)/2)<<"; array[(int)((xright-xleft)/2)]:"<<array[(int)((xright-xleft)/2)]<<endl;
	if (array[(int)((xright-xleft)/2)] == N)
	{
		cout<<"binary_search_int(): N="<<N<<" (a "<<log2l(N)<<" bit number); Factor is "<<xleft+(int)((xright-xleft)/2)<<"; Factor*(yright or yleft)="<<(xleft+((int)((xright-xleft)/2)))<<"*"<<yright<<"="<<(xleft+((int)((xright-xleft)/2)))*yright<<endl;
		return xleft+(int)((xright-xleft)/2);
	}
	else 
	{
		if (array[(int)((xright-xleft)/2)] > N)
			binary_search_int(N, xleft, yleft, xleft+(int)((xright-xleft)/2), yright);
		else
			binary_search_int(N, xleft+(int)((xright-xleft)/2)+1, yleft, xright, yright);
	}
}


long double binary_search_dble(long double N, long double xleft, long double yleft, long double xright, long double yright)
{
	int array[(int)(xright-xleft)+1];
	//cout<<"binary_search_int(): xleft = "<<xleft<<"; xright = "<<xright<<endl;
	cout<<"binary_search_dble(): tile searched is [";
	for(int i=0;i <= ((int)xright-(int)xleft); i++)
	{
		cout<<"binary_search_dble(): i="<<i<<"; (xleft+i)="<<(xleft+i)<<"; yleft="<<yleft<<endl;
		array[i]=(int)(((int)xleft+i)*yleft);
		cout<<array[i]<<",";
	}
	cout<<"]"<<endl;
	cout<<"size of tile array:"<<sizeof(array)<<endl;
	if(sizeof(array)==4)
		return xleft;

	//cout<<"(int)((xleft+xright)/2):"<<(int)((xleft+xright)/2)<<"; array[(int)((xright-xleft)/2)]:"<<array[(int)((xright-xleft)/2)]<<endl;
	if (array[(((int)xright-(int)xleft)/2)] == N)
	{
		cout<<"binary_search_dble(): N="<<N<<"; Factor is "<<xleft+((int)xright-(int)xleft)/2<<endl;
		return xleft+((int)xright-(int)xleft)/2;
	}
	else 
	{
		if (array[(((int)xright-(int)xleft)/2)] > N)
			binary_search_dble(N, xleft, yleft, xleft+(((int)xright-(int)xleft)/2), yright);
		else
			binary_search_dble(N, xleft+(((int)xright-(int)xleft)/2), yleft, xright, yright);
	}
}

long double stirling_upperbound(long double n)
{
	long double term=0.0;
	long double e=2.71828;
	long double pi=3.14159265359;
	long double term1=0.0;
	long double term2=0.0;
	term1=power_of_x(e, 2*n);
	term2=2*pi*e*n*power_of_x(n-1,n);
	return log2l(term1/term2);
}

long double power_of_x(long double x, long double n)
{
	long double power = 1.0 ;
	for (long double i=n;i > 0.0;i--)
		power = power * x;
	return power;
}
