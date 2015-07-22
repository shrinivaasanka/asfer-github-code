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
KMeans clustering for AsFer encoded horo strings with a distance metric
*/


#include "asferkmeansclustering.h"
#include "asferstringdistance.h"
#include <unordered_map>
#include <vector>

using namespace std;

extern std::string asferroot;

unordered_map<int, vector<string>> clusters;

int k=10; //number of clusters

void asferkmeansclustering::KMeansClustering(string distanceMetric)
{
	bool converged=false;

	asferstringdistance asd;
	string centroids[k]; // centroids recomputed for each cluster

   	std::vector<string> enchoro_vec;
        ifstream input;
        char line[256];
        string enchorospath(asferroot);
        enchorospath.append("/asfer.enchoros");
        input.open(enchorospath.c_str(), ifstream::in);
        
	while (!input.eof())
        {
               input.getline(line,256);
               string enchorostr(line);
               enchoro_vec.push_back(enchorostr);
        }

	//label initially with some cluster id
	int cluster_id=0;
	clusters.clear();
        for(int i=0;i < enchoro_vec.size();i++)
        {
		string nullstring("");
		if(enchoro_vec[i] != nullstring)
			clusters[cluster_id].push_back(enchoro_vec[i]);
		cluster_id = (cluster_id+1) % k;
        }

	//pseudorandomly label centroids for each cluster instead of usual [vector sum/number of vectors]
	for(int i=0; i < k; i++)
	{
		cout<<"clusters["<<i<<"].at(0)"<<clusters[i].at(0)<<endl;
		centroids[i]=clusters[i].at(0);
		cout<<"centroids["<<i<<"]="<<centroids[i]<<endl;
	}

	int iteration=0;
	while(iteration < 10 || !converged)
	{
		printClusters(iteration);
		//For each cluster
		for(int i=0; i < k; i++)
		{
			//For each point in each cluster compute edit distance to the centroids in other clusters and
			//relabel the point to the nearest cluster
			vector<int> distToOtherCentroids;
			int index=0;
			for(vector<string>::iterator it1=clusters[i].begin(); it1 != clusters[i].end() ; it1++) // for each point in cluster
			{
				distToOtherCentroids.clear();
				double minEditDistance=100000000.0;
				int closestClusterId=0;
				for(int p=0; p < k; p++) // for each cluster centroid 
				{
					//cout<<"*it1="<<*it1<<", "<<(*it1).length()<<endl;
					int ed=minEditDistance;
					if((*it1).length() > 0)
					{
						ed=asd.editDistanceWagnerFischer(*it1, centroids[p]);
						distToOtherCentroids.push_back(ed);
					}
					if (minEditDistance > ed)
					{
						minEditDistance=ed;
						closestClusterId=p;
					}
				}
				string movepoint=*it1;
				converged=true;
				if(closestClusterId != i) //if not the same cluster
				{
					cout<<"relabelling ["<<*it1<<"] to nearest cluster "<<closestClusterId<<" from cluster "<<i<<endl;
					clusters[closestClusterId].push_back(movepoint); // relabelled to nearest cluster
					//clusters[i].erase(index);
					it1=clusters[i].erase(it1);
					converged=false;
				}
				if(it1 == clusters[i].end())
					break;
				index++;
			}
		}
		
		//recompute centroids - average edit distance per cluster instead of usual [vector sum / number of vectors]
		//as an experiment
		int sumdist=0;
		string refstring("-------------------------------");
		for(int i=0; i < k; i++)
		{
			for(vector<string>::iterator it1=clusters[i].begin(); it1 != clusters[i].end(); it1++)
			{
				sumdist += asd.editDistanceWagnerFischer(*it1, refstring);
			}
			float centroid_distance = ((float) sumdist)/((float) clusters[i].size());
			float mindistancediff=50000.0;
			for(vector<string>::iterator it1=clusters[i].begin(); it1 != clusters[i].end(); it1++)
			{
				float dist = (float) asd.editDistanceWagnerFischer(*it1, refstring); 
				if(abs((int)(dist-centroid_distance)) < mindistancediff)
				{
					mindistancediff=abs((int)(dist-centroid_distance));
					centroids[i]=*it1;
				}	
			}
			sumdist=0;
		}	
		iteration++;
	}
	if(converged)
	{
		cout<<"KMeans clustering converged to:"<<endl;
		printClusters(iteration);
	}
}

void asferkmeansclustering::printClusters(int iteration)
{
	cout<<"############################################################"<<endl;
	cout<<"Iteration: "<<iteration<<endl;
	cout<<"############################################################"<<endl;
	for(int i=0; i < k; i++)
	{
		cout<<"==========="<<endl;
		cout<<"Cluster "<<i<<endl;
		cout<<"==========="<<endl;
		for(vector<string>::iterator it1=clusters[i].begin(); it1 != clusters[i].end(); it1++)
		{
			cout<<"encoded string ["<<*it1<<"] "<<endl;
		}
	}
	cout<<"############################################################"<<endl;
}
