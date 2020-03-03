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

import socket

class SocketWebServerDecorator(object):
	def __init__(self,host,port):
		print "SocketWebServerDecorator.__init__():"
		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.s.bind((host,port))
		self.s.listen(100)
	
	def __call__(self,datasourcefunc):
		self.conn,self.addr = self.s.accept()
		cnt=1
		while True:
			dataiterator=datasourcefunc()
			try:
				for data in dataiterator:	
					print "SocketWebServerDecorator.__call__(): data cnt:",cnt
					cnt+=1
					if data is not None:
						ret=self.conn.send(str(data[0]))
						print "conn.send() returned :",ret
					else:
						print "data is None"
			except Exception as e:
				print "__call__() exception:",e
