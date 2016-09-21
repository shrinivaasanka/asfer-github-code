all:
	g++ -g -w -std=c++14 -I/home/shrinivaasanka/zeromq-4.1.5/include/ -L/usr/lib/i386-linux-gnu -L/home/shrinivaasanka/zeromq-4.1.5/.libs/  zeromq_client.c -o zeromq_client -lzmq -lpthread
	g++ -g -w -std=c++14 -I/home/shrinivaasanka/zeromq-4.1.5/include/ -L/usr/lib/i386-linux-gnu -L/home/shrinivaasanka/zeromq-4.1.5/.libs/  zeromq_server.c -o zeromq_server -lzmq -lpthread
clean:
	rm zeromq_client zeromq_server 

