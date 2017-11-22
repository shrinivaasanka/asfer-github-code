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

int create_tiles(int n,int xleft, int yleft, int xright, int yright);
long double pixelated_hyperbolic_arc(long double n);

static long double factor=-1.0;

const int PADDING=0;

#ifndef NUMBER_OF_TILES
#define NUMBER_OF_TILES 1024 /* NUMBER_OF_TILES must be nearest power of 2 greater than the integer to factor */
#endif

int mergedtiles[NUMBER_OF_TILES]; /* NUMBER_OF_TILES must be nearest power of 2 greater than the integer to factor */
int coordinates[NUMBER_OF_TILES]; /* NUMBER_OF_TILES must be nearest power of 2 greater than the integer to factor */
int next=0;

int main(int argc, char *argv[])
{
	long double number_to_factorize = 0.0;
	long double n = 0.0, i=0.0;
	long double prevlogsumoflogs=0.0;
	long double prevsum = 0.0, sum = 0.0, prevsumdiff = 0.0, sumdiff = 0.0, term1 = 0.0;
	cout<<"NUMBER_OF_TILES:"<<NUMBER_OF_TILES<<endl;
	number_to_factorize=atoi(argv[1]);

	double sumoflogs=pixelated_hyperbolic_arc(number_to_factorize);

	for(int mt=0; mt < NUMBER_OF_TILES; mt++)
	{
		cout<<"mergedtiles = "<<mergedtiles[mt]<<endl;
		cout<<"coordinates = "<<coordinates[mt]<<endl;
	}
}


long double pixelated_hyperbolic_arc(long double n)
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
		cout<<"create_tiles("<<(int)n<<","<<(int)xtile_start<<","<<(int)y<<","<<(int)(xtile_end)<<","<<(int)y<<")"<<endl;
		factor=create_tiles((int)n,(int)(xtile_start)-PADDING,(int)y,(int)(xtile_end)+PADDING,(int)y);
		xtile_end=xtile_start;
		xtile_start=xtile_end-(n/((y+1.0)*(y+2.0)));
		xtile_sum += (n/(y*(y+1.0)));
		sumoflogs += temp;
	}
	while(y++ < (n));

	return sumoflogs;
}

int create_tiles(int N, int xleft, int yleft, int xright, int yright)
{
	int array[(xright-xleft)+1];
	int i;
	for(i=0;i <= (xright-xleft); i++)
	{
		mergedtiles[next]=(xleft+i)*yleft;
		next++;
		coordinates[next]=yleft;
	}
}
