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
#--------------------------------------------------------------------------------------------------------
*/

#include <zmq.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>

int main (int argc,char* argv[])
{
    void *context = zmq_ctx_new ();
    void *clientsocket = zmq_socket (context, ZMQ_REQ);
    zmq_connect (clientsocket, "tcp://localhost:5555");

    printf("NEURONRAIN CLI Client\n");
    char reply[500];
    zmq_send (clientsocket, argv[1], strlen(argv[1]), 0);
    zmq_recv (clientsocket, reply, 500, 0);
    
    zmq_close (clientsocket);
    zmq_ctx_destroy (context);
    return 0;
}
