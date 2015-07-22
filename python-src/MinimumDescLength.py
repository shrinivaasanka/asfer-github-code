#---------------------------------------------------------------------------------------------------------
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

import Entropy

#Zlib compression
import zlib
import sys
compstr=zlib.compress(sys.argv[1])
print "String Length = " + str(len(sys.argv[1]))
print "Minimum Description Length with Zlib compression = " + str(len(compstr))
print "Compression Ratio with Zlib compression = " + str(float(len(compstr))/float(len(sys.argv[1])))

#vowel compression
vowels=["a","e","i","o","u","A","E","I","O","U"]
stripvow = [x for x in sys.argv[1] if x not in vowels]
print "Minimum Description Length with vowel compression = " + str(len(stripvow))
print "Compression Ratio with vowel compression = " + str(float(len(stripvow))/float(len(sys.argv[1])))  

#Entropy measure for extent of order in text
e=Entropy.Entro()
estr=str(e.entropy(sys.argv[1]))
print "Entropy of the text (measure of minimum length describability) - weighted average of number of bits needed to describe text:",estr

#Minimum Description Length - Kraft Inequality
#Reference: http://homepages.cwi.nl/~pdg/ftp/mdlintro.ps
#If the text comprises standard ASCII or Unicode alphabet of size 256 or 512
#MDL = -log p1^n1 * p2^n2 * .... p256^n256 .... * p512^n512
#where each pi is probability of occurence of the alphabet
#and ni is number of occurrences of the alphabet - sigma(ni)=size of the text
#Thus the entire text is minimum-describable as Bernoulli trials
mdl=str(e.MDL(sys.argv[1]))
print "Minimum Description Length (Kraft Inequality) = ", mdl
