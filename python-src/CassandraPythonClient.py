#--------------------------------------------------------------------------------------------------------
#ASFER - a ruleminer which gets rules specific to a query and executes them (component of iCloud Platform)
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
#
#-----------------------------------------------------------------------------------------------------
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Ph: 9789346927, 9003082186, 9791165980
#Krishna iResearch Open Source Products Profiles: 
#http://sourceforge.net/users/ka_shrinivaasan, https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#ZODIAC DATASOFT: https://github.com/shrinivaasanka/ZodiacDatasoft
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, 
#kashrinivaasan@live.com
#-----------------------------------------------------------------------------------------------------

from cassandra.cluster import Cluster
cl=Cluster()
session = cl.connect('cassandrakeyspace')

inputf=open('movielens_stream2.data')
for line in inputf:
	linetoks=line.split(' ')
	query='INSERT INTO stream_data(row_id,alphanum) VALUES (\''+linetoks[0]+'\',\''+linetoks[1]+'\');'
	print query
	session.execute(query)
query='SELECT * FROM stream_data'
resultrows=session.execute(query)
for row in resultrows:
	print row.row_id,' ',row.alphanum

