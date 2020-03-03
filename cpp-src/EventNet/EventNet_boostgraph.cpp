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

//=======================================================================
// Copyright 2001 Jeremy G. Siek, Andrew Lumsdaine, Lie-Quan Lee, 
//
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
//=======================================================================

/*
boost graph library example modified for EventNet
*/

#include "EventNet_boostgraph.h"
#include <iostream>
#include <fstream>
#include <iostream>
#include <boost/tokenizer.hpp>
#include <string>


#include <boost/config.hpp>
#include <boost/graph/graph_traits.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/dijkstra_shortest_paths.hpp>
#include <boost/graph/topological_sort.hpp>
#include <boost/graph/strong_components.hpp>
#include <boost/graph/graphviz.hpp>
#include <boost/graph/graph_utility.hpp>

using namespace boost;
using namespace std;

struct Vertex
{
	string event_vertex;
	string event_partakers;
	string event_conversations;
}; 

int main(int argc,char* argv[])
{
  typedef adjacency_list < listS, vecS, directedS,
  	 no_property, property < edge_weight_t, int > > graph_t;
  typedef graph_traits < graph_t >::vertex_descriptor vertex_descriptor;
  typedef graph_traits < graph_t >::edge_descriptor edge_descriptor;
  typedef std::pair<int,int> Edge;

  ifstream edgesfile1;
  edgesfile1.open("EventNetEdges.txt",ifstream::in);
  ifstream verticesfile1;
  verticesfile1.open("EventNetVertices.txt",ifstream::in);
  char line[256];
  int num_nodes=0;
  int num_edges=0;
  while(!edgesfile1.eof())
  {
	edgesfile1.getline(line,256);
	num_edges++;
  }
  while(!verticesfile1.eof())
  {
	verticesfile1.getline(line,256);
	num_nodes++;
  }

  //enum nodes { A, B, C, D, E };
  //Edge edge_array[] = { Edge(A, C), Edge(B, B), Edge(B, D), Edge(B, E),
  //  Edge(C, B), Edge(C, D), Edge(D, E), Edge(E, A), Edge(E, B)
  //};
  Edge edge_array[num_edges];
  Vertex vertex_array[num_nodes];
  
  //int weights[] = { 1, 2, 1, 2, 7, 3, 1, 1, 1 };
  int weights[num_nodes*num_nodes];
  string name[num_nodes];


  ifstream edgesfile;
  edgesfile.open("EventNetEdges.txt",ifstream::in);
  ifstream verticesfile;
  verticesfile.open("EventNetVertices.txt",ifstream::in);

  boost::char_separator<char> sep(",");
  int e=0;
  int v=0;
  while(!edgesfile.eof())
  {
	edgesfile.getline(line,256);
	string text(line);
	tokenizer<char_separator<char> > tokens(text, sep);
	string edge[2];
	int i=0;
	cout<<"edge:"<<endl;
	for(tokenizer<char_separator<char>>::iterator tok=tokens.begin(); tok != tokens.end(); tok++,i++)
	{
		edge[i] = *tok;
		cout<<" "<<*tok<<endl;
	}
	if(edge[1] != "" && edge[0] != "")
	{
		edge_array[e]=Edge(atoi(edge[0].c_str()),atoi(edge[1].c_str()));
		cout<<"edge_array[e].first="<<edge_array[e].first<<"; edge_array[e].second="<<edge_array[e].second<<endl;
		weights[e]=1;
		e++;
	}
  }

  boost::char_separator<char> sep2("-");
  while(!verticesfile.eof())
  {
	verticesfile.getline(line,256);
	string text(line);
	tokenizer<char_separator<char> > tokens(text, sep2);
	string vertex[3];
	int i=0;
	cout<<"vertex: "<<endl;
	for(tokenizer<char_separator<char>>::iterator tok=tokens.begin(); tok != tokens.end(); tok++,i++)
	{
		vertex[i] = *tok;
		cout<<" "<<*tok<<endl;
	}
	if(vertex[0] != "")
	{
		name[v]=vertex[0];
		cout<<"name["<<v<<"] :"<<name[v]<<endl;
		vertex_array[v].event_vertex=vertex[0];
		vertex_array[v].event_partakers=vertex[1];
		vertex_array[v].event_conversations=vertex[2];
		v++;
	}
  }

  int num_arcs = sizeof(edge_array) / sizeof(Edge);

#if defined(BOOST_MSVC) && BOOST_MSVC <= 1300
  graph_t g(num_nodes);
  property_map<graph_t, edge_weight_t>::type weightmap = get(edge_weight, g);
  for (std::size_t j = 0; j < num_arcs; ++j) {
    edge_descriptor e; bool inserted;
    boost::tie(e, inserted) = add_edge(edge_array[j].first, edge_array[j].second, g);
    weightmap[e] = weights[j];
  }
#else
  graph_t g(edge_array, edge_array + num_arcs, weights, num_nodes);
  remove_edge(0,0,g);
  remove_vertex(num_nodes,g);
  property_map<graph_t, edge_weight_t>::type weightmap = get(edge_weight, g);
#endif
  std::vector<vertex_descriptor> p(num_vertices(g));

  std::ofstream dot_file;
  dot_file.open("EventNet_BoostGL.dot",ofstream::out);
  dot_file << "digraph D {\n"
    << "  rankdir=LR\n"
    << "  size=\"4,3\"\n"
    << "  ratio=\"fill\"\n"
    << "  edge[style=\"bold\"]\n" << "  node[shape=\"circle\"]\n";

  for(int i=0;i < num_nodes;i++)
  {
	if(vertex_array[i].event_vertex != "")
	{
  		dot_file<<"\""<<vertex_array[i].event_vertex<<"\" [Label=\""<<vertex_array[i].event_partakers<<"\"]"<<endl;
	}
  }

  graph_traits < graph_t >::edge_iterator ei, ei_end;
  int k=0;
  for (boost::tie(ei, ei_end) = edges(g); ei != ei_end; ++ei) {
    graph_traits < graph_t >::edge_descriptor e = *ei;
    graph_traits < graph_t >::vertex_descriptor u = source(e, g), v = target(e, g);
    cout<<"u="<<u<<",v="<<v<<endl;
    if(edge_array[k].first != edge_array[k].second)
    {
   	cout << name[u] << " -> " << name[v] << endl;
   	//dot_file << edge_array[k].first << " -> " << edge_array[k].second << "[label=\"" << weights[k] << "\"";
   	dot_file << name[u] << " -> " << name[v] << "[label=\"" << weights[k] << "\"";
	/*
    	if (p[v] == u)
     		dot_file << ", color=\"black\"";
    	else
	*/
      		dot_file << ", color=\"grey\"";
    	dot_file << "]"<<endl;
    }
    k++;
  }
  dot_file << "}"<<endl;

  bool has_cycle=false;
  cycle_detector cyc_det(has_cycle);
  boost::depth_first_search(g, visitor(cyc_det));
  cout<<"EventNet has cycle?: "<<has_cycle<<endl;

  typedef std::vector< vertex_descriptor > container;
  container c;
  topological_sort(g, std::back_inserter(c));

  deque<vertex_descriptor> c2;
  topological_sort(g, std::front_inserter(c2));

  cout<<"===================================="<<endl;
  cout<<"topological ordering(back_inserter):"<<endl;
  cout<<"===================================="<<endl;
  std::ofstream toposort_file;
  toposort_file.open("EventNetOrdering.txt",ofstream::out);

  int i=0;
  for(container::reverse_iterator it=c.rbegin();it != c.rend();it++,i++)
  {
	cout<<i<<" - "<<*it<<endl;
	toposort_file<<i<<" - "<<*it<<" "<<endl;
  }

  cout<<"===================================="<<endl;
  cout<<"topological ordering(front_inserter):"<<endl;
  cout<<"===================================="<<endl;
  i=0;
  for(vertex_descriptor it2: c2)
  {
	cout<<i<<" - "<<it2<<endl;
	i++;
  }
 
  cout<<"===================================="<<endl;
  cout<<"vertices"<<endl;
  cout<<"==========="<<endl;
  typename graph_traits<graph_t>::vertex_iterator n,end;
  for(tie(n,end) = vertices(g); n != end; n++)
  {
	cout<<*n<<endl;
  }

  std::vector<int> component(num_vertices(g)), discover_time(num_vertices(g));
  std::vector<default_color_type> color(num_vertices(g));
  std::vector<vertex_descriptor> root(num_vertices(g));
  int num = strong_components(g, make_iterator_property_map(component.begin(), get(vertex_index, g)), 
                              root_map(make_iterator_property_map(root.begin(), get(vertex_index, g))).
                              color_map(make_iterator_property_map(color.begin(), get(vertex_index, g))).
                              discover_time_map(make_iterator_property_map(discover_time.begin(), get(vertex_index, g))));
 
  cout<<"===================================="<<endl;
  std::cout << "Total number of Strongly Connected components: " << num << std::endl;
  cout<<"===================================="<<endl;
  std::vector<int>::size_type t;
  for (t = 0; t != component.size(); ++t)
    std::cout << "Vertex " << name[t]
         <<" is in component " << component[t] << std::endl;

/*
  adjacency_list<vecS, vecS, directedS> g2;
  dynamic_properties dp;
  read_graphviz("EventNet_BoostGL.dot", g2, dp);

  std::cout << "A directed graph:" << std::endl;
  print_graph(g2, "EventNet_BoostGL.boostgraph");
*/


  return EXIT_SUCCESS;
}
