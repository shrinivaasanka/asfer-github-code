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
invokes NEURONRAIN VIRGO system calls by number - defined in $VIRGO_SRC/linux-kernel-extensions/arch/x86/syscalls/syscalls_64.tbl
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

int memory_versus_filesystem=-1;

void asfer_virgo_set_kernel_analytics(char* key, char* value)
{
	switch(memory_versus_filesystem)
	{

		case -1:
		{
		        long int ret=syscall(548,"virgo_cloud_test_kernelspace");
			break;
		}
		case 0:
		{
			/*
			virgo_malloc(), virgo_set(), virgo_get() and virgo_free() syscalls called by syscall numbers
			- Ka.Shrinivaasan
			*/

			unsigned long long virgo_unique_id;

			/* virgo_malloc */
			/*syscall(384,100,&virgo_unique_id);*/
			syscall(549,1000,&virgo_unique_id);
			printf("vuid malloc-ed : %llu \n",virgo_unique_id);

			/* virgo_set */
			char set_data[256];
			strcpy(set_data,"DataSet");
			printf("virgo_set() data to set: %s\n",set_data);
			/*long set_ret=syscall(385,virgo_unique_id,set_data);*/
			long set_ret=syscall(550,virgo_unique_id,set_data);

			/*virgo_get*/
			char get_data[256];
			/*long get_ret=syscall(386,virgo_unique_id,get_data);*/
			long get_ret=syscall(551,virgo_unique_id,get_data);
			printf("virgo_get() data : %s\n",get_data);

			/*virgo_free*/
			/*long free_ret=syscall(387,virgo_unique_id);*/
			long free_ret=syscall(552,virgo_unique_id);
			break;

		}
		case 1:
		{
			/*
			Testcases for:

			sys_virgo_open(char* filepath);
			sys_virgo_read(long vfsdesc, char __user *data_out, int size, int pos);
			sys_virgo_write(long vfsdesc, const char __user *data_in, int size, int pos);
			sys_virgo_close(long vfsdesc);

			invoked by syscall numbers in arch/x86/syscalls/syscalls_64.tbl
			*/

			/* long vfsdesc = syscall(364,"/var/log/virgo_fs/virgofstest.txt"); */ /* open */
			long vfsdesc = syscall(553,"/var/log/virgo_fs/virgofstest.txt"); /* open */
			printf("test_virgo_filesystem.c: vfsdesc = %ld\n",vfsdesc);
			char data_read[256];
		
			/* syscall(366,vfsdesc,data_read,250,0); */ /* read */
			syscall(555,vfsdesc,data_read,250,0);  /* read */
			printf("test_virgo_filesystem.c: data_read = %s\n",data_read);

			/* syscall(367,vfsdesc,"test_virgo_filesystem_29September2015",250,0); */ /* write */
			syscall(556,vfsdesc,"test_virgo_filesystem_26April2017",250,0); /* write */

			/* syscall(365,vfsdesc);  */ /* close */
			syscall(554,vfsdesc);  /* close */

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
