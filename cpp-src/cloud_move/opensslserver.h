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

/*
Reference: OpenSSL Server Example - https://wiki.openssl.org/index.php/Simple_TLS_Server
*/

#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <openssl/ssl.h>
#include <openssl/err.h>

int create_socket(int port)
{
	int s;
	struct sockaddr_in addr;
	addr.sin_family = AF_INET;
	addr.sin_port = htons(port);
	addr.sin_addr.s_addr = htonl(INADDR_ANY);
	s = socket(AF_INET, SOCK_STREAM, 0);
	if (s < 0) {
		perror("Unable to create socket");
		exit(EXIT_FAILURE);
	}
	if (bind(s, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
		perror("Unable to bind");
		exit(EXIT_FAILURE);
	}
	if (listen(s, 1) < 0) {
		perror("Unable to listen");
		exit(EXIT_FAILURE);
	}
	return s;
}

void init_openssl()
{
	SSL_load_error_strings();
	OpenSSL_add_ssl_algorithms();
}

void cleanup_openssl()
{
	EVP_cleanup();
}

SSL_CTX *create_context()
{
	const SSL_METHOD *method;
	SSL_CTX *ctx;
	method = SSLv23_server_method();
	ctx = SSL_CTX_new(method);
	if (!ctx) {
		perror("Unable to create SSL context");
		ERR_print_errors_fp(stderr);
		exit(EXIT_FAILURE);
	}
	return ctx;
}

void configure_context(SSL_CTX *ctx)
{
	SSL_CTX_set_ecdh_auto(ctx, 1);
	/* Set the key and cert */
	if (SSL_CTX_use_certificate_file(ctx, "cert.pem", SSL_FILETYPE_PEM) <= 0) {
		ERR_print_errors_fp(stderr);
		exit(EXIT_FAILURE);
	}
	if (SSL_CTX_use_PrivateKey_file(ctx, "key.pem", SSL_FILETYPE_PEM) <= 0 ) {
		ERR_print_errors_fp(stderr);
		exit(EXIT_FAILURE);
	}
}

std::string openssl_server()
{
	int sock;
	char request[1024];
	SSL_CTX *ctx;
	init_openssl();
	ctx = create_context();
	configure_context(ctx);
	sock = create_socket(443);
	/* Handle connections */
	if(1) {
		struct sockaddr_in addr;
		uint len = sizeof(addr);
		SSL *ssl;
		int client = accept(sock, (struct sockaddr*)&addr, &len);
		if (client < 0) {
			perror("Unable to accept");
			exit(EXIT_FAILURE);
		}
		ssl = SSL_new(ctx);
		SSL_set_fd(ssl, client);
		if (SSL_accept(ssl) <= 0) {
			ERR_print_errors_fp(stderr);
		}
		else {
			SSL_read(ssl, request, 1024);
			cout<<"openssl_server(): request = "<<request<<endl;
		}
		SSL_free(ssl);
		close(client);
	}
	close(sock);
	SSL_CTX_free(ctx);
	cleanup_openssl();
	std::string requeststring(request);
	cout<<"requeststring="<<requeststring<<endl;
	return requeststring;
}
