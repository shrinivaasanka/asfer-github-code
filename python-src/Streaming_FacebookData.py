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

import sys
import facebook
import requests

def facebook_graph():
	token="EAACvK6dFKs8BAJ2jNabZBci3HQUmjwd8tZAeekltnBmQtS9eV2GBDVbiNTM4Y2y2krUFp6xJOSlAdzxrjsuLsTsQcB9RawdFdT0gzpfZBJuZCyJmvZAtBATk3xxL8eSPplt8M3mzXXdB3OyCuqIavrsAPto847d0ZD"
	#user="X"

	graph=facebook.GraphAPI(access_token=token,version=3.0)
	#profile=graph.get_object(user)
	#posts = graph.get_connections(profile['id'], 'posts')
	search_results=graph.request("me", {"fields":"name"})
	print(search_results)

if __name__=="__main__":
	facebook_graph()
