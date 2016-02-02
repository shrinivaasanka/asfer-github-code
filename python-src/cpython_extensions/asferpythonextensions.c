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
#--------------------------------------------------------------------------------------------------------
#Copyleft(Copyright+):
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Ph: 9791499106, 9003082186
#Krishna iResearch Open Source Products Profiles:
#http://sourceforge.net/users/ka_shrinivaasan,
#https://github.com/shrinivaasanka,
#https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com,
#kashrinivaasan@live.com
#--------------------------------------------------------------------------------------------------------
*/

#include <Python.h>
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

static PyObject* asfer_virgo_set_kernel_analytics(PyObject* self, PyObject* args)
{
	/* VIRGO malloc system calls to set the key-value pairs */
	
	char keyvalue[80];
	if (!PyArg_ParseTuple(args, "s", keyvalue))
		return NULL;
	
	printf("asfer_virgo_set_kernel_analytics(): %s \n",keyvalue);
	
	struct virgo_address* vaddr;
	unsigned long virgo_unique_id=3250409088u;

	/* virgo_malloc */
	syscall(360,100,&virgo_unique_id);

	/* virgo_set */
	printf("asfer_virgo_set_kernel_analytics(): keyvalue: %s\n",keyvalue);
	long set_ret=syscall(361,virgo_unique_id,keyvalue);
	/*
	long set_ret=syscall(361,virgo_unique_id,"key1:value1");
	*/

	/* virgo_get */
	char get_data[256];
	long get_ret=syscall(362,virgo_unique_id,get_data);

	/* virgo_free */
	/*
	long free_ret=syscall(363,virgo_unique_id); 
	*/
        return Py_BuildValue("l",virgo_unique_id);
}

static char py_add_doc[]="asfer_virgo_set_kernel_analytics";

static PyMethodDef AsFer_VIRGO_Methods[] =
{
	{"asfer_virgo_set_kernel_analytics", asfer_virgo_set_kernel_analytics, METH_VARARGS, py_add_doc},
	{NULL, NULL, 0, NULL}
};

/*PyMODINIT_FUNC*/
void 
initasfer_virgo_pyext(void)
{
	PyObject* mod;
	mod=Py_InitModule("asfer_virgo_pyext", AsFer_VIRGO_Methods);
}
