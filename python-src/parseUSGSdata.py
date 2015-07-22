#-------------------------------------------------------------------------`
#ASFER - a ruleminer which gets rules specific to a query and executes them
#
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
#
#-----------------------------------------------------------------------------------------------------------------------------------
#Copyright (C):
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Independent Open Source Developer, Researcher and Consultant
#Ph: 9003082186, 9791165980
#Open Source Products Profile(Krishna iResearch): http://sourceforge.net/users/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
#-----------------------------------------------------------------------------------------------------------------------------------

import os
from bs4 import BeautifulSoup

#eqdata=open("/home/kashrinivaasan/KrishnaiResearch_OpenSource/asfer-code/cpp-src/magnitude8_1900_date.php.html","r")
eqdata=open("./magnitude8_1900_date.php.html","r")
eqparsedtxt=open("./earthquakesFrom1900with8plusmag.pygen.txt","w")

parser=BeautifulSoup(eqdata.read())
zipped=zip(parser.find_all("td",headers="t2"), parser.find_all("td", headers="t6"), parser.find_all("td", headers="t7"))
print zipped
for tagtll in zipped:
	eqparsedtxt.write(str(tagtll[0].contents[0]).encode("utf-8"))
	eqparsedtxt.write(" ")
	eqparsedtxt.write(str(tagtll[1].contents[0]).encode("utf-8"))
	eqparsedtxt.write(" ")
	eqparsedtxt.write(str(tagtll[2].contents[0]).encode("utf-8"))
	eqparsedtxt.write("\n")

	


