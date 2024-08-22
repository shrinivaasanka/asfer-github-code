# -------------------------------------------------------------------------------------------------------
# NEURONRAIN ASFER - Software for Mining Large Datasets
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------------------------------
# K.Srinivasan
# NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
# Personal website(research): https://sites.google.com/site/kuja27/
# --------------------------------------------------------------------------------------------------------

import Entropy

# Zlib compression
import zlib
import sys

def normalized_compression_distance(string1,string2):
    compstr_12 = len(zlib.compress(bytes((string1+string2).encode("utf-8"))))
    compstr_1 = len(zlib.compress(bytes(string1.encode("utf-8"))))
    compstr_2 = len(zlib.compress(bytes(string2.encode("utf-8"))))
    ncd = (compstr_12 - min(compstr_1,compstr_2)) / max(compstr_1,compstr_2)
    print("Normalized Compression Distance (approximation of Kolmogorov Complexity) between 2 strings:",ncd)
    return ncd

def minimum_descriptive_complexity(string):
    compstr = zlib.compress(bytes(string.encode("utf-8")))
    print("String Length = " + str(len(string)))
    print("Minimum Description Length with Zlib compression = " + str(len(compstr)))
    print("Compression Ratio with Zlib compression = " +
          str(float(len(compstr))/float(len(string))))

    # vowel compression
    vowels = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
    stripvow = [x for x in string if x not in vowels]
    print("Minimum Description Length with vowel compression = " + str(len(stripvow)))
    print("Compression Ratio with vowel compression = " +
          str(float(len(stripvow))/float(len(string))))

    # Entropy measure for extent of order in text
    e = Entropy.Entro()
    estr = str(e.entropy(string))
    print("Entropy of the text (measure of minimum length describability) - weighted average of number of bits needed to describe text:", estr)

    # Minimum Description Length - Kraft Inequality
    # Reference: http://homepages.cwi.nl/~pdg/ftp/mdlintro.ps
    # If the text comprises standard ASCII or Unicode alphabet of size 256 or 512
    # MDL = -log p1^n1 * p2^n2 * .... p256^n256 .... * p512^n512
    # where each pi is probability of occurence of the alphabet
    # and ni is number of occurrences of the alphabet - sigma(ni)=size of the text
    # Thus the entire text is minimum-describable as Bernoulli trials
    mdl = str(e.MDL(string))
    print("Minimum Description Length (Kraft Inequality) = ", mdl)
    return (mdl, estr)


if __name__ == "__main__":
    minimum_descriptive_complexity("askkdjkjskjdkjskjdsjdjsdwiieuieui")
