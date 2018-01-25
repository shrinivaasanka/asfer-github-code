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
#Personal website(research): https://sites.google.com/site/kuja27/
#--------------------------------------------------------------------------------------------------------
*********************************************************************************************************/

#include "asferkNNclustering.h"
#include "asferstringdistance.h"
#include <string>
#include <unordered_map>
#include <vector>

extern std::string asferroot;

unordered_map<string,int> labelled_points; // each entry has key:value of <encoded_string,cluster_id>

#define MAX_NO_CLUSTERS 10 

void asferknnclustering::kNNClustering(string distancemetric)
{
        bool converged=false;

        asferstringdistance asd;

	int max_no_of_points=0;
	int max_cluster_id=0;

	//training labelled dataset
        ifstream input1;
        char line1[256];
        char line2[256];
        string encstrpath1(asferroot);
        encstrpath1.append("/asfer.enterprise.encstr.kNN");
        input1.open(encstrpath1.c_str(), ifstream::in);
	labelled_points.clear();
	
	int i=0;
        while (!input1.eof())
        {
               input1.getline(line1,256);
               string encstrtr(line1);
	       if(encstrtr != "")
	       {
			cout<<"training dataset : encstrtr = "<<encstrtr<<endl;
			labelled_points[encstrtr] = i % MAX_NO_CLUSTERS;
	       		i++;
	       }
        }
	
	cout<<"Before kNN clustering"<<endl;
	printClusters();
                                            
       	//kNN clustering classification 
        ifstream input2;
        string encstrpath2(asferroot);
        encstrpath2.append("/asfer.enterprise.encstr");
        input2.open(encstrpath2.c_str(), ifstream::in);

        while (!input2.eof()) //for each unlabelled encoded string 
        {
                input2.getline(line2,256);
                string encstrtr(line2);
		if(encstrtr != "")
		{
			int editdistance_radius=8;
	      		unordered_map<string,int> kNearestNeighbours; // <encoded_string,cluster_id>
 
			printClusters();
			for(unordered_map<string,int>::iterator it1 = labelled_points.begin(); it1 != labelled_points.end(); it1++) // for each labelled encoded string
			{
				//compute distance to all labelled points from this unlabelled point
				//and create a map of k Nearest neighbours that are with in a
				//radius edit distance
	       			int ed;
				cout<<"kNNClustering iteration: encstrtr = "<<encstrtr<<endl;
				if(it1->first != "")
				{
					ed = asd.editDistanceWagnerFischer(encstrtr, it1->first);
					if(ed < editdistance_radius)
					{
						kNearestNeighbours[it1->first] = it1->second;
					}
				}
			}	
			
			//find the cluster id label that is
			//in majority in above k Nearest Neighbours
			unordered_map<int,int> labelMajority; // <cluster_id, no_of_points_in_cluster>
			for(unordered_map<string,int>::iterator it2 = kNearestNeighbours.begin(); it2 != kNearestNeighbours.end(); it2++)
			{
				//if(it2->first != "")
					labelMajority[it2->second]++;
			}
			
			for(unordered_map<int,int>::iterator it3 = labelMajority.begin(); it3 != labelMajority.end(); it3++)
			{
				if(it3->second > max_no_of_points)
				{
					max_no_of_points = it3->second;
					max_cluster_id = it3->first;
				}
			}
			//label with max_cluster_id
			labelled_points[encstrtr]=max_cluster_id;
			max_no_of_points=0;
			max_cluster_id=0;
        	}
	}
	printClusters();
}

void asferknnclustering::printClusters()
{
	cout<<"================================================="<<endl;
	cout<<"kNN clustering"<<endl;
	cout<<"================================================="<<endl;
	for(unordered_map<string,int>::iterator it1 = labelled_points.begin(); it1 != labelled_points.end(); it1++) // for each labelled encoded string
	{
		cout<<"cluster id ["<<it1->second<<"] ------- encodedstr ["<<it1->first<<"]"<<"; encodedstr.length() = "<<it1->first.length()<<endl;
	}
}
