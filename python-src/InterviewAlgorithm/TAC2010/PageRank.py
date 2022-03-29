# -------------------------------------------------------------------------------------------------------
# NEURONRAIN ASFER - Software for Mining Large Datasets
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------------------------------
# K.Srinivasan
# NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
# Personal website(research): https://acadpdrafts.readthedocs.io/en/latest/
# --------------------------------------------------------------------------------------------------------

# PageRank algorithm
# By Peter Bengtsson
#    http://www.peterbe.com/
#    mail@peterbe.com
# License: BSD,http://opensource.org/licenses/bsd-license.php 
#
# Requires the numarray module
# http://www.stsci.edu/resources/software_hardware/numarray

#from numarray import *
import numpy
from numpy import *
import numpy.linalg as la

def _sum_sequence(seq):
    """ sums up a sequence """
    def _add(x,y): return x+y
    return reduce(_add, seq, 0)

class PageRanker:
    def __init__(self, p, webmatrix):
        assert p>=0 and p <= 1
        self.p = float(p)
        if type(webmatrix)in [type([]), type(())]:
            #webmatrix = array(webmatrix, Float)
	    webmatrix = array(webmatrix, numpy.float64)
        assert webmatrix.shape[0]==webmatrix.shape[1]
        self.webmatrix = webmatrix
	print 'webmatrix = ',
	print self.webmatrix
	
        # create the deltamatrix
        #imatrix = identity(webmatrix.shape[0], Float)
	imatrix = identity(webmatrix.shape[0], numpy.float64)
        for i in range(webmatrix.shape[0]):
            imatrix[i] = imatrix[i]*sum(webmatrix[i,:])
        #deltamatrix = la.inverse(imatrix)
	deltamatrix = la.inv(imatrix)
        self.deltamatrix = deltamatrix
	print 'deltamatrix = ',
	print self.deltamatrix

        # create the fmatrix
        #self.fmatrix = ones(webmatrix.shape, Float)
	self.fmatrix = ones(webmatrix.shape, numpy.float64)

        self.sigma = webmatrix.shape[0]

        # calculate the Stochastic matrix
        _f_normalized = (self.sigma**-1)*self.fmatrix
        _randmatrix = (1-p)*_f_normalized

        #_linkedmatrix = p * matrixmultiply(deltamatrix, webmatrix)
	_linkedmatrix = p * multiply(deltamatrix, webmatrix)
        M = _randmatrix + _linkedmatrix
        
        self.stochasticmatrix = M
	print 'M = ',
	print M
	
        #self.invariantmeasure = ones((1, webmatrix.shape[0]), Float)
	#self.stochasticmatrix = self.webmatrix
	self.invariantmeasure = ones((1, webmatrix.shape[0]), numpy.float64)
	print 'self.invariant =',
	print self.invariantmeasure

    def improve_guess(self, times=1):
        for i in range(times):
            self._improve()
            
    def _improve(self):
	print '######################################'
	print self.invariantmeasure
        #self.invariantmeasure = matrixmultiply(self.invariantmeasure, self.stochasticmatrix)
	self.invariantmeasure = multiply(self.invariantmeasure, self.stochasticmatrix)
	
    def get_invariant_measure(self):
        return self.invariantmeasure

    def getPageRank(self):
        sum = _sum_sequence(self.invariantmeasure[0])
        copy = self.invariantmeasure[0]
        for i in range(len(copy)):
            copy[i] = copy[i]/sum
        return copy


if __name__=='__main__':
    	# Example usage
	'''
	web = ((0, .2, .2, .2, .2, .2, 0),
           (.2, 0, .2, .2, .2, 0, .2),
           (.2, .2, 0, .2, .2, 0, .2),
           (.2, .2, .2, 0, .2, .2, 0),
    	    (.16, .16, .17, .17, 0, .17, .17),
    	   (.17, .17, .16, .17, .16, 0, .17),
    	   (.17, .17, .17, .17, .16, .16, 0))
	'''
	web = ((0,1,0,0),(0,0,1,0),(0,1,0,1),(1,1,0,0))
	pr = PageRanker(0.85, web)
    	pr.improve_guess(10)
	print '-----------------------------------'
	print 'Pagerank ='
    	print pr.getPageRank()
    
