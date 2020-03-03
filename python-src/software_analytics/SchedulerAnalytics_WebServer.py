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

from NeuronRain_Generic_WebServer import SocketWebServerDecorator
from SchedulerAnalytics_Config import scheduler_analytics_host,scheduler_analytics_port
from DeepLearning_SchedulerAnalytics import ProcessIterator

@SocketWebServerDecorator(scheduler_analytics_host,scheduler_analytics_port)
def get_stream_data():
        print "--------------------------------------------------------------------------------------------------"
        print "DeepLearning_SchedulerAnalytics.get_stream_data(): Process Iterator Wrapper"
        print "--------------------------------------------------------------------------------------------------"
        processiterator=ProcessIterator()
        return processiterator


try:
	get_stream_data()
except Exception as e:
	print "get_stream_data() exception:",e
