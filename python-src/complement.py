#-------------------------------------------------------------------------`
#ASFER - a ruleminer which gets rules specific to a query and executes them
#Copyright (C) 2009-2013  Ka.Shrinivaasan
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
#--------------------------------------------------------------------------------------------------------
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Independent Open Source Developer, Researcher and Consultant
#Ph: 9003082186, 9791165980
#Open Source Products Profile(Krishna iResearch): http://sourceforge.net/users/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
#--------------------------------------------------------------------------------------------------------

################################################################################################
# Test python script written in March 2011 While at CMI as JRF for 
# "Decidability of Existence and Construction of a Complement of a given Function" :
# http://arxiv.org/abs/1106.4102 and 
# https://sites.google.com/site/kuja27/ComplementOfAFunction_earlier_draft.pdf?attredirects=0
# Added to repository for numerical pattern analysis mentioned in http://sourceforge.net/p/asfer/code/HEAD/tree/AstroInferDesign.txt
################################################################################################

Lf=[2,3,5,7,11,13,17,19,23]

def getgofx(x):
    u=0
    z=-1
    while True:
        if u in Lf:
            u=u+1
        if u not in Lf:
            z=z+1
            if (z==x):
                return u
            else:
                u=u+1


for i in range(10):
     print "g(",i,")=",getgofx(i)
