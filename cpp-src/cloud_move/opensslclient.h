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
Reference: OpenSSL client example - https://wiki.openssl.org/index.php/SSL/TLS_Client
*/

#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <openssl/x509.h>
#include <iostream>

#define HOST_NAME "localhost"
#define HOST_PORT "443"

using namespace std;

void printError(int errcode)
{
	cout<<"Error:"<<errcode<<endl;
}

void verify_callback()
{
	cout<<"verify_callback() invoked"<<endl;
}

void init_openssl_library()
{
	(void)SSL_library_init();
	SSL_load_error_strings();
	/* ERR_load_crypto_strings(); */
	/* OPENSSL_config(NULL); */
}

int openssl_client(const char* rvaluestr)
{
	long res = 1;
	SSL_CTX* ctx = NULL;
	BIO *web = NULL, *out = NULL;
	SSL *ssl = NULL;
	init_openssl_library();
	const SSL_METHOD* method = SSLv23_method();
	if(!(NULL != method)) printError(1);
	ctx = SSL_CTX_new(method);
	if(!(ctx != NULL)) printError(2);
	/* Cannot fail ??? */
	//SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER, verify_callback);
	/* Cannot fail ??? */
	SSL_CTX_set_verify_depth(ctx, 4);
	/* Cannot fail ??? */
	const long flags = SSL_OP_NO_SSLv2 | SSL_OP_NO_SSLv3 | SSL_OP_NO_COMPRESSION;
	SSL_CTX_set_options(ctx, flags);
	res = SSL_CTX_load_verify_locations(ctx, "cert.pem", NULL);
	if(!(1 == res)) printError(3);
	web = BIO_new_ssl_connect(ctx);
	if(!(web != NULL)) printError(4);
	res = BIO_set_conn_hostname(web, HOST_NAME ":" HOST_PORT);
	if(!(1 == res)) printError(5);
	BIO_get_ssl(web, &ssl);
	if(!(ssl != NULL)) printError(6);
	const char* const PREFERRED_CIPHERS = "HIGH:!aNULL:!kRSA:!PSK:!SRP:!MD5:!RC4";
	res = SSL_set_cipher_list(ssl, PREFERRED_CIPHERS);
	if(!(1 == res)) printError(7);
	res = SSL_set_tlsext_host_name(ssl, HOST_NAME);
	if(!(1 == res)) printError(8);
	out = BIO_new_fp(stdout, BIO_NOCLOSE);
	if(!(NULL != out)) printError(9);
	res = BIO_do_connect(web);
	if(!(1 == res)) printError(10);
	res = BIO_do_handshake(web);
	if(!(1 == res)) printError(11);
	/* Step 1: verify a server certificate was presented during the negotiation */
	X509* cert = SSL_get_peer_certificate(ssl);
	if(cert) { X509_free(cert); } /* Free immediately */
	if(NULL == cert) printError(12);
	/* Step 2: verify the result of chain verification */
	/* Verification performed according to RFC 4158
	*/
	res = SSL_get_verify_result(ssl);
	if(!(X509_V_OK == res)) printError(13);
	/* Step 3: hostname verification */
	/* An exercise left to the reader */
	//BIO_puts(web, rvaluestr);
	int len = 0;
	//do
	//{
	if(1)
	{
		char buff[1024];
		strcpy(buff,rvaluestr);
		//len = BIO_read(web, buff, sizeof(buff));
		//if(len > 0)
		//BIO_write(out, buff, len);
		cout<<"before BIO_write(): buff = "<<buff<<" ;rvaluestr = "<<rvaluestr<<endl;
		BIO_write(web, buff, 1024);
	}
	//} while (len > 0 || BIO_should_retry(web));
	if(out)
		BIO_free(out);
	if(web != NULL)
		BIO_free_all(web);
	if(NULL != ctx)
		SSL_CTX_free(ctx);

	/******************************************************************************
        struct sockaddr_in addr;
        uint len = sizeof(addr);
        SSL *ssl;
        ssl = SSL_new(ctx);
        SSL_set_fd(ssl, client);
        SSL_read(ssl, request, strlen(request));
        cout<<"openssl_server(): request = "<<request<<endl;
        SSL_write(ssl, reply, strlen(reply));
        SSL_free(ssl);
        close(client);
	******************************************************************************/
}

