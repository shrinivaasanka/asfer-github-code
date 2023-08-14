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
#Personal website(research): http://www.krishna-iresearch.org/ , 
#--------------------------------------------------------------------------------------------------------

def parse_syscall_trace_log(tracefile):
    tracefd=open(tracefile)
    freqreadfs=[]
    for line in tracefd.readlines():
        if "read(" in line:
            linetoks=line.split(" ")
            print(linetoks)
            readfd=linetoks[3][:-1].split("(")
            freqreadfs.append(readfd[1])
    kernelanalytics=open("/etc/virgo_kernel_analytics.conf","a")
    kernelanalytics.write(",frequently_read_filedescriptors="+str(set(freqreadfs)))

if __name__=="__main__":
    parse_syscall_trace_log("./asfer_syscall_trace.log")


