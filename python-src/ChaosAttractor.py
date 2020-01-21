#------------------------------------------------------------------------------------------------------------
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
#---------------------------------------------------------------------------------------------------------
#K.Srinivasan
#NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
#Personal website(research): https://sites.google.com/site/kuja27/
#---------------------------------------------------------------------------------------------------------

import rpy2.robjects as robj

#non-linearity starts from k >= 3 and below 3 there are periods
input_seq=[]
#correlation_flag="linear"
correlation_flag="chaotic"

def plotGraph(x):
	no_of_hashes=x*100
	for i in xrange(int(no_of_hashes)):
		print "#",
	print "\n"

#Chaotic PRG implementation - Verhulste's Logistic equation and Lehmer-Palmore Pseudorandom generator
def ChaosPRG(algorithm="Logistic",seqlen=100,radix=10,initialcondition=0.7,prime=104729):
    x=initialcondition
    k=radix
    chaos_seq=[]
    print "ChaosPRG() algorithm:",algorithm
    while True:
        if algorithm == "Logistic":
	    xnext = k*x*(1-x)	
        if algorithm == "Lehmer-Palmore":
            xnext = (k * x) % prime
	print "x: ",x,", xnext: ",xnext
	#plotGraph(xnext)
	chaos_seq.append(float(x)*100000)
	x=xnext
	if len(chaos_seq) == seqlen:
		break
    return chaos_seq

if __name__=="__main__":
    #Read input sequence
    #f=open("ChaosAttractorInputSequence.txt")
    f=open("ChaosAttractorInputSequence_DJIA.txt")
    f_str=f.read()
    input_seq=f_str.split(",")

    #using rpy2.objects and compute R correlation coefficient
    if correlation_flag == "chaotic":
        chaosx = robj.FloatVector(ChaosPRG("Logistic",19449,3.8,0.7,104729))
        #chaosx = robj.FloatVector(ChaosPRG("Lehmer-Palmore",19449,3.8,0.7,104729))
    if correlation_flag == "linear":
	chaosx = robj.FloatVector(xrange(19449))
    print "Chaotic PRG sequence:",chaosx 
    inputstreamy = robj.FloatVector(input_seq[0:19449])
    corfn = robj.r['cor']
    corfn(chaosx,inputstreamy)
    ret=corfn(chaosx,inputstreamy)
    print "correlation coefficient of pseudorandom and DJIA sequences is:", (ret.r_repr())
