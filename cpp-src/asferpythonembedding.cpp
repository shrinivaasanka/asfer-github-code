/*********************************************************************************************************
---------------------------------------------------------------------------------------------------------
ASFER - Inference Software for Large Datasets - component of iCloud Platform
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

---------------------------------------------------------------------------------------------------------
Copyright (C):
Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
Ph: 9791499106, 9003082186
Krishna iResearch Open Source Products Profiles:
http://sourceforge.net/users/ka_shrinivaasan
https://github.com/shrinivaasanka/
https://www.openhub.net/accounts/ka_shrinivaasan
Personal website(research): https://sites.google.com/site/kuja27/
emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
---------------------------------------------------------------------------------------------------------
*********************************************************************************************************/

/*
Prerequisites: 
- python-dbg and python-dev packages
- rename libpython2.7_d.so to libpython2.7 as some symbols are not found in libpython2.7.so during g++ ld. 
- asferpythonembedding.sh has two commandlines (simpler and detailed based on python-config cflags and ldflags) for building this. Also a makefile generated and modified based on python script in https://www6.software.ibm.com/developerworks/education/l-pythonscript/l-pythonscript-ltr.pdf has been added. 

Following main() can be uncommented and executed as independent binary with above makefile commandlines.

root@shrinivaasanka-Inspiron-1545:/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/KrishnaiResearch_OpenSource/GitHub/asfer-github-code/cpp-src# python2.7-config --cflags
-I/usr/include/python2.7 -I/usr/include/i386-linux-gnu/python2.7  -fno-strict-aliasing -D_FORTIFY_SOURCE=2 -g -fstack-protector-strong -Wformat -Werror=format-security  -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes

root@shrinivaasanka-Inspiron-1545:/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/KrishnaiResearch_OpenSource/GitHub/asfer-github-code/cpp-src# python2.7-config --ldflags
-L/usr/lib/python2.7/config-i386-linux-gnu -L/usr/lib -lpython2.7 -lpthread -ldl  -lutil -lm  -Xlinker -export-dynamic -Wl,-O1 -Wl,-Bsymbolic-functions
*/

#include <Python.h>
#include <stdio.h>

class asferpythonembedding
{
	public:
		void execute_python_script(char *python_file)
		{
		  Py_Initialize();
		  FILE* fp=fopen(python_file, "r");
		  PyRun_SimpleFile(fp, python_file);
		  Py_Finalize();
		}
};

/*
int main(int argc, char* argv[])
{
  Py_Initialize();
  FILE* fp=fopen(python_file, "r");
  PyRun_SimpleFile(fp, python_file);
  Py_Finalize();
}
*/
