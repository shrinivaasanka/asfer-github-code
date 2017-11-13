PYLIB=/usr/lib/python2.7/config-i386-linux-gnu/libpython2.7.a
PYINC=-I-I/usr/include -I/usr/include -I/usr/include/python2.7 -I/usr/include/python2.7
LIBS=-L/usr/lib -L/usr/lib -lz -lpthread -ldl  -lutil -lm
OPTS=-DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes

all:
	#g++ -g -std=c++0x *.cpp -o asfer
	#g++ -g -w -std=c++14 *.cpp -o asfer
	g++ -g -w -std=c++14 -I/usr/include/python2.7 -L/usr/lib/i386-linux-gnu *.cpp -lpython2.7 -o asfer
clean:
	rm asfer

