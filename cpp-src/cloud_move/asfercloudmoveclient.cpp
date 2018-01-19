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

#ifdef OPENSSL
#include "asfercloudmove_openssl.h"
#else
#include "asfercloudmove.h"
#endif

#include <boost/uuid/uuid.hpp>
#include <boost/uuid/uuid_generators.hpp>
#include <boost/uuid/uuid_io.hpp>
#include <boost/lexical_cast.hpp>
#include <string>
#include <iostream>
#include <utility>

using namespace boost::uuids;

int main()
{
        //std::cout<< " Cloud Move - Client"<<endl;
	//MessageObject msg1("MessageSource1");
	//MessageObject msg2("None");
	//cloudmove<MessageObject> cm_source(&msg1, "localhost");
        //cloudmove<MessageObject> cm_dest(&msg2, "localhost");
	//std::cout<<" source before std::move "<<cm_source.get_data().msg<<endl;
        //cm_dest = std::move(cm_source);
	//std::cout<<" source after std::move "<<cm_source.get_data().msg<<endl;
	//std::cout<<" proxy remote destination "<<cm_dest.get_data().msg<<endl;

	//Protocol Buffer Currency Object
	//std::string move_semantics="std::move";
	//std::string move_semantics="std::forward";
	std::string move_semantics="nonprimitiveforward";
	currency::Currency c1;
	currency::Currency c2;
	std::string uuid_and_denom=create_neuro_uuid_and_denom(100);
	c1.set_uuid_and_denom(uuid_and_denom);
	cloudmove<currency::Currency> currency_src(&c1,"localhost");
	cloudmove<currency::Currency> currency_dest(&c2,"localhost");
	std::string&& uuid_and_denom2="ff20a894-a2c4-4002-ac39-93d053ea3020:100";
	if(move_semantics=="std::move")
	{
		std::cout<<"currency_src before std::move =  "<<currency_src.get_data().uuid_and_denom()<<endl;
		currency_dest = std::move(currency_src);
		std::cout<<"currency_src after std::move ="<<currency_src.get_data().uuid_and_denom()<<endl;
	}
	else if(move_semantics=="std::forward")
	{
		std::cout<<"std::forward()-ed rvalue of uuid_and_denom2: "<<std::forward<std::string>(uuid_and_denom2)<<endl;
		currency::Currency c3;
		c3.set_uuid_and_denom(std::forward<std::string>(uuid_and_denom2));
		cloudmove<currency::Currency> currency_src2(&c3,"localhost");
		std::cout<<"currency_src2 before std::move =  "<<currency_src2.get_data().uuid_and_denom()<<endl;
		currency_dest=std::move(currency_src2);
		std::cout<<"currency_src2 after std::move =  "<<currency_src2.get_data().uuid_and_denom()<<endl;
	}
	else
	{
		cloudmove<currency::Currency>&& currency_src2="ff20a894-a2c4-4002-ac39-93d053ea3020:100";
		std::cout<<"nonprimitiveforward: currency_src2 before std::forward =  "<<currency_src2.get_data().uuid_and_denom()<<endl;
		cloudmove<currency::Currency>&& currency_src3=std::forward<cloudmove<currency::Currency>>(currency_src2);
		std::cout<<"nonprimitiveforward: before std::move:"<<currency_src3.get_data().uuid_and_denom()<<endl;
		currency_dest=std::move(currency_src3);
		//currency_dest=std::move(std::forward<cloudmove<currency::Currency>>(currency_src2));
		std::cout<<"nonprimitiveforward: currency_src2 after std::move =  "<<currency_src3.get_data().uuid_and_denom()<<endl;
	}
	std::cout<<"currency_dest proxy remote destination ="<<currency_dest.get_data().uuid_and_denom()<<endl;
}

std::string create_neuro_uuid_and_denom(int denomination)
{
	//Fictitious Message-As-Currency in AsFer-KingCobra has been named "Neuro".
	//Does a non-trivial proof-of-work computation and finds a universally unique hash id for each Neuro MAC which has 2 leading "ff"s
	//from Boost UUID
	random_generator gen;
	uuid id=gen();
	std::string sid=to_string(id);
	cout<<"sid = "<<sid<<endl;
	while(sid.substr(0,2) != "ff")
	{
		id=gen();
		sid=to_string(id);
		cout<<"sid = "<<sid<<endl;
	}
	std::string denom_str=std::to_string(denomination);
	sid.append(":");
	return sid.append(denom_str);
}
