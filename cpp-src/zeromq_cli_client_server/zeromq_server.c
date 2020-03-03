/*
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
#---------------------------------------------------------------------------------------------------------
*/


#include <zmq.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <pthread.h>

int number_of_workers=50;

static void* worker_func(void* context)
{
   void *workersocket = zmq_socket(context, ZMQ_REP);

   zmq_connect(workersocket, "inproc://workers");


   while (1) 
   {
        char buffer[500];
	zmq_recv (workersocket,buffer,500,0);
        printf ("Received Request %s\n",buffer);
	system(buffer);
        zmq_send (workersocket,"Request Forwarded to NeuronRain",100,0);
   }
}


int main (void)
{
    void *context = zmq_ctx_new ();
    void *clientsockets = zmq_socket (context, ZMQ_ROUTER);
    int ret1 = zmq_bind (clientsockets, "tcp://*:5555");

    void *workersockets = zmq_socket(context, ZMQ_DEALER);
    int ret2 = zmq_bind(workersockets, "inproc://workers");

    for (int i=0; i < number_of_workers; i++)
    {
	pthread_t worker_thread;
   	printf("NEURONRAIN - CLI ZeroMQ Concurrent Request Router-Dealer Server - Spawning Worker Thread: %d\n",i);
	pthread_create(&worker_thread,NULL,worker_func,context);
    }
    zmq_proxy(clientsockets,workersockets,NULL);
    
    return 0;
}

