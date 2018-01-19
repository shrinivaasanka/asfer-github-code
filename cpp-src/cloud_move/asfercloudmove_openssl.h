/**********************************************************************************************************
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
**********************************************************************************************************/

#include <iostream>
#include <cstddef>
#include <typeinfo>
#include <utility>
#include <cstring>      // Needed for memset
#include <sys/socket.h> // Needed for the socket functions
#include <sys/types.h>
#include <netdb.h>      // Needed for the socket functions
#include <arpa/inet.h>
#include "protocol_buffers/out_dir/currency.pb.h"
#include "protocol_buffers/out_dir/currency.pb.cc"
#include "opensslclient.h"
#include "opensslserver.h"


using namespace std;

class MessageObject;

/*
Implementation of Move Semantics for Cloud objects:
----------------------------------------------------
This expands on the usual move semantics in C++ and implements a Perfect Forwarding of objects over cloud. A move client invokes the T&& rvalue reference move constructor to move(instead of copying) a local memory content to a remote machine in userspace. Functionality similar to this in kernelspace is required for transactional currency move in KingCobra - http://sourceforge.net/p/kcobra/code-svn/HEAD/tree/KingCobraDesignNotes.txt and https://github.com/shrinivaasanka/kingcobra-github-code/blob/master/KingCobraDesignNotes.txt. Though kernel with C++ code is not advised ,kingcobra driver can make an upcall to userspace move client and server executables and perfom currency move with .proto currency messages.

VIRGO kernel sockets code has been carried over and changed for userspace that uses traditional sockaddr_in and htons.

C++ sockets reference code adapted for std::move - for use_addrinfo clause:
- getaddrinfo linux man pages 
- http://codebase.eu/tutorial/linux-socket-programming-c/ (addrinfo instead of usual sockaddr_in and htons)

Move semantics schematic:
-------------------------
                                    &
 member fn temp arg lvalue <-------source data rvalue
                  |	             /	
              &   |		    / && (removes a temp copy)
                  |		   /
                  V		  /
client proxy destination lvalue<-/ 
		  |
		  |-------------------------> cloud server destination 

lvalue reference& does additional copy which is removed by rvalue reference&& to get the rvalue directly. Move client proxies the remote object and connects to Move server and the object is written over socket.

Currency object has been implemented with Google Protocol Buffers - in protocol_buffers/ src_dir and out_dir directories. Currency has been defined in src_dir/currency.proto file. Choice of Protocol Buffer over other formats is due to:
- lack of JSON format language specific compilers 
- XML is too complicated
- Protocol Buffers also have object serialization-to-text member functions in generated C++ classes.

Protocol Buffer compilation after change to currency object:
protoc -I=src_dir/ --cpp_out=out_dir/ src_dir/currency.proto
 
*/

#define BUF_SIZE 10000

std::string create_neuro_uuid_and_denom(int);

template <class T>
class cloudmove
{
	T curr;
	T* data;
        string remotehostname;
	bool use_addrinfo=false;
public:
	cloudmove(const char* neuro_uuid_denom)
	{
		std::string neuro_uuid_denom_str(neuro_uuid_denom);
	   	curr.set_uuid_and_denom(neuro_uuid_denom);
	   	data=&curr; 
	}

        cloudmove(T* x, string rhn)
        {
           data=x;
           remotehostname=rhn;
        }

        T& get_data()
        {
           return *data;
        } 

        /*
        ~cloudmove()
        {
           delete data;
        }
        */

        //Cloud Move Listener - Move Server
        void receive_moved()
        {
		std::string recds=openssl_server();
                data->set_uuid_and_denom(recds);
	}

	T& operator=(const char* neuro_uuid_denom)
	{
		std::string neuro_uuid_denom_str(neuro_uuid_denom);
	   	T curr; 
	   	curr.set_uuid_and_denom(neuro_uuid_denom);
	   	data=&curr; 
	}

	T& operator=(cloudmove<T>& lvalue)
	{
		cout<<"invoking T& operator=(cloudmove<T>& lvalue)"<<endl;
		data=lvalue.data;
		remotehostname=lvalue.remotehostname;
	}

	//Cloud Move operator= overloaded - Move client	
	T& operator=(cloudmove<T>&& rvalue) 
	{
		openssl_client(rvalue.data->uuid_and_denom().c_str());
		rvalue.data->set_uuid_and_denom("");
        }
};

class MessageObject
{
public:
	string msg;
	MessageObject(string x)
	{
		msg=x;
	}

	~MessageObject()
	{
		cout<<"object is deleted"<<endl;
	}
};

