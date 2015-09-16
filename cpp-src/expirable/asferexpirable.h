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

#include <iostream>
#include <cstddef>
#include <typeinfo>
#include <utility>

using namespace std;

class IntObject;

/*
Expirable template class implementation 
---------------------------------------
Similar to weak_ptr and shared_ptr, this is a generic datatype that wraps any datatype
and sets an expiry count to it. For example, a bitmap or a JPEG image can be wrapped in
expirable container and it can be access-controlled. If expiry count is 1, the object (an 
image for example) can be written to or displayed only once and thus a singleton.  Presently
this is only for rvalues. Implementing for lvalues (just a usage without assignment should
be able expire an object) seems to be a hurdle as there is no operator overloading available
for lvalues.
*/


template <class T>
class expirable
{
	T* data;
	int expiry_count=6;
	int assign_refcount=1;
	int access_refcount=1;
	int copy_assignment=1;
	int move_assignment=1;
public:
	expirable(T* x)
	{
		data=x;
	}

	/*
		Overloaded dereferencing operator
	*/
	T& operator* () // const
	{
		cout<<"access_refcount: dereference operator invoked"<<endl;
		if(access_refcount < expiry_count)
		{
			access_refcount++;
			cout<<"access_refcount < expiry_count : dereference operator invoked"<<endl;
		}
		else
		{
			cout<<"access_refcount > expiry_count : this object expires, cannot be accessed anylonger"<<endl;
		}
		return *data;
	}

	/*
		Overloaded Copy Assignment operator
	*/

	T& operator=(expirable<T>& lvalue)
	{
		if(copy_assignment)
		{
			if(assign_refcount < expiry_count)
			{
				cout<<"copy_assignment: assignment operator invoked"<<endl;
				assign_refcount++;
				std::swap(data,lvalue.data);
			}
			else
			{
				cout<<"copy_assignment: this object expires, cannot be assigned to rvalue anylonger"<<endl;
				//delete &lvalue;	
			}
		}
		return *data;
	}

	/*
		Overloaded Move Assignment operator
	*/

	T& operator=(expirable<T>&& rvalue) 
	{
		if(move_assignment)
		{
			if(assign_refcount < expiry_count)
			{
				cout<<"move_assignment: assignment operator invoked"<<endl;
				assign_refcount++;
				data=std::move(rvalue.data);
			}
			else
			{
				cout<<"move_assignment: this object expires, cannot be assigned to rvalue anylonger"<<endl;
				//delete &rvalue;	
			}
		}
		return *data;
	}
};

class IntObject
{
public:
	int num;
	IntObject(int x)
	{
		num=x;
	}

	~IntObject()
	{
		cout<<"object is deleted"<<endl;
	}
};
