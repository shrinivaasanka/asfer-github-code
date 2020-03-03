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
#Copyleft (Copyright+):
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Ph: 9791499106, 9003082186
#Krishna iResearch Open Source Products Profiles:
#http://sourceforge.net/users/ka_shrinivaasan,
#https://github.com/shrinivaasanka,
#https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com,
#kashrinivaasan@live.com
#--------------------------------------------------------------------------------------------------------

#Reference: WordNet::Similarity CPAN example - Copyright (c) 2005-2008, Ted Pedersen, Siddharth Patwardhan, Satanjeev Banerjee, and Jason Michelizzi - http://search.cpan.org/dist/WordNet-Similarity/

#!/usr/bin/perl

use WordNet::QueryData;
use WordNet::Similarity::path;
use WordNet::Similarity::PathFinder;
use 5.010;
#use warnings;

sub WordNetDistance
{
	my $word1 = shift;
	my $word2 = shift;
	my $wn = WordNet::QueryData->new;
	my $measure = WordNet::Similarity::path->new($wn);
	my $distance = $measure->getRelatedness($word1, $word2);
	($error, $errorString) = $measure->getError();
	my $traceString = $measure->getTraceString();
	print "distance=$distance \n";
	print "error=$error, errorString=$errorString \n";
	print "trace string = $traceString \n";
}

sub WordNetPath
{
	my $word1 = shift;
	my $word2 = shift;
	my $wn = WordNet::QueryData->new;
	my $measure = WordNet::Similarity::PathFinder->new($wn);
	my @paths = $measure->getAllPaths($word1, $word2, "n", "wps");
	print "All paths = $paths \n";
	print "path top = $paths[0][0] \n";
	print "path length = $paths[0][1] \n";
	print "path synsets = $paths[0][2] \n";

	my @synsets=$paths[0][2];
	foreach my $i (0 .. 100)
	{
		print "synset $i in path = $paths[0][2][$i] \n";
		if ($paths[0][2][$i] eq $word2)
		{
			last;
		}
	}
}

my $word1 = $ARGV[0];
my $word2 = $ARGV[1];
WordNetDistance($word1, $word2);
WordNetPath($word1, $word2);
