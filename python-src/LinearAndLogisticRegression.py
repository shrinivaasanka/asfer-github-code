#------------------------------------------------------------------------------------------------------------
#ASFER - a ruleminer which gets rules specific to a query and executes them (component of iCloud Platform)
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
#---------------------------------------------------------------------------------------------------------
#Copyright (C):
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Ph: 9789346927, 9003082186, 9791165980
#Krishna iResearch Open Source Products Profiles: 
#http://sourceforge.net/users/ka_shrinivaasan, https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#ZODIAC DATASOFT: https://github.com/shrinivaasanka/ZodiacDatasoft
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
#---------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------
#Linear Regression in 2 variables:
#y=w1*x1 + w2*x2 + b
#E.g may be used to predict a algorithmic economics dependent 
#variable like inflation which could be dependent
#on two independent variables money supply(x1) and demand (x2) 
#-----------------------------------------------------------------

import rpy2.robjects as robj
import math

def LinearRegression(weights,bias,x1s,x2s):
	for x1,x2 in zip(x1s, x2s):
		regressedoutput = bias + weights[0]*x1 + weights[1]*x2
		print "Linear Regression for [",x1,"] and [",x2,"]: ",regressedoutput

#-----------------------------------------------------------------
#Logistic Regression in 2 variables:
#y=1/(1+e^(-(w1*x1 + w2*x2 + b)))
#E.g may be used to predict a algorithmic economics dependent 
#variable like inflation which could be dependent
#on two independent variables money supply(x1) and demand (x2) 
#-----------------------------------------------------------------

def LogisticRegression(weights,bias,x1s,x2s):
	for x1,x2 in zip(x1s, x2s):
		regressedoutput = bias + 1/(1 + math.pow(2.718, -1*(weights[0]*x1 + weights[1]*x2+bias)))
		print "Logistic Regression for [",x1,"] and [",x2,"]: ",regressedoutput

weights=[2.0,5.0]
bias=0.0
x1s=[1.0,2.0,5.0,7.0,8.0]
x2s=[5.0,3.0,6.0,7.0,2.0]
print "##################"
print "Linear Regression:"
print "##################"
LinearRegression(weights,bias,x1s,x2s)
print "##################"
print "Logistic Regression:"
print "##################"
LogisticRegression(weights,bias,x1s,x2s)
