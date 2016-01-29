#Sophisticated build commandline:
g++ -I/usr/include/python2.7 -I/usr/include/i386-linux-gnu/python2.7  -fno-strict-aliasing -D_FORTIFY_SOURCE=2 -g -fstack-protector-strong -Wformat -Werror=format-security  -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -L/usr/lib/python2.7/config-i386-linux-gnu -L/usr/lib -lpython2.7 -lpthread -ldl  -lutil -lm  -Xlinker -export-dynamic -Wl,-O1 -Wl,-Bsymbolic-functions asferpythonembedding.cpp -o asferpythonembedding

#Simpler build commandline:
g++ -I/usr/include/python2.7 -L/usr/lib/i386-linux-gnu asferpythonembedding.cpp -lpython2.7 -o asferpythonembedding
