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
#K.Srinivasan
#NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
#Personal website(research): https://sites.google.com/site/kuja27/
#--------------------------------------------------------------------------------------------------------

import PyPDF2
from RecursiveLambdaFunctionGrowth import RecursiveLambdaFunctionGrowth
from datetime import datetime
import sys
import math
from sympy.combinatorics.partitions import IntegerPartition
from scipy import stats


class HRAnalytics(object):
	def __init__(self):
		self.profile_text=[]
		self.work_experience=[]
		self.academics=[]
		self.total_work_experience=0
		self.total_academics=0
		self.timedeltas=[]
		self.stinthistogram=None

	def parse_profile(self, datasource, type, social_profile):
                profile_text=""
		if type=="pdf":
			self.file=open(social_profile,"rb")
			file_reader=PyPDF2.PdfFileReader(self.file)
			num_pages=file_reader.numPages
			for p in xrange(num_pages):
				page_object=file_reader.getPage(p)
				page_contents=page_object.extractText()
                                profile_text += page_contents
                        return profile_text 
		if datasource=="linkedin" and type=="text":
			self.file=open(social_profile,"r")
			profile_text=self.file.read()
			stints=[]
			self.file=open(social_profile,"r")
			for l in self.file.readlines():
				ltok=l.split()
				#print "ltok:",ltok
				if "Experience" in ltok:
					print "Profile"
					stints=self.work_experience
				if "Education" in ltok:
					print "Education"
					stints=self.academics
				if self.isdaterange(l):
					stints.append(l.strip())
			print "Work Experience:",self.work_experience
			print "Academics:",self.academics	
			#self.stinthistogram=IntegerPartition(self.timedeltas)
			print "Tenure Histogram - Integer Partition - :",self.timedeltas
			print "Tenure Histogram - Partition Rank:",max(self.timedeltas) - len(self.timedeltas)
			return profile_text
		else:
			self.file=open(social_profile,"r")
			profile_text=self.file.read()
			return profile_text

	def tenure_partition_rank_correlation(self,designations, remunerations, durations):
		tau1, pvalue1 = stats.kendalltau(designations, remunerations)
		tau2, pvalue2 = stats.kendalltau(designations, durations)
		tau3, pvalue3 = stats.kendalltau(remunerations, durations)
		print "Kendall Tau Rank Correlations - Designations and Remunerations: tau=",tau1,", pvalue=",pvalue1
		print "Kendall Tau Rank Correlations - Designations and Durations: tau=",tau2,", pvalue=",pvalue2
		print "Kendall Tau Rank Correlations - Durations and Remunerations: tau=",tau3,", pvalue=",pvalue3

	def isdaterange(self,l):
		months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		monthdict={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
		tdelta=0
		try:
			ltok=l.split("-")
			starttok=[]
			endtok=[]
			start=""
			end=""
			if len(ltok) > 1:
				start=ltok[0]
				starttok=start.split()
				end=ltok[1]
				endtok=end.split()
			if len(ltok) == 1:
				start=ltok[0]
				starttok=start.split()
			if len(starttok) > 1:
				if (starttok[0] in months and endtok[0] in months) or end == "Present":
					startmonth=monthdict[starttok[0]]
					startyear=int(starttok[1])
					endmonth=monthdict[endtok[0]]
					endyear=int(endtok[1])
					startdate=datetime(startyear,startmonth,1)
					enddate=datetime(endyear,endmonth,1)
					print "startdate:",startdate
					print "enddate:",enddate
					tdelta=startdate-enddate
					self.timedeltas.append(int(abs(tdelta.total_seconds())))
					self.total_work_experience += abs(tdelta.total_seconds())
					return True
			if len(starttok) == 1:
				if (int(starttok[0]) and int(endtok[0])) or end == "Present":
					startyear=int(starttok[0])
					endyear=int(endtok[0])
					startdate=datetime(startyear,1,1)
					enddate=datetime(endyear,1,1)
					tdelta=startdate-enddate
					self.timedeltas.append(int(abs(tdelta.total_seconds())))
					self.total_academics += abs(tdelta.total_seconds())
					print "startdate:",startdate
					print "enddate:",enddate
					return True	
			return False
		except Exception:
			print sys.exc_info() 
			return False
			
	def rlfg_intrinsic_merit(self, profile_contents):
		rlfg=RecursiveLambdaFunctionGrowth()
		rlfg.grow_lambda_function3(profile_contents,2)

	def least_energy_intrinsic_merit(self):
		print "Total work experience timedeltas:", self.total_work_experience
		print "Total academics:",self.total_academics
		self.log_normal_least_energy_intrinsic_merit = 1.0/float(math.log(self.total_work_experience) + math.log(self.total_academics)) 
		print "Inverse Log Normal Least Energy Intrinsic Merit (low values imply high merit):",self.log_normal_least_energy_intrinsic_merit

	def experiential_intrinsic_merit(self,degree=0):
		#E = M*e^(kMt) = log(dv(t)) * e^(klog(dv(t))*t/clogt) / clogt for evolving degree dv(t)
		#after time t
		if degree==0:
			M=self.log_normal_least_energy_intrinsic_merit
			t=self.total_work_experience
			k=1
			self.experiential_intrinsic_merit=math.log(M) + float(k*M*t)
			print "Log Normal Experiential Intrinsic Merit:",self.experiential_intrinsic_merit	
		else:
			logdegree=math.log(degree)
			tdelta=float(self.total_work_experience + self.total_academics)/1000000.0
			numer=logdegree*tdelta
			print "tdelta:",tdelta
			denom=math.log(tdelta)
			self.experiential_intrinsic_merit=logdegree * math.exp(numer/denom) / denom
			print "Experiential Intrinsic Merit:",self.experiential_intrinsic_merit	

	def parse_connections(self, connections):
		connections_tok=connections.split()
		number_of_connections=connections_tok[connections_tok.index("Connections") - 2]
		print "number of connections:", number_of_connections
		print "connections:", connections_tok
		return int(number_of_connections)

if __name__=="__main__":
	hranal=HRAnalytics()
	#profile_text=hranal.parse_profile("linkedin","pdf","testlogs/CV.pdf")
        #print profile_text
	#profile_text=hranal.parse_profile("linkedin","text","testlogs/ProfileLinkedIn_KSrinivasan.txt")
	#hranal.least_energy_intrinsic_merit()
	#hranal.experiential_intrinsic_merit()
	#profile_text=hranal.parse_profile("none","tex","testlogs/CV.tex")
	profile_text=hranal.parse_profile("linkedin","text","testlogs/ProfileLinkedIn_KSrinivasan.txt")
	#hranal.rlfg_intrinsic_merit(profile_text)
	number_of_connections=hranal.parse_connections(profile_text)
	hranal.least_energy_intrinsic_merit()
	hranal.experiential_intrinsic_merit(number_of_connections)
	designations=[1,2,3,4,5,6,7]
	remunerations=[100000,700000,1000000,1300000,200000,1400000,2500000]
	durations=[0.7,5,0.1,2,3,2,0.5]
	hranal.tenure_partition_rank_correlation(designations, remunerations, durations)
	#profile_text=hranal.parse_profile("none","text","testlogs/ConnectionsLinkedIn_KSrinivasan.txt")
	#hranal.rlfg_intrinsic_merit(profile_text)
