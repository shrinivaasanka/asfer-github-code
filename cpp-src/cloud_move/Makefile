all:
	g++ -DOPENSSL -g -w -std=c++14 asfercloudmoveclient.cpp -o asfercloudmoveclient -lprotobuf -lpthread -lssl -lcrypto
	g++ -DOPENSSL -g -w -std=c++14 asfercloudmoveserver.cpp -o asfercloudmoveserver -lprotobuf -lpthread -lssl -lcrypto
clean:
	rm asfercloudmoveclient asfercloudmoveserver

