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
#-----------------------------------------------------------------------------------------------------------------------------------

############################################################################################
#top - 14:30:25 up  1:43,  1 user,  load average: 0.13, 0.61, 0.71
#Tasks: 224 total,   1 running, 223 sleeping,   0 stopped,   0 zombie
#%Cpu(s):  3.7 us,  1.0 sy,  0.0 ni, 95.0 id,  0.2 wa,  0.0 hi,  0.2 si,  0.0 st
#KiB Mem :  3060516 total,   238584 free,  1655272 used,  1166660 buff/cache
#KiB Swap:  3103740 total,  2923336 free,   180404 used.   347920 avail Mem 
#  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
#  836 root      20   0  179464  28756  21896 S   2.6  0.9   2:47.71 Xorg
# 1516 shriniv+  20   0  118984  30696  25328 S   2.3  1.0   0:16.08 gnome-terminal-
# 2244 shriniv+  20   0 1053416 666728 503040 S   2.0 21.8   4:32.93 chromium-browse
# 1139 shriniv+  20   0  561832 232600  71696 S   0.7  7.6   1:04.08 chromium-browse
# 1390 shriniv+  20   0  247364  61084  31688 S   0.7  2.0   2:56.09 compiz
# 1352 shriniv+  20   0   29172   4588   4548 S   0.3  0.1   0:00.36 at-spi2-registr
# 1810 shriniv+  20   0 1492036 182208  80648 S   0.3  6.0   8:55.66 chromium-browse
# 2141 shriniv+  20   0  441960 122380  71740 S   0.3  4.0   0:25.10 chromium-browse
# 3790 root      20   0    8088   3564   3028 R   0.3  0.1   0:00.17 top
#    1 root      20   0   24228   4336   3344 S   0.0  0.1   0:04.26 systemd
############################################################################################
# Following DeepLearning models learn from 3 variable inputs - CPU, Memory and TIME+ data
# for each process id row in previous example top display - BackPropagation, RecurrentLSTM
# RecurrentGRU and ConvolutionNetwork models learn software analytics neural networks from training data
# This is very fundamental analytics which is a function of CPU, Memory usages and time duration
# for each process. 
############################################################################################

from DeepLearning_BackPropagation import BackPropagation
from DeepLearning_LSTMRecurrentNeuralNetwork import LSTMRecurrentNeuralNetwork
from DeepLearning_GRURecurrentNeuralNetwork import GRURecurrentNeuralNetwork
from DeepLearning_ConvolutionNetwork_BackPropagation import DeepLearningConvolution
import pprint
import random
import psutil

if __name__=="__main__":
	print "##########################################################################################"
	print "BackPropagation"
	print "##########################################################################################"
        #parameters - initial conditions - inputlayer,hiddenlayer,expectedoutput,weights_array
	sample=0
	while sample < 2:
		cpu_percent=psutil.cpu_percent()/10000.0
		cpu_percent=psutil.cpu_percent()/10000.0
		virtmem=psutil.virtual_memory()
		virtmem=psutil.virtual_memory()
		memory_percent=virtmem.percent/10000.0
		diskusage=psutil.disk_usage("/media/")
		diskusage=psutil.disk_usage("/media/")
		disk_percent=diskusage.percent/10000.0
	
		print "Process perf variables: [cpu_percent,memory_percent,disk_percent]"
		print [cpu_percent,memory_percent,disk_percent]
		iter=0
		weights=[0.01,0.023,0.056,0.043,0.099,0.088,0.033,0.021,0.12,0.23,0.34,0.45,0,11,0.56,0.77,0.21,0.88,0.92]
		#parameters - initial conditions - inputlayer,hiddenlayer,expectedoutput,weights_array
		inputlayer=[cpu_percent,memory_percent,disk_percent]
		hiddenlayer=[0.8,0.9,0.3]
		expectedoutput=[0.999999,0.999999,0.999999]
        	bpnn=BackPropagation(inputlayer,hiddenlayer,expectedoutput,weights)
        	bpnn.compute_neural_network()
        	bpnn.print_layers()
        	print "Error before Backpropagation:"
        	print bpnn.output_error(bpnn.output_layer,bpnn.expected_output_layer)
		while iter < 10000:
               		for m in xrange(len(inputlayer)):
                       		for l in xrange(len(inputlayer)):
                               		bpnn.backpropagation_pde_update_hidden_to_output(m,len(weights)/2 + len(inputlayer)*m + l)

               		for m in xrange(len(inputlayer)):
                       		for l in xrange(len(inputlayer)):
                               		bpnn.backpropagation_pde_update_input_to_hidden(m,len(inputlayer)*m+l)

               		print "Recomputing Neural Network after backpropagation weight update"
               		bpnn.compute_neural_network()
               		print "Error after Backpropagation- iteration :",iter
               		print bpnn.output_error(bpnn.output_layer,bpnn.expected_output_layer)
               		print "Layers in this iteration:"
               		bpnn.print_layers()
               		print "Weights updated in this iteration:"
              		print bpnn.weights
               		iter=iter+1
        	print "Software Analytics - BackPropagation - Error after Backpropagation- iteration :",iter
		bpnn.output_error(bpnn.output_layer,bpnn.expected_output_layer)
        	print "Software Analytics - BackPropagation - Layers in this iteration:"
		bpnn.print_layers()
        	print "Software Analytics - BackPropagation - Weights updated in this iteration:",bpnn.weights
		sample += 1
	
	print "##################################################################################"
	print "LSTM Recurrent Neural Network"
	print "##################################################################################"
	cellvars=[0.01,0.2,0.3]
        cellweights=[0.8,0.4,0.1]
        inputvars=[0.026,0.009,2.75/18.0]
        inputweights=[0.1,0.2,0.3]
        forgetvars=[0.01,0.5,0.14]
        forgetweights=[0.4,0.2,0.5]
        outputvars=[0.1,0.5,0.2]
        outputweights=[0.11,0.445,0.24]
        iteration = 0
        lstmRNN=LSTMRecurrentNeuralNetwork(cellvars, cellweights, inputvars, inputweights, forgetvars, forgetweights, outputvars, outputweights)
        while iteration < 100:
                lstmRNN.compute_cell_input_product1_level1()
                lstmRNN.compute_forget_feedback_product2_level1()
                lstmRNN.compute_product1_product2_sum1_level2()
                lstmRNN.compute_sum1_output_product1_level3()
                print "Iteration: ", iteration, " Final LSTM Recurrent Neural Network out value = ", lstmRNN.sum1_output_product1_level3
                print "####################################################################################################################"
                iteration += 1
        print "Software Analytics - LSTM Recurrent Neural Network - Final LSTM Recurrent Neural Network out value = ", lstmRNN.sum1_output_product1_level3

	print "##################################################################################"
	print "GRU Recurrent Neural Network"
	print "##################################################################################"
	cellvars=[0.01,0.2,0.3]
        cellweights=[0.8,0.4,0.1]
        inputvars=[0.026,0.009,2.75/18.0]
        inputweights_cell=[0.21,0.05,0.7]
        inputweights_update=[0.1,0.45,0.33]
        inputweights_reset=[0.4,0.05,0.3]
        updatevars=[0.02,0.3,0.05]
        updateweights=[0.1,0.02,0.3]
        resetvars=[0.01,0.05,0.14]
        resetweights=[0.04,0.2,0.5]

	GRURNN=GRURecurrentNeuralNetwork(cellvars, cellweights, inputvars, inputweights_cell, inputweights_update, inputweights_reset, updateweights, resetweights)
        while iteration < 1000:
                GRURNN.compute_update_input_htprev_gate()
                GRURNN.compute_reset_input_htprev_gate()
                GRURNN.compute_cell_htprev_reset_product()
                GRURNN.compute_update_cell_product()
                print "####################################################################################################################"
                iteration += 1
                print "Iteration:",iteration
                print "state at time t",GRURNN.ht
                print "Cellvars:",GRURNN.cellvars
                print "Update gate:",GRURNN.update_input_htprev
                print "Reset gate:",GRURNN.reset_input_htprev
        print "Software Analytics - GRU Recurrent Neural Network - state at time t",GRURNN.ht
        print "Software Analytics - GRU Recurrent Neural Network - Cellvars:",GRURNN.cellvars
        print "Software Analytics - GRU Recurrent Neural Network - Update gate:",GRURNN.update_input_htprev
        print "Software Analytics - GRU Recurrent Neural Network - Reset gate:",GRURNN.reset_input_htprev

	print "##################################################################################"
	print "Convolution Neural Network + BackPropagation"
	print "##################################################################################"
	input_bitmap11=[[0.026,0.009,2.75/18.0,0,0,0,0,0,0,0],
			[0.023,0.01,0.25/18.0,0,0,0,0,0,0,0],
			[0.02,0.21,4.5/18.0,0,0,0,0,0,0,0],
			[0.007,0.76,1.07/18.0,0,0,0,0,0,0,0],
			[0.007,0.02,3.0/18.0,0,0,0,0,0,0,0],
			[0.003,0.001,0.05/18.0,0,0,0,0,0,0,0],
			[0.003,0.06,9.0/18.0,0,0,0,0,0,0,0],
			[0.003,0.04,0.5/18.0,0,0,0,0,0,0,0],
			[0.003,0.001,0.02/18.0,0,0,0,0,0,0,0],
			[0,0.001,0.6/18.0,0,0,0,0,0,0,0]]

	dlc11=DeepLearningConvolution(input_bitmap11)

	#maximum stride is 5
	convolution_stride=2
	conv_map11=dlc11.convolution(convolution_stride)

	#maximum pool sliding window width is 5
	pool_slidewindow_width=2
	pool_map11=dlc11.max_pooling(pool_slidewindow_width)

	print "##########################################"
	print "Set of Convolution Maps"
	print "##########################################"
	print "Example 11:"
	print "###########"
	pprint.pprint(conv_map11)
	print "##########################################"
	print "Max Pooling Map"
	print "##########################################"
	print "Example 11:"
	print "###########"
	pprint.pprint(pool_map11)
	print "####################################################################################################"
	print "Final layer that connects all neurons in max pooling map and does backpropagation"
	print "####################################################################################################"
	maxpool_map_width=5
	print "###########################################################################################"
	print "Inference from Max Pooling Layer" 
	print "###########################################################################################"
	print "Example 11:"
	print "###########"
	print "Software Analytics - Convolution Network + BackPropgation - max pooling inference:",dlc11.infer_from_max_pooling(pool_map11,maxpool_map_width)
