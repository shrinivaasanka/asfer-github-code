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

class HRAnalytics(object):
	def __init__(self):
		self.profile_text=[]
		self.work_experience=[]
		self.academics=[]
		self.total_work_experience=0
		self.total_academics=0

	def parse_profile(self, datasource, type, social_profile):
		if type=="pdf":
			self.file=open(social_profile,"rb")
			file_reader=PyPDF2.PdfFileReader(self.file)
			num_pages=file_reader.numPages
			for p in xrange(num_pages):
				page_object=file_reader.getPage(p)
				page_contents=page_object.getContents()
				for c in page_contents:
					print c.getObject()
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
			return profile_text
		else:
			self.file=open(social_profile,"r")
			profile_text=self.file.read()
			return profile_text

	def isdaterange(self,l):
		months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		monthdict={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
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
					self.total_work_experience += abs(tdelta.total_seconds())
					return True
			if len(starttok) == 1:
				if (int(starttok[0]) and int(endtok[0])) or end == "Present":
					startyear=int(starttok[0])
					endyear=int(endtok[0])
					startdate=datetime(startyear,1,1)
					enddate=datetime(endyear,1,1)
					tdelta=startdate-enddate
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
		rlfg.grow_lambda_function3(profile_contents)

	def least_energy_intrinsic_merit(self):
		print "Total work experience timedeltas:", self.total_work_experience
		print "Total academics:",self.total_academics
		self.log_normal_least_energy_intrinsic_merit = 1.0/float(math.log(self.total_work_experience) + math.log(self.total_academics)) 
		print "Inverse Log Normal Least Energy Intrinsic Merit (low values imply high merit):",self.log_normal_least_energy_intrinsic_merit

	def experiential_intrinsic_merit(self):
		#E = M*e^(kMt)		
		M=self.log_normal_least_energy_intrinsic_merit
		t=self.total_work_experience
		k=1
		self.experiential_intrinsic_merit=math.log(M) + float(k*M*t)
		print "Log Normal Experiential Intrinsic Merit:",self.experiential_intrinsic_merit	

if __name__=="__main__":
	hranal=HRAnalytics()
	#hranal.parse_profile("linkedin","pdf","testlogs/ProfileLinkedIn_KSrinivasan.pdf")
	#profile_text=hranal.parse_profile("linkedin","text","testlogs/ProfileLinkedIn_KSrinivasan.txt")
	#hranal.least_energy_intrinsic_merit()
	#hranal.experiential_intrinsic_merit()
	profile_text=hranal.parse_profile("none","tex","testlogs/CV.tex")
	hranal.rlfg_intrinsic_merit(profile_text)
