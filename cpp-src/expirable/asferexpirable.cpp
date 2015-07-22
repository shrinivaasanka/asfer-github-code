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
Ph: 9789346927, 9003082186, 9791165980
Krishna iResearch Open Source Products Profiles:
http://sourceforge.net/users/ka_shrinivaasan, https://www.openhub.net/accounts/ka_shrinivaasan
Personal website(research): https://sites.google.com/site/kuja27/
ZODIAC DATASOFT: https://github.com/shrinivaasanka/ZodiacDatasoft
emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
---------------------------------------------------------------------------------------------------------
*********************************************************************************************************/

#include "asferexpirable.h"

int main()
{
	IntObject *data1 = new IntObject(10);
	IntObject *data2 = new IntObject(20);
	IntObject *data3 = new IntObject(30);
	expirable<IntObject> x1(data1);
	expirable<IntObject> x2(data2);

	expirable<IntObject> *x3 = new expirable<IntObject> (data3);
	expirable<IntObject>& x4 = *x3; // for some reason this implicit dereference doesnot invoke operator*() 
	x3->operator*(); // this invokes operator*() directly  
	x3->operator*(); // this invokes operator*() directly  
	x3->operator*(); // this invokes operator*() directly  
	x3->operator*(); // this invokes operator*() directly  
	x3->operator*(); // this invokes operator*() directly  
	x3->operator*(); // this invokes operator*() directly , should expire

	x2=x1;
	x2=x1;
	x2=std::move(x1);
	x2=std::move(x1);
	x2=std::move(x1);
	x2=std::move(x1); // should expire
	x2=x1;  // should expire
	x2=std::move(x1); // should expire
	x2=x1;  // should expire
}
