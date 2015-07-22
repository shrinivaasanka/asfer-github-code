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

#mail to: ka.shrinivaasan@gmail.com (Krishna iResearch)
########################################################################

from Bio.Alphabet import generic_dna
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment
from Bio import SeqIO
from Bio.Align.Applications import ClustalOmegaCommandline
import os

i=0
seqlist=[]
enchorofile=open("./asfer.enchoros","r")
for line in enchorofile:
	nextid="SeqId_"+str(i)
	line=line.strip()
	seqrec=SeqRecord(Seq(line, generic_dna), id=nextid)
	seqlist.append(seqrec)
	i=i+1

SeqIO.write(seqlist, "asfer.enchoros.unaligned.fasta", "fasta")

cline = ClustalOmegaCommandline(infile="asfer.enchoros.unaligned.fasta",outfile="asfer.enchoros.aligned.fasta",verbose=True, auto=True)
print "Executing ClustalOmega on unaligned Encoded Horoscopes File with commandline:",cline
os.system(str(cline))

