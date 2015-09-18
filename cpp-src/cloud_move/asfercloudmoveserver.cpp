/*********************************************************************************************************
---------------------------------------------------------------------------------------------------------
ASFER - Inference Software for Large Datasets - component of iCloud Platform
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

---------------------------------------------------------------------------------------------------------
Copyright (C):
Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
Ph: 9791499106, 9003082186
Krishna iResearch Open Source Products Profiles:
http://sourceforge.net/users/ka_shrinivaasan
https://github.com/shrinivaasanka/
https://www.openhub.net/accounts/ka_shrinivaasan
Personal website(research): https://sites.google.com/site/kuja27/
emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
---------------------------------------------------------------------------------------------------------
*********************************************************************************************************/

#include "asfercloudmove.h"

int main()
{
        std::cout<< "Cloud Move - Listener Server" <<endl;
        //MessageObject msg1("MessageDest");
        //cloudmove<MessageObject> cm_dest(&msg1, "localhost");
        currency::Currency currency_dest;
	cloudmove<currency::Currency> cm_dest(&currency_dest, "localhost");	
        cm_dest.receive_moved();
        std::cout<< " cloud destination - received cloud-moved object :" <<cm_dest.get_data().uuid_and_denom() <<endl;
}
