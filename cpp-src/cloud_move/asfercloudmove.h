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

template <class T>
class cloudmove
{
	T* data;
        string remotehostname;
	bool use_addrinfo=false;
public:
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
	     if(use_addrinfo)
             {
             	int status;
             	struct addrinfo host_info;       // The struct that getaddrinfo() fills up with data.
             	struct addrinfo *host_info_list; // Pointer to the to the linked list of host_info's.

             	memset(&host_info, 0, sizeof host_info);

             	std::cout << "Setting up the structs..."  << std::endl;

             	host_info.ai_family = AF_UNSPEC;     // IP version not specified. Can be both.
             	host_info.ai_socktype = SOCK_STREAM; // Use SOCK_STREAM for TCP or SOCK_DGRAM for UDP.
             	host_info.ai_flags = AI_PASSIVE;     // IP Wildcard

             	status = getaddrinfo(NULL, "55555", &host_info, &host_info_list);
             	if (status != 0)  std::cout << "getaddrinfo error" << gai_strerror(status) ;

             	std::cout << "Creating a socket..."  << std::endl;
             	int socketfd ; // The socket descripter
             	socketfd = socket(host_info_list->ai_family, host_info_list->ai_socktype,
                                                       host_info_list->ai_protocol);
             	if (socketfd == -1)  std::cout << "socket error " ;

             	std::cout << "Binding socket..."  << std::endl;
             	// we use to make the setsockopt() function to make sure the port is not in use
             	// by a previous execution of our code. (see man page for more information)
             	int yes = 1;
             	status = setsockopt(socketfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int));
             	status = bind(socketfd, host_info_list->ai_addr, host_info_list->ai_addrlen);
             	if (status == -1)  std::cout << "bind error" << std::endl ;

             	std::cout << "Listen()ing for connections..."  << std::endl;
             	status =  listen(socketfd, 5);
             	if (status == -1)  std::cout << "listen error" << std::endl ;

             	int new_sd;
             	struct sockaddr_storage their_addr;
             	socklen_t addr_size = sizeof(their_addr);
             	new_sd = accept(socketfd, (struct sockaddr *)&their_addr, &addr_size);
             	if (new_sd == -1)
             	{
               	  std::cout << "listen error" << std::endl ;
             	}
             	else
             	{
               	  std::cout << "Connection accepted. Using new socketfd : "  <<  new_sd << std::endl;
             	}
             	ssize_t recd;
             	char buffer[1000];
             	recd = recv(new_sd, buffer,1000, 0);
             	// If no data arrives, the program will just wait here until some data arrives.
             	if (recd == -1) 
			std::cout << "errno set:" << errno << std::endl ;
             	std::cout << recd << " bytes recieved :" << std::endl ;
             	buffer[recd] = '\0' ;
             	std::cout << buffer << std::endl;
             	std::cout << "Receiving complete. Closing socket..." << std::endl;
             	freeaddrinfo(host_info_list);
             	string recds(buffer);
             	data->set_uuid_and_denom(recds); 
             	shutdown(new_sd,SHUT_RDWR);
	     } 
             else
             {
		//VIRGO kernel sockets code modified
	     	int len, error;
	     	struct msghdr msg;
             	struct iovec iov;
             	char buffer[BUF_SIZE];
             	int sock, clientsock;
	     	struct sockaddr_in sin;
 	     	memset(&sin, 0, sizeof(struct sockaddr_in));
             	sin.sin_family=AF_INET;
             	sin.sin_addr.s_addr=htonl(INADDR_ANY);
             	sin.sin_port=htons(55555);

             	sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
             	clientsock=NULL;
             	error = bind(sock, (struct sockaddr*)&sin, sizeof(struct sockaddr_in));
             	error = listen(sock, 2);
	     	socklen_t addr_sz=sizeof(sin);
             	clientsock = accept(sock, (struct sockaddr *)&sin, &addr_sz);

             	memset(buffer, 0, BUF_SIZE);
             	iov.iov_base=(void*)buffer;
             	iov.iov_len=BUF_SIZE;
             	msg.msg_name = (struct sockaddr *) &sin;
             	msg.msg_namelen = sizeof(struct sockaddr);
             	msg.msg_iov = (struct iovec *) &iov;
             	msg.msg_iovlen = 1;
             	msg.msg_control = NULL;
             	msg.msg_controllen = 0;
             	msg.msg_flags=MSG_NOSIGNAL;

             	len  = recvmsg(clientsock, &msg, msg.msg_flags);
		string recds(buffer);
             	data->set_uuid_and_denom(recds); 
             }
	}

	//Cloud Move operator= overloaded - Move client	
	T& operator=(cloudmove<T>&& rvalue) 
	{
	        if(use_addrinfo)
                {	
                	int status;
                	struct addrinfo host_info;       // The struct that getaddrinfo() fills up with data.
                	struct addrinfo *host_info_list; // Pointer to the to the linked list of host_info's.

             		 // The MAN page of getaddrinfo() states "All  the other fields in the structure pointed
               		 // to by hints must contain either 0 or a null pointer, as appropriate." When a struct
               		 // is created in c++, it will be given a block of memory. This memory is not nessesary
               		 // empty. Therefor we use the memset function to make sure all fields are NULL.
                	memset(&host_info, 0, sizeof host_info);

                	std::cout << "Setting up the structs..."  << std::endl;

                	host_info.ai_family = AF_UNSPEC;     // IP version not specified. Can be both.
                	host_info.ai_socktype = SOCK_STREAM; // Use SOCK_STREAM for TCP or SOCK_DGRAM for UDP.

                	// Now fill up the linked list of host_info structs with google's address information.
                	status = getaddrinfo("localhost", "55555", &host_info, &host_info_list);
                	// getaddrinfo returns 0 on succes, or some other value when an error occured.
                	// (translated into human readable text by the gai_gai_strerror function).
                	if (status != 0)  std::cout << "getaddrinfo error" << gai_strerror(status) ;


                	std::cout << "Creating a socket..."  << std::endl;
                	int socketfd ; // The socket descripter
                	socketfd = socket(host_info_list->ai_family, host_info_list->ai_socktype,
                   	   	host_info_list->ai_protocol);
                	if (socketfd == -1)  std::cout << "socket error " ;

                	std::cout << "Connect()ing..."  << std::endl;
                	status = connect(socketfd, host_info_list->ai_addr, host_info_list->ai_addrlen);
                	if (status == -1)  
                      		std::cout << "connect error" ;

                	std::cout << "Object move - send()ing message object...:"  << rvalue.data->uuid_and_denom() <<std::endl;
                	int len;
                	ssize_t bytes_sent;
                	len = strlen(rvalue.data->uuid_and_denom().c_str());
                	bytes_sent = send(socketfd, rvalue.data->uuid_and_denom().c_str(), len, 0);
                	//rvalue.data->msg="";
			rvalue.data->set_uuid_and_denom("");
	        }
		else
		{	
			//VIRGO kernel sockets code modified
			char buf[BUF_SIZE];
   	        	char tempbuf[BUF_SIZE];
        		int sfd, s, j;
        		size_t len;
        		ssize_t nread;
			struct msghdr msg;
			int error;
			int nr;
			struct iovec iov;
			char* hostip = (char*) remotehostname.c_str();
			int port=55555;
			int sock;
			struct sockaddr_in sin;
			inet_pton(AF_INET, hostip, &sin.sin_addr.s_addr);
			sin.sin_family=AF_INET;
       			sin.sin_port=htons(port);
			strcpy(buf,rvalue.data->uuid_and_denom().c_str());

			iov.iov_base=buf;
			iov.iov_len=strlen(buf);
			msg.msg_name = (struct sockaddr *) &sin;
			msg.msg_namelen = sizeof(struct sockaddr);
			msg.msg_iov = (struct iovec *) &iov;
			msg.msg_iovlen = 1;
			msg.msg_control = NULL;
			msg.msg_controllen = 0;
			msg.msg_flags = 0;
			nr=1;
	
			sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
			connect(sock, (struct sockaddr*)&sin, sizeof(sin));
			len = sendmsg(sock, &msg, msg.msg_flags);
                	//rvalue.data->msg="";
			rvalue.data->set_uuid_and_denom("");
		}
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
