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

int main()
{
        std::cout<< "Cloud Move - Listener Server" <<endl;
        //MessageObject msg1("MessageDest");
        //cloudmove<MessageObject> cm_dest(&msg1, "localhost");
        currency::Currency currency_dest;
	cloudmove<currency::Currency> cm_dest(&currency_dest, "localhost");	
	cout<<"before receive_moved()"<<endl;
        cm_dest.receive_moved();
	cout<<"after receive_moved()"<<endl;
        std::cout<< " cloud destination - received cloud-moved object :" <<cm_dest.get_data().uuid_and_denom() <<endl;
}
