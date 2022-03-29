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
# Personal website(research): https://acadpdrafts.readthedocs.io/en/latest/
# --------------------------------------------------------------------------------------------------------

from __future__ import division

def factorial(n):
	if (n==0):
		return 1.0
	else:
		return n*factorial(n-1)


def power_of_4(n):
	power = 1.0 ;
	i=n
	while i > 0:
		power = power * 4.0;
		i = i - 1
	return power


#P(good) = (2n)!/(4^n) { 1/(n+1)!(n-1)! + 1/(n+2)!(n-2)! + ... + 1/(n+n)!(n-n)!}
n = 0
i=1
prevsum = 0.0
sum1 = 0.0
prevsumdiff = 0.0
sumdiff = 0.0
term1 = 0.0
while n < 30000:
	term1 = factorial(2*n) / power_of_4(n)
	while i <= n:
		sum1 = sum1 + (1.0 / (factorial(n+i) * factorial(n-i)))
		i = i + 1
	sum1 = term1 * sum1
	print "Probability of good choice for population of " + str(2*n) + "=" + str(sum1*100.0)
	sumdiff = sum1 - prevsum
	print "prob - prevprob = " + str(sumdiff)
	prevsum = sum1
	prevsumdiff = sumdiff
	sum1 =0.0
	n = n + 1
	i=1
	

