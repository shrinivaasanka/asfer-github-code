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

############################################################################################
#Scheduler Analytics for Linux Kernel:
#=====================================
# Following DeepLearning models learn from process perf variables - CPU, Memory, Context switches, Number of Threads and Nice data
# for each process id retrieved by psutil process iterator - BackPropagation, RecurrentLSTM
# RecurrentGRU and ConvolutionNetwork models learn software analytics neural networks from psutil process performance info 
# Key value pairs learnt from these can be read by Linux Kernel Scheduler or anything else
# and suitably acted upon for changing the process priorities dynamically. Any kernel module can make an upcall to this userspace
# executable and dump the key-value pairs in /etc/kernel_analytics.conf. Presently the implementation is quite primitive and
# classifies the output layer of neural network into "Highest, Higher, High, Normal, Medium, Low, Lower and Lowest" priority classes
# in the format: <pid>=<scheduled_priority_class>. Number of iterations has been set to 10 for all deep learning networks.
############################################################################################

from DeepLearning_BackPropagation import BackPropagation
from DeepLearning_LSTMRecurrentNeuralNetwork import LSTMRecurrentNeuralNetwork
from DeepLearning_GRURecurrentNeuralNetwork import GRURecurrentNeuralNetwork
from DeepLearning_ConvolutionNetwork_BackPropagation import DeepLearningConvolution
import pprint
import random
import psutil
import numpy
import json
import pprint
from dictdiffer import diff
import hashlib
from SparkKernelLogMapReduceParser import log_mapreducer
from ImageToBitMatrix import image_to_bitmatrix
import Streaming_AbstractGenerator

expected_process_priorities_input=open("DeepLearning_SchedulerAnalytics.input","r")
expected_process_priorities=json.loads(expected_process_priorities_input.read())
encodedprocessesfile=open("./asfer.enterprise.encstr.scheduleranalytics","w")
procdict=True
prevprocessfeatures=None
processfeatures=None
processesfeatures=[]
numproc=0
process_md5hash_string=False

class ProcessIterator(object):
        def __iter__(self):
                self.psutilprocessiter=psutil.process_iter()
                for process in self.psutilprocessiter:
			if process is not None:
				processfeatures=process_feature_vector(process)
				yield processfeatures
			else:
				yield "{No Process from PsUtil Iterator}"

def getHash(str):
        h=hashlib.new("ripemd160")
        h.update(str)
        hash=bin(int(h.hexdigest(),16))
        print "hash for string [",str,"] :",hash
        return hash

def process_feature_vector(proc):
	#process = <pid, processname, executable, memory_info, connections, ioinfo>
	feature_vector=[]
	if procdict==False:
		proc_pid=proc.pid
		feature_vector.append(proc_pid)
		proc_cmdline=proc.cmdline()
		feature_vector.append(proc_cmdline)
		proc_name=proc.name()
		proc_name=proc.name()
		feature_vector.append(proc_name)
		proc_exe=proc.exe()
		proc_exe=proc.exe()
		feature_vector.append(proc_exe)
		proc_meminfo=proc.memory_full_info()
		proc_meminfo=proc.memory_full_info()
		feature_vector.append(proc_meminfo)
		proc_connections=proc.connections()
		proc_connections=proc.connections()
		feature_vector.append(proc_connections)
		proc_iocounters=proc.io_counters()
		proc_iocounters=proc.io_counters()
		feature_vector.append(proc_iocounters)
	else:
		proc_dict=proc.as_dict()
		feature_vector.append(proc_dict)
	#pprint.pprint(feature_vector)
	return feature_vector

def is_prioritizable(proc_name):
	#print "is_prioritizable(): proc_name:",proc_name
	for k,v in expected_process_priorities.iteritems():
		if proc_name.find(k) != -1:
			prioritizable=True
			break
		else:
			prioritizable=False
	return prioritizable

def get_expected_priority(output_layer_index,proc_name):
	print "get_expected_priority(): proc_name:",proc_name
	for k,v in expected_process_priorities.iteritems():
		print k,v
		if proc_name.find(k) != -1:
			return v*output_layer_index/10.0
	return 0.1	

def sched_debug_runqueue():
	print "-------------------"
	print "Scheduler Runqueue"
	print "-------------------"
	iter=0
	runqueuedict={}
	#print "----------------------------------------------------"
	runqueuedict[iter]=["task","PID","tree-key","switches","prio","exec-runtime","sum-exec","sum-sleep"]
	#print "----------------------------------------------------"
	scheddebug=open("/proc/sched_debug","r")
	lines=scheddebug.readlines()
	lines.reverse()
	for line in lines:
		if "tree-key" in line or "---------" in line:
			break
		linefields=line.split()
		if len(linefields) > 0:
			runqueuedict[str(iter)]=linefields
		iter += 1
	return runqueuedict
				
def learnt_scheduler_class(deep_learnt_output, sysctl=False):	
	mean=numpy.mean(deep_learnt_output)
	if sysctl==True:
		if mean > 0.9:
			return 	["kernel.sched_latency_ns=9000000",
				"kernel.sched_migration_cost_ns=100000",
				"kernel.sched_wakeup_granularity_ns=2000000",
				"kernel.rr_timeslice_ms=10",
				"kernel.sched_rt_runtime_us=990000",
				"kernel.sched_nr_migrate=12",
				"kernel.sched_time_avg_ms=100"]
		elif mean > 0.8:
			return 	["kernel.sched_latency_ns=8000000",
				"kernel.sched_migration_cost_ns=90000",
				"kernel.sched_wakeup_granularity_ns=1800000",
				"kernel.rr_timeslice_ms=9",
				"kernel.sched_rt_runtime_us=890000",
				"kernel.sched_nr_migrate=11",
				"kernel.sched_time_avg_ms=90"]
		elif mean > 0.7:
			return 	["kernel.sched_latency_ns=7000000",
				"kernel.sched_migration_cost_ns=80000",
				"kernel.sched_wakeup_granularity_ns=1700000",
				"kernel.rr_timeslice_ms=8",
				"kernel.sched_rt_runtime_us=790000",
				"kernel.sched_nr_migrate=10",
				"kernel.sched_time_avg_ms=80"]
		elif mean > 0.5:
			return 	["kernel.sched_latency_ns=6000000",
				"kernel.sched_migration_cost_ns=70000",
				"kernel.sched_wakeup_granularity_ns=1600000",
				"kernel.rr_timeslice_ms=7",
				"kernel.sched_rt_runtime_us=690000",
				"kernel.sched_nr_migrate=9",
				"kernel.sched_time_avg_ms=70"]
		elif mean > 0.4:
			return 	["kernel.sched_latency_ns=5000000",
				"kernel.sched_migration_cost_ns=60000",
				"kernel.sched_wakeup_granularity_ns=1500000",
				"kernel.rr_timeslice_ms=6",
				"kernel.sched_rt_runtime_us=590000",
				"kernel.sched_nr_migrate=8",
				"kernel.sched_time_avg_ms=60"]
		elif mean > 0.3:
			return 	["kernel.sched_latency_ns=4000000",
				"kernel.sched_migration_cost_ns=50000",
				"kernel.sched_wakeup_granularity_ns=1400000",
				"kernel.rr_timeslice_ms=5",
				"kernel.sched_rt_runtime_us=490000",
				"kernel.sched_nr_migrate=7",
				"kernel.sched_time_avg_ms=50"]
		elif mean > 0.1:
			return 	["kernel.sched_latency_ns=3000000",
				"kernel.sched_migration_cost_ns=40000",
				"kernel.sched_wakeup_granularity_ns=1200000",
				"kernel.rr_timeslice_ms=4",
				"kernel.sched_rt_runtime_us=390000",
				"kernel.sched_nr_migrate=6",
				"kernel.sched_time_avg_ms=40"]
		else:
			return 	["kernel.sched_latency_ns=2000000",
				"kernel.sched_migration_cost_ns=30000",
				"kernel.sched_wakeup_granularity_ns=1100000",
				"kernel.rr_timeslice_ms=3",
				"kernel.sched_rt_runtime_us=290000",
				"kernel.sched_nr_migrate=5",
				"kernel.sched_time_avg_ms=30"]
	else:
		if mean > 0.9:
			return "Highest"
		elif mean > 0.8:
			return "Higher"
		elif mean > 0.7:
			return "High"
		elif mean > 0.5:
			return "Normal"
		elif mean > 0.4:
			return "Medium"
		elif mean > 0.3:
			return "Low"
		elif mean > 0.1:
			return "Lower"
		else:
			return "Lowest"	

#############################################################################################
if __name__=="__main__":
	schedrunqstream=Streaming_AbstractGenerator.StreamAbsGen("OperatingSystem","SchedulerRunQueue")
	runqcnt=0
	for runq in schedrunqstream:
		if runqcnt > 10:
			break
		print "Scheduler Runqueue Stream:",runq
		runqcnt+=1
	#log_mapreducer("perf.data.schedscript","sched_stat_runtime")
	kernel_analytics_conf=open("/etc/kernel_analytics.conf","w")
	weights=[0.01,0.023,0.056,0.043,0.099,0.088,0.033,0.021,0.12,0.23,0.34,0.45,0,11,0.56,0.77,0.21,0.88,0.92]
	hiddenlayer=[0.8,0.9,0.3]
	inputlayer=[0.01,0.01,0.01]
	expectedoutput=[0.1,0.1,0.1]
	bpnn=BackPropagation(inputlayer,hiddenlayer,expectedoutput,weights)
	for proc in psutil.process_iter():
		print "-------------------------------------------"
		print "Process Feature Vector:"
		print "-------------------------------------------"
		prevprocessfeatures=processfeatures
		processfeatures=process_feature_vector(proc)
		processesfeatures.append(processfeatures)
		numproc += 1
		if numproc == 2:
			exit
		#	json.dump(processesfeatures,encodedprocessesfile)
		if prevprocessfeatures != None:
			process_distance=list(diff(prevprocessfeatures,prevprocessfeatures))
			print "Distance between previous and previous processes:",len(process_distance)
			process_distance=list(diff(processfeatures,processfeatures))
			print "Distance between present and present processes:",len(process_distance)
			process_distance=list(diff(prevprocessfeatures,processfeatures))
			print "Distance between previous and present processes:",len(process_distance)
		proc_pid=proc.pid
		proc_cmdline=proc.cmdline()
		proc_name=proc.name()
		proc_name=proc.name()
		proc_exe=proc.exe()
		proc_exe=proc.exe()
	
		if not is_prioritizable(proc_name):
			continue	
	
		print "========================================================================================"
		print "Process id:", proc_pid
		print "Process cmdline:", proc_cmdline
		print "Process executable:",proc_exe
		print "Process name:",proc_name
		print "========================================================================================"
		cpu_percent=proc.cpu_percent(interval=1) / psutil.cpu_count()
		cpu_percent=proc.cpu_percent(interval=None) / psutil.cpu_count()
		ctxsw=proc.num_ctx_switches()
		num_ctx_switches=ctxsw[0]+ctxsw[1]
		num_involuntary_ctx_switches=ctxsw[1]
		num_threads=proc.num_threads()
		memory_percent=proc.memory_percent() / psutil.cpu_count()
		memory_percent=proc.memory_percent() / psutil.cpu_count()
		
		#assumes nice ranges from -20 to +20
		nice=float(proc.nice())/20.0 
	
		num_of_pids=len(psutil.pids())
	
		print "Process perf variables: [cpu_percent,num_involuntary_ctx_switches,num_ctx_switches,num_threads,memory_percent,nice]"
		print [cpu_percent,num_involuntary_ctx_switches,num_ctx_switches,num_threads,memory_percent,nice]
		
		print "##########################################################################################"
		print "BackPropagation"
		print "##########################################################################################"
		iter=0
		
		#parameters - initial conditions - inputlayer,hiddenlayer,expectedoutput,weights_array
		bpnn.input_layer=[cpu_percent/100.0,memory_percent/100.0,float(num_involuntary_ctx_switches)/float(num_ctx_switches)]

		bpnn.expected_output_layer=[get_expected_priority(1,proc_name),get_expected_priority(2,proc_name),get_expected_priority(3,proc_name)]
		print "Expected output layer:",bpnn.expected_output_layer
		#bpnn=BackPropagation(inputlayer,hiddenlayer,expectedoutput,weights)
		bpnn.compute_neural_network()
		bpnn.print_layers()
		print "Error before Backpropagation:"
		print bpnn.output_error(bpnn.output_layer,bpnn.expected_output_layer)
		while iter < 10:
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

		scheduler_class_bpnn=learnt_scheduler_class(bpnn.output_layer,True)
	
		print "##################################################################################"
		print "LSTM Recurrent Neural Network"
		print "##################################################################################"
		cellvars=[0.01,0.2,0.3]
		cellweights=[0.8,0.4,0.1]
		inputvars=[cpu_percent,memory_percent,nice]
		inputweights=[0.1,0.2,0.3]
		forgetvars=[0.01,0.5,0.14]
		forgetweights=[0.4,0.2,0.5]
		outputvars=[0.1,0.5,0.2]
		outputweights=[0.11,0.445,0.24]
		iteration = 0
		lstmRNN=LSTMRecurrentNeuralNetwork(cellvars, cellweights, inputvars, inputweights, forgetvars, forgetweights, outputvars, outputweights)
		while iteration < 10:
			lstmRNN.compute_cell_input_product1_level1()
			lstmRNN.compute_forget_feedback_product2_level1()
			lstmRNN.compute_product1_product2_sum1_level2()
			lstmRNN.compute_sum1_output_product1_level3()
			print "Iteration: ", iteration, " Final LSTM Recurrent Neural Network out value = ", lstmRNN.sum1_output_product1_level3
			print "####################################################################################################################"
			iteration += 1
		print "Software Analytics - LSTM Recurrent Neural Network - Final LSTM Recurrent Neural Network out value = ", lstmRNN.sum1_output_product1_level3
		scheduler_class_lstm=learnt_scheduler_class([lstmRNN.sum1_output_product1_level3])

		print "##################################################################################"
		print "GRU Recurrent Neural Network"
		print "##################################################################################"
		cellvars=[0.01,0.2,0.3]
		cellweights=[0.8,0.4,0.1]
		inputvars=[cpu_percent,memory_percent,nice]
		inputweights_cell=[0.21,0.05,0.7]
		inputweights_update=[0.1,0.45,0.33]
		inputweights_reset=[0.4,0.05,0.3]
		updatevars=[0.02,0.3,0.05]
		updateweights=[0.1,0.02,0.3]
		resetvars=[0.01,0.05,0.14]
		resetweights=[0.04,0.2,0.5]

		GRURNN=GRURecurrentNeuralNetwork(cellvars, cellweights, inputvars, inputweights_cell, inputweights_update, inputweights_reset, updateweights, resetweights)
		while iteration < 10:
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
		scheduler_class_gru=learnt_scheduler_class(GRURNN.ht)

		print "##################################################################################"
		print "Convolution Neural Network + BackPropagation"
		print "##################################################################################"
		input_bitmap11=[[cpu_percent,memory_percent,nice,0,0,0,0,0,0,0],
			[cpu_percent,memory_percent,nice,0,0,0,0,0,0,0],
			[cpu_percent,memory_percent,nice,0,0,0,0,0,0,0],
			[cpu_percent,memory_percent,nice,0,0,0,0,0,0,0],
			[cpu_percent,memory_percent,nice,0,0,0,0,0,0,0],
			[cpu_percent,memory_percent,nice,0,0,0,0,0,0,0],
			[cpu_percent,memory_percent,nice,0,0,0,0,0,0,0],
			[cpu_percent,memory_percent,nice,0,0,0,0,0,0,0],
			[cpu_percent,memory_percent,nice,0,0,0,0,0,0,0],
			[cpu_percent,memory_percent,nice,0,0,0,0,0,0,0]]

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
		scheduler_class_cnbp=learnt_scheduler_class(dlc11.infer_from_max_pooling(pool_map11,maxpool_map_width))
		print "Scheduled Classes by Deep Learning for process id ",proc.pid," - [BackPropagation, LSTM, GRU, Convolution] = ", [scheduler_class_bpnn,scheduler_class_lstm,scheduler_class_gru,scheduler_class_cnbp]
		kernel_analytics_conf.write(str(proc.pid) + "#BackPropagation=")
		kernel_analytics_conf.write(str(scheduler_class_bpnn))
		kernel_analytics_conf.write("\n")
		kernel_analytics_conf.write(str(proc.pid) + "#LSTM=" + scheduler_class_lstm + "\n")
		kernel_analytics_conf.write(str(proc.pid) + "#GRU=" + scheduler_class_gru + "\n")
		kernel_analytics_conf.write(str(proc.pid) + "#Convolution=" + scheduler_class_cnbp + "\n")

	#Pictorial Performance Pattern Mining by Convolution Network:
	#------------------------------------------------------------
	#Input to this Convolution Network is an image bitmap matrix obtained from some standard graphic
	#performance analyzers - runqueuelat, BPF/bcc-tools, perf etc., Following example image is created
	#by "perf timechart" on perf.data which captures the state,timeslice etc., information of list of
	#processes in scheduler at any instant in the form of a gantt chart. Backpropagation-Convolution is
	#then applied to this performance snapshot and convolution, maxpooling, final neuron layers are
	#computed as usual. This convolution is iterated periodically for stream of performance snapshot bitmaps.
	#Advantages of mining graphic images of performances captured periodically are:
	#	- number of dimensions of a performance snapshot image is 2 while psutils creates 1 dimensional 
	#	array stream of data per process id.
	#	- 2 dimensional performance snapshots are system wide and capture all process id(s) at a time
	#	and not process id specific. 
	#	- Recent advanced performance analyzers like BPF/bcc-tools provide a histogram equivalent of
	#	timechart in perf (runqueuelat) which is also an image bitmap. So support for graphic performance
	#	data analytics is futuristic.
	#	- Processing stream of performance snapshot image bitmaps by convolution to extract patterns is
	#	more universal/holistic than applying convolution to stream of process structure data
	#	- Specifically if remaining_clockticks-to-processes dynamic hash tables are available as 
	#	stream of histogram images, applying convolution on this stream creates frequent recurring
	#	patterns of queueing in OS Scheduler 

	print "###########################################################"
	print "Convolution on 2 dimensional graphic performance data stream"
	print "############################################################" 

	#input_bitmap12=image_to_bitmatrix("/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/software_analytics/perf.timechart.jpeg")
	input_bitmap12=image_to_bitmatrix("/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/software_analytics/perf.flamegraph.jpeg")
	dlc12=DeepLearningConvolution(input_bitmap12)

	#maximum stride is 5
	convolution_stride=2
	conv_map12=dlc12.convolution(convolution_stride)

	#maximum pool sliding window width is 5
	pool_slidewindow_width=2
	pool_map12=dlc12.max_pooling(pool_slidewindow_width)

	print "##########################################"
	print "Set of Convolution Maps"
	print "##########################################"
	print "Example 12:"
	print "###########"
	pprint.pprint(conv_map12)
	print "##########################################"
	print "Max Pooling Map"
	print "##########################################"
	print "Example 12:"
	print "###########"
	pprint.pprint(pool_map12)
	print "####################################################################################################"
	print "Final layer that connects all neurons in max pooling map and does backpropagation"
	print "####################################################################################################"
	maxpool_map_width=5
	print "###########################################################################################"
	print "Inference from Max Pooling Layer" 
	print "###########################################################################################"
	print "Example 12:"
	print "###########"
	print "Software Analytics - Convolution Network + BackPropgation - max pooling inference:",dlc12.infer_from_max_pooling(pool_map12,maxpool_map_width)
	scheduler_class_cnbp=learnt_scheduler_class(dlc12.infer_from_max_pooling(pool_map12,maxpool_map_width))

	for pf in processesfeatures:
		hash1=getHash(str(pf))
		hash2=getHash(str(pf))
		#print "hash1 == hash2:",hash1 == hash2
		if process_md5hash_string == True:
			encodedprocessesfile.write(str(pf[0]["pid"])+":"+str(pf[0]["name"])+":"+getHash(str(pf)))
			encodedprocessesfile.write("\n")
		else:
			#print "process_md5hash_string == False: str(pf[0]) = ",str(pf[0])
			encodedprocessesfile.write(str(pf[0]))
			encodedprocessesfile.write("\n")
