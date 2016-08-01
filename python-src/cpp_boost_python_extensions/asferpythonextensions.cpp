/*
-------------------------------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------------------------------
#Copyleft(Copyright+):
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
#-----------------------------------------------------------------------------------------------------------
*/

/*
invokes NEURONRAIN VIRGO system calls by number - defined in $VIRGO_SRC/linux-kernel-extensions/arch/x86/syscalls/syscalls_32.tbl
*/

#include <iostream>

#include <stdio.h>
#include <syscall.h>
#include <unistd.h>
#include <string.h>

struct virgo_address
{
        int node_id;
        struct hostport* hstprt;
        void* addr;
};

struct hostport
{
        char* hostip;
        int port;
};

using namespace std;

int memory_versus_filesystem=0;

void asfer_virgo_set_kernel_analytics(char* key, char* value)
{
	switch(memory_versus_filesystem)
	{
		case -1:
		{
		        syscall(359,"virgo_cloud_test_kernelspace ");
			break;
		}
		case 0:
		{
			//cout<<"asfer_virgo_set_kernel_analytics():"<<"key:"<<key<<"; value:"<<value<<endl;

			// VIRGO malloc system calls to set the key-value pairs
	
			struct virgo_address* vaddr;
			unsigned long virgo_unique_id=3250409088u;

			// virgo_malloc
			syscall(360,100,&virgo_unique_id);
			//printf("vuid malloc-ed : %lu \n",virgo_unique_id);

			// virgo_set
			char set_data[256];
			strcpy(set_data,key);
			strcpy(set_data,":");
			strcpy(set_data,value);
			//printf("vuid virgo_set() \n");
			long set_ret=syscall(361,virgo_unique_id,"key1:value1");
			//long set_ret=syscall(361,virgo_unique_id,set_data);

			// virgo_get
			char get_data[256];
			long get_ret=syscall(362,virgo_unique_id,get_data);
			//printf("vuid virgo_get() : %s \n",get_data);

			// virgo_free
			// long free_ret=syscall(363,virgo_unique_id);
			break;
		}
		case 1:
		{
			// virgo_open
			long open_ret=syscall(364, "/home/shrinivaasanka/virgocloudfs.txt");

			// virgo_read
			syscall(366, open_ret, "text", 250, 0);

			// virgo_write
			syscall(367, open_ret, "AppendedText_30May2016", 250, 0);
		}
	}
}

#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
using namespace boost::python;

BOOST_PYTHON_MODULE(asfer_virgo_pyext)
{
	def("asfer_virgo_set_kernel_analytics",asfer_virgo_set_kernel_analytics);
}
