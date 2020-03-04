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

import PyPDF2
from datetime import datetime
import sys
import math
from sympy.combinatorics.partitions import IntegerPartition
from scipy import stats
import pandas
import numpy as np
import json
import nameparser
import re
from CompressedSensing import CompressedSensing
from jellyfish import match_rating_codex


class HRAnalytics(object):
    def __init__(self):
        self.profile_text = []
        self.work_experience = []
        self.academics = []
        self.total_work_experience = 0
        self.total_academics = 0
        self.timedeltas = []
        self.stinthistogram = None

    def parse_profile(self, datasource, type, social_profile):
        profile_text = ""
        if type == "pdf":
            self.file = open(social_profile, "rb")
            file_reader = PyPDF2.PdfFileReader(self.file)
            num_pages = file_reader.numPages
            for p in range(num_pages):
                page_object = file_reader.getPage(p)
                page_contents = page_object.extractText()
                profile_text += page_contents
            return profile_text
        if datasource == "linkedin" and type == "text":
            self.file = open(social_profile, "r")
            profile_text = self.file.read()
            stints = []
            self.file = open(social_profile, "r")
            for l in self.file.readlines():
                ltok = l.split()
                #print "ltok:",ltok
                if "Experience" in ltok:
                    print("Profile")
                    stints = self.work_experience
                if "Education" in ltok:
                    print("Education")
                    stints = self.academics
                if self.isdaterange(l):
                    stints.append(l.strip())
            print("Work Experience:", self.work_experience)
            print("Academics:", self.academics)
            # self.stinthistogram=IntegerPartition(self.timedeltas)
            print("Tenure Histogram - Integer Partition - :", self.timedeltas)
            print("Tenure Histogram - Partition Rank:", max(
                self.timedeltas) - len(self.timedeltas))
            return profile_text
        else:
            self.file = open(social_profile, "r")
            profile_text = self.file.read()
            return profile_text

    def tenure_partition_rank_correlation(self, designations, remunerations, durations):
        tau1, pvalue1 = stats.kendalltau(designations, remunerations)
        tau2, pvalue2 = stats.kendalltau(designations, durations)
        tau3, pvalue3 = stats.kendalltau(remunerations, durations)
        print("Kendall Tau Rank Correlations - Designations and Remunerations: tau=", tau1, ", pvalue=", pvalue1)
        print("Kendall Tau Rank Correlations - Designations and Durations: tau=", tau2, ", pvalue=", pvalue2)
        print("Kendall Tau Rank Correlations - Durations and Remunerations: tau=", tau3, ", pvalue=", pvalue3)

    def nameparser(self, full_name, pattern, context):
        name = nameparser.HumanName(full_name)
        print("HumanName Parser - parsed name (wrong):", repr(name))
        nametokenized = full_name.split(" ")
        print("nametokenized = ", nametokenized)
        contexttokenized = context.splitlines()
        print("contexttokenized = ", contexttokenized)
        for n in nametokenized:
            for m in contexttokenized:
                if n in m:
                    print("NeuronRain Human Name Parsing by Context - nameparser(): name substring - ", n, " - found in context = ", m)
                    regex = re.search(pattern, m, flags=re.IGNORECASE)
                    if regex is None:
                        continue
                    regexgroupdict = regex.groupdict()
                    for k, v in regexgroupdict.items():
                        print("NeuronRain Human Name Parsing by Context - nameparser():", k, ":", v)
                    return regexgroupdict

    def pipldotcom_analytics(self, first_name=None, last_name=None, email=None):
        from piplapis.search import SearchAPIRequest
        request = SearchAPIRequest(email=email, first_name=first_name,
                                   last_name=last_name, api_key='20307is19nx0tu0mar4zt987')
        response = request.send()
        print("pipldotcom_analytics(): JSON response for query (", first_name, ",", last_name, ",", email, "):")
        jsonloads = json.loads(response.to_json())
        print(json.dumps(jsonloads, indent=5, sort_keys=True))

    def linkedin_dataset_tenure_analytics(self, linkedindata):
        from pyspark.sql import SparkSession
        from pyspark.sql import DataFrameStatFunctions as dfsfunc
        from pyspark.ml.feature import VectorAssembler
        from pyspark.ml.stat import Correlation
        from pyspark.sql.types import IntegerType
        spsess = SparkSession.builder.master(
            "local[4]").appName("People Analytics").getOrCreate()
        df = spsess.read.format("csv").option(
            "header", "true").load(linkedindata)
        #tenures=sorted(df.groupBy(['avg_n_pos_per_prev_tenure', 'avg_pos_len', 'avg_prev_tenure_len', 'c_name', 'm_urn', 'n_pos', 'n_prev_tenures', 'tenure_len', 'age', 'beauty', 'beauty_female', 'beauty_male', 'blur', 'blur_gaussian', 'blur_motion', 'emo_anger', 'emo_disgust', 'emo_fear', 'emo_happiness', 'emo_neutral', 'emo_sadness', 'emo_surprise', 'ethnicity', 'face_quality', 'gender', 'glass', 'head_pitch', 'head_roll', 'head_yaw', 'img', 'mouth_close', 'mouth_mask', 'mouth_open', 'mouth_other', 'skin_acne', 'skin_dark_circle', 'skin_health', 'skin_stain', 'smile', 'african', 'celtic_english', 'east_asian', 'european', 'greek', 'hispanic', 'jewish', 'muslim', 'nationality', 'nordic', 'south_asian', 'n_followers']).agg(['c_name']).collect())
        variables = ['avg_n_pos_per_prev_tenure', 'avg_pos_len', 'avg_prev_tenure_len', 'c_name', 'm_urn', 'n_pos', 'n_prev_tenures', 'tenure_len', 'age', 'beauty', 'beauty_female', 'beauty_male', 'blur', 'blur_gaussian', 'blur_motion', 'emo_anger', 'emo_disgust', 'emo_fear', 'emo_happiness', 'emo_neutral', 'emo_sadness', 'emo_surprise', 'ethnicity', 'face_quality',
                     'gender', 'glass', 'head_pitch', 'head_roll', 'head_yaw', 'img', 'mouth_close', 'mouth_mask', 'mouth_open', 'mouth_other', 'skin_acne', 'skin_dark_circle', 'skin_health', 'skin_stain', 'smile', 'african', 'celtic_english', 'east_asian', 'european', 'greek', 'hispanic', 'jewish', 'muslim', 'nationality', 'nordic', 'south_asian', 'n_followers']
        for v in variables:
            df = df.withColumn(v, df[v].cast(IntegerType()))
        assembler = VectorAssembler(
            inputCols=variables, outputCol="TenureCorrelations")
        tenuredf = assembler.transform(df)
        avg_n_pos_per_prev_tenure = [x.avg_n_pos_per_prev_tenure for x in tenuredf.select(
            tenuredf.avg_n_pos_per_prev_tenure).orderBy(tenuredf.avg_n_pos_per_prev_tenure).collect()]
        avg_pos_len = [x.avg_pos_len for x in tenuredf.select(
            tenuredf.avg_pos_len).orderBy(tenuredf.avg_pos_len).collect()]
        avg_prev_tenure_len = [x.avg_prev_tenure_len for x in tenuredf.select(
            tenuredf.avg_prev_tenure_len).orderBy(tenuredf.avg_prev_tenure_len).collect()]
        n_prev_tenures = [x.n_prev_tenures for x in tenuredf.select(
            tenuredf.n_prev_tenures).orderBy(tenuredf.n_prev_tenures).collect()]
        tenure_len = [x.tenure_len for x in tenuredf.select(
            tenuredf.tenure_len).orderBy(tenuredf.tenure_len).collect()]
        n_followers = [x.n_followers for x in tenuredf.select(
            tenuredf.n_followers).orderBy(tenuredf.n_followers).collect()]
        tau1, pvalue1 = stats.kendalltau(
            avg_n_pos_per_prev_tenure, avg_pos_len)
        tau2, pvalue2 = stats.kendalltau(
            avg_n_pos_per_prev_tenure, avg_prev_tenure_len)
        tau3, pvalue3 = stats.kendalltau(avg_prev_tenure_len, avg_pos_len)
        print("linkedin_dataset_tenure_analytics(): tau1  = ", tau1, ", pvalue1 = ", pvalue1)
        print("linkedin_dataset_tenure_analytics(): tau2  = ", tau2, ", pvalue2 = ", pvalue2)
        print("linkedin_dataset_tenure_analytics(): tau3  = ", tau3, ", pvalue3 = ", pvalue3)
        linkedin_lognormal_experiential_merits = []
        linkedin_degree_experiential_merits = []
        print("###########################################################################")
        for n in range(df.count()):
            experience = abs(
                avg_n_pos_per_prev_tenure[n] * avg_pos_len[n] * n_prev_tenures[n] + tenure_len[n])
            print("Experience computed from LinkedIn Dataset:", experience)
            print("n_followers = ", n_followers[n])
            if experience > 0:
                k = 1.0
                M = 1.0/float(math.log(experience))
                t = experience
                lognormal_experiential_intrinsic_merit = math.log(
                    M) + float(k*M*t)
                print("LinkedIn DataSet - Log Normal Experiential Intrinsic Merit for this profile:", lognormal_experiential_intrinsic_merit)
                linkedin_lognormal_experiential_merits.append(
                    lognormal_experiential_intrinsic_merit)
            else:
                linkedin_lognormal_experiential_merits.append(0)
            if abs(n_followers[n]) > 0:
                logdegree = math.log(abs(n_followers[n]))
                tdelta = float(experience)
                numer = logdegree*tdelta/100000.0
                print("tdelta:", tdelta)
                denom = abs(math.log(tdelta))
                print("numer", numer)
                print("denom:", denom)
                try:
                    degree_experiential_intrinsic_merit = logdegree * \
                        math.exp(float(numer)/float(denom)) / denom
                except:
                    degree_experiential_intrinsic_merit = 0.0
                print("LinkedIn DataSet - Degree Experiential Intrinsic Merit for this profile:", degree_experiential_intrinsic_merit)
                linkedin_degree_experiential_merits.append(
                    degree_experiential_intrinsic_merit)
            else:
                linkedin_degree_experiential_merits.append(0)
        tenurearray = np.array([avg_n_pos_per_prev_tenure, avg_pos_len, avg_prev_tenure_len, n_prev_tenures,
                                tenure_len, linkedin_lognormal_experiential_merits, linkedin_degree_experiential_merits])
        pandasDF = pandas.DataFrame(tenurearray.T, columns=['avg_n_pos_per_prev_tenure', 'avg_pos_len', 'avg_prev_tenure_len',
                                                            'n_prev_tenures', 'tenure_len', 'lognormal_experiential_merits', 'degree_experiential_merits'])
        print("linkedin_dataset_tenure_analytics(): pandas correlation coefficient = ", pandasDF.corr())

    def isdaterange(self, l):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthdict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                     'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
        tdelta = 0
        try:
            ltok = l.split("-")
            starttok = []
            endtok = []
            start = ""
            end = ""
            if len(ltok) > 1:
                start = ltok[0]
                starttok = start.split()
                end = ltok[1]
                endtok = end.split()
            if len(ltok) == 1:
                start = ltok[0]
                starttok = start.split()
            if len(starttok) > 1:
                if (starttok[0] in months and endtok[0] in months) or end == "Present":
                    startmonth = monthdict[starttok[0]]
                    startyear = int(starttok[1])
                    endmonth = monthdict[endtok[0]]
                    endyear = int(endtok[1])
                    startdate = datetime(startyear, startmonth, 1)
                    enddate = datetime(endyear, endmonth, 1)
                    print("startdate:", startdate)
                    print("enddate:", enddate)
                    tdelta = startdate-enddate
                    self.timedeltas.append(int(abs(tdelta.total_seconds())))
                    self.total_work_experience += abs(tdelta.total_seconds())
                    return True
            if len(starttok) == 1:
                if (int(starttok[0]) and int(endtok[0])) or end == "Present":
                    startyear = int(starttok[0])
                    endyear = int(endtok[0])
                    startdate = datetime(startyear, 1, 1)
                    enddate = datetime(endyear, 1, 1)
                    tdelta = startdate-enddate
                    self.timedeltas.append(int(abs(tdelta.total_seconds())))
                    self.total_academics += abs(tdelta.total_seconds())
                    print("startdate:", startdate)
                    print("enddate:", enddate)
                    return True
            return False
        except Exception:
            print(sys.exc_info())
            return False

    def rlfg_intrinsic_merit(self, profile_contents):
        from RecursiveLambdaFunctionGrowth import RecursiveLambdaFunctionGrowth
        from RecursiveGlossOverlap_Classifier import nondictionaryword
        dictionary=open("Dictionary.txt")
        dictwords=[]
        for d in dictionary.readlines():
            dictword=d.split(" ")[0]
            if dictword:
                dictwords.append(dictword)
        #print("profile_contents:",profile_contents)
        filteredprofilecontents=[]
        for p in profile_contents.split():
            #print("p:",p)
            if p in dictwords:
                filteredprofilecontents.append(p)
        rlfg = RecursiveLambdaFunctionGrowth()
        filteredprofiletext=" ".join(list(set(filteredprofilecontents))[:50])
        print("filteredprofilecontents:",filteredprofilecontents)
        rlfg.grow_lambda_function3(text=filteredprofiletext)

    def least_energy_intrinsic_merit(self):
        print("Total work experience timedeltas:", self.total_work_experience)
        print("Total academics:", self.total_academics)
        self.log_normal_least_energy_intrinsic_merit = 1.0 / \
            float(math.log(self.total_work_experience) +
                  math.log(self.total_academics))
        print("Inverse Log Normal Least Energy Intrinsic Merit (low values imply high merit):", self.log_normal_least_energy_intrinsic_merit)

    def experiential_intrinsic_merit(self, degree=0):
        # E = M*e^(kMt) = log(dv(t)) * e^(klog(dv(t))*t/clogt) / clogt for evolving degree dv(t)
        # after time t
        if degree == 0:
            M = self.log_normal_least_energy_intrinsic_merit
            t = self.total_work_experience
            k = 1
            self.experiential_intrinsic_merit = math.log(M) + float(k*M*t)
            print("Log Normal Experiential Intrinsic Merit:", self.experiential_intrinsic_merit)
        else:
            logdegree = math.log(degree)
            tdelta = float(self.total_work_experience +
                           self.total_academics)/1000000.0
            numer = logdegree*tdelta
            print("tdelta:", tdelta)
            denom = math.log(tdelta)
            self.experiential_intrinsic_merit = logdegree * \
                math.exp(numer/denom) / denom
            print("Experiential Intrinsic Merit:", self.experiential_intrinsic_merit)

    def parse_connections(self, connections):
        connections_tok = connections.split()
        number_of_connections = connections_tok[connections_tok.index(
            "Connections") - 2]
        print("number of connections:", number_of_connections)
        print("connections:", connections_tok)
        return int(number_of_connections)


if __name__ == "__main__":
    hranal = HRAnalytics()
    #profile_text = hranal.parse_profile("linkedin", "pdf", "testlogs/CV.pdf")
    #print profile_text
    # profile_text=hranal.parse_profile("linkedin","text","testlogs/ProfileLinkedIn_KSrinivasan.txt")
    # hranal.least_energy_intrinsic_merit()
    # hranal.experiential_intrinsic_merit()
    # profile_text=hranal.parse_profile("none","tex","testlogs/CV.tex")
    # profile_text=hranal.parse_profile("linkedin","text","testlogs/ProfileLinkedIn_KSrinivasan.txt")
    # hranal.rlfg_intrinsic_merit(profile_text)
    # number_of_connections=hranal.parse_connections(profile_text)
    # hranal.least_energy_intrinsic_merit()
    # hranal.experiential_intrinsic_merit(number_of_connections)
    # designations=[1,2,3,4,5,6,7]
    # remunerations=[100000,700000,1000000,1300000,200000,1400000,2500000]
    # durations=[0.7,5,0.1,2,3,2,0.5]
    #hranal.tenure_partition_rank_correlation(designations, remunerations, durations)
    # hranal.linkedin_dataset_tenure_analytics("linkedin_data.csv")
    profile_text=hranal.parse_profile("none","text","testlogs/ConnectionsLinkedIn_KSrinivasan.txt")
    #profile_text=hranal.parse_profile("none","pdf","testlogs/ConnectionsLinkedIn_KSrinivasan.pdf")
    hranal.rlfg_intrinsic_merit(profile_text)
    # hranal.pipldotcom_analytics(first_name=u'Srinivasan',last_name=u'Kannan',email='ka.shrinivaasan@gmail.com')
    # hranal.pipldotcom_analytics(first_name=u'Srinivasan',last_name=u'Kannan',email='shrinivas.kannan@gmail.com')
    # hranal.pipldotcom_analytics(first_name=u'Srinivasan',last_name=u'Kannan',email='kashrinivaasan@live.com')
    # emailcontexts=["testlogs/SocialNetworkAnalysis_PeopleAnalytics_NameParsing/SocialNetworkAnalysis_PeopleAnalytics_NameParsing1.txt","testlogs/SocialNetworkAnalysis_PeopleAnalytics_NameParsing/SocialNetworkAnalysis_PeopleAnalytics_NameParsing2.txt","testlogs/SocialNetworkAnalysis_PeopleAnalytics_NameParsing/SocialNetworkAnalysis_PeopleAnalytics_NameParsing3.txt","testlogs/SocialNetworkAnalysis_PeopleAnalytics_NameParsing/SocialNetworkAnalysis_PeopleAnalytics_NameParsing4.txt","testlogs/SocialNetworkAnalysis_PeopleAnalytics_NameParsing/SocialNetworkAnalysis_PeopleAnalytics_NameParsing5.txt"]
    # for emailcontext in emailcontexts:
    #    ecf=open(emailcontext)
    #    emailcontext_text=ecf.read()
    #    print "============================================================================="
    #    hranal.nameparser("Kannan Srinivasan",r"(?P<second_name>\w+).(?P<first_name>\w+)",emailcontext_text)
    #    print "============================================================================="
    #    hranal.nameparser("Kannan Srinivasan",r"(?P<second_name>\w+) (?P<first_name>\w+)",emailcontext_text)
    idcontexts = ["testlogs/SocialNetworkAnalysis_PeopleAnalytics_NameParsing/SocialNetworkAnalysis_PeopleAnalytics_NameParsing6.txt",
                  "testlogs/SocialNetworkAnalysis_PeopleAnalytics_NameParsing/SocialNetworkAnalysis_PeopleAnalytics_NameParsing7.txt", "testlogs/SocialNetworkAnalysis_PeopleAnalytics_NameParsing/SocialNetworkAnalysis_PeopleAnalytics_NameParsing8.txt"]
    for idcontext in idcontexts:
        idf = open(idcontext)
        idcontext_text = idf.read()
        print("==============================================================================")
        hranal.nameparser(
            "Kannan Srinivasan", r"(?P<second_name>\w+) (?P<first_name>\w+)", idcontext_text)
        hranal.nameparser(
            "kannan srinivasan", r"(?P<second_name>\w+) (?P<first_name>\w+)", idcontext_text.lower())
        print("==============================================================================")
    csensing = CompressedSensing()
    syllvector1 = csensing.syllable_boundary_text_compression("Shrinivaasan")
    syllvector2 = csensing.syllable_boundary_text_compression("Shrinivas")
    syllvector3 = csensing.syllable_boundary_text_compression("Srinivasan")
    syllvector4 = csensing.syllable_boundary_text_compression(profile_text)
    print("======================================================================")
    print("Match Rating Codex ")
    print("======================================================================")
    mr1 = match_rating_codex(str("Shrinivaasan"))
    mr2 = match_rating_codex(str("Shrinivas"))
    mr3 = match_rating_codex(str("Srinivasan"))
    print("Match ratings for same name of differing spellings - [Shrinivaasan,Shrinivas,Srinivasan]:", [
        mr1, mr2, mr3])
