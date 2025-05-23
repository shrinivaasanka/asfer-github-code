# -------------------------------------------------------------------------------------------------------
# ASFER - Software for Mining Large Datasets
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


# *****************************************************************************/
# Copyright attribution for Maitreya text client referred in this file:
#
#  Maitreya, open source platform for Vedic and western astrology.
#  Release    8.0
#  Author     Martin Pettau
#  Copyright  2003-2012 by the author
#  http://www.saravali.de/
# ****************************************************************************/

import os
import sys
import getopt
import math
from datetime import date, time, datetime, timedelta
from collections import defaultdict

useGeonames = False
ClassAssociationRuleSearch = False
PlanetariumSearch = True
if useGeonames:
    from . import geonames
MaitreyasDreams_Version = "8.0"
SearchOption = 2
max_iterations = 100000000
min_year = 0
min_month = 0
min_days = 0
min_hours = 0
min_minutes = 0
min_seconds = 0
min_long = 0
min_lat = 0
max_year = 0
max_month = 0
max_days = 0
max_hours = 0
max_minutes = 0
max_seconds = 0
max_long = 0
max_lat = 0
opts, args = getopt.getopt(sys.argv[1:], "x", ["min_year=", "min_month=", "min_days=", "min_hours=", "min_minutes=", "min_seconds=",
                                               "min_long=", "min_lat=", "max_year=", "max_month=", "max_days=", "max_hours=", "max_minutes=", "max_seconds=", "max_long=", "max_lat="])
print(opts)
print(args)
for opt, arg in opts:
    print(opt)
    print(arg)
    if opt == "--min_year":
        min_year = int(arg)
    if opt == "--min_month":
        min_month = int(arg)
    if opt == "--min_days":
        min_days = int(arg)
    if opt == "--min_hours":
        min_hours = int(arg)
    if opt == "--min_minutes":
        min_minutes = int(arg)
    if opt == "--min_seconds":
        min_seconds = int(arg)
    if opt == "--min_long":
        min_long = int(arg)
    if opt == "--min_lat":
        min_lat = int(arg)
    if opt == "--max_year":
        max_year = int(arg)
    if opt == "--max_month":
        max_month = int(arg)
    if opt == "--max_days":
        max_days = int(arg)
    if opt == "--max_hours":
        max_hours = int(arg)
    if opt == "--max_minutes":
        max_minutes = int(arg)
    if opt == "--max_seconds":
        max_seconds = int(arg)
    if opt == "--max_long":
        max_long = int(arg)
    if opt == "--max_lat":
        max_lat = int(arg)


class NextDateTimeTimezoneLonglat:
    def __iter__(self):
        global min_year
        global min_month
        global min_days
        global min_hours
        global min_minutes
        global min_seconds
        global min_long
        global min_lat
        global max_year
        global max_month
        global max_days
        global max_hours
        global max_minutes
        global max_seconds
        global max_long
        global max_lat
        print("__iter__:", min_long, max_long)
        for long_deg in range(min_long, max_long, 1):
            for long_min in range(0, 9, 1):
                for lat_deg in range(min_lat, max_lat, 1):
                    for lat_min in range(0, 9, 1):
                        begin_datetime = datetime(
                            min_year, min_month, min_days, min_hours, min_minutes, min_seconds)
                        next_datetime = datetime(
                            min_year, min_month, min_days, min_hours, min_minutes, min_seconds)
                        end_datetime = datetime(
                            max_year, max_month, max_days, max_hours, max_minutes, max_seconds)
                        time_delta = timedelta(days=1)
                        while next_datetime <= end_datetime:
                            next_datetime = next_datetime + time_delta
                            print("next_datetime: ", next_datetime)
                            date_time_timezone_longlat = " --date=\"" + str(next_datetime.year) + "-" + str(next_datetime.month) + "-" + str(next_datetime.day) + " " + str(next_datetime.hour) + ":" + str(next_datetime.minute) + ":" + str(next_datetime.second) + " " + self.geonames_time_zone(
                                str(long_deg) + "." + str(long_min) + " " + str(lat_deg) + "." + str(lat_min)) + "\"  --location=\" x " + str(long_deg) + ":" + str(long_min) + ":" + str(0) + " " + str(lat_deg) + ":" + str(lat_min) + ":" + str(0) + " \" --planet-list"
                            yield date_time_timezone_longlat

    def geonames_time_zone(self, latlong):
        print(latlong)
        latlong_tokens = latlong.split(" ")
        # Geonames Geolocation free service lookup seems to have a limit on number of webservice lookups per hour
        # preferentially switch with a boolean flag
        if useGeonames:
            geonames_client = geonames.GeonamesClient('ka_shrinivaasan')
            geonames_result = geonames_client.find_timezone(
                {'lat': latlong_tokens[1], 'lng': latlong_tokens[0]})
            print(geonames_result)
            if geonames_result['gmtOffset'] is not None:
                geonames_timezone = str(geonames_result['gmtOffset'])
            else:
                geonames_timezone = "0"
        else:
            geonames_timezone = "5.5"
        return geonames_timezone


def toString(planetslist):
    planetsliststring = ""
    # return " , ".join(planetslist)
    if len(planetslist) < 1:
        return "Unoccupied"
    for p in planetslist:
        planetsliststring += p
        planetsliststring += " , "
    print("toString() planetsliststring=", planetsliststring[:-3])
    return planetsliststring[:-3]


def substring_find(str1, str2):
    issubstring = False
    s1 = 0
    s2 = 0
    beg = -1
    while s1+len(str2) < len(str1):
        s2 = 0
        while s2 < len(str2):
            if str1[s1+s2] == str2[s2]:
                if s2 == len(str2)-2:
                    issubstring = True
                    beg = s1
                    break
            else:
                break
            s2 = s2+1
        s1 = s1+1
        if issubstring == True:
            break
    if issubstring == True:
        return beg
    else:
        return -1

def match_chart_and_rule(sign_planets_dict_chart,pruned_rule):
    print("match_chart_and_rule(): pruned_rule = ",pruned_rule)
    pruned_rule_toks_1d=pruned_rule.split(",")
    pruned_rule_toks_2d="-".join(pruned_rule_toks_1d).split("- Cus -")
    print("match_chart_and_rule(): pruned_rule_toks_2d = ",pruned_rule_toks_2d) 
    pruned_rule_dict=defaultdict(list)
    pruned_rule_dict['Ari']=[n.strip() for n in pruned_rule_toks_2d[0].split(" - ")]
    pruned_rule_dict['Tau']=[n.strip() for n in pruned_rule_toks_2d[1].split(" - ")]
    pruned_rule_dict['Gem']=[n.strip() for n in pruned_rule_toks_2d[2].split(" - ")]
    pruned_rule_dict['Can']=[n.strip() for n in pruned_rule_toks_2d[3].split(" - ")]
    pruned_rule_dict['Leo']=[n.strip() for n in pruned_rule_toks_2d[4].split(" - ")]
    pruned_rule_dict['Vir']=[n.strip() for n in pruned_rule_toks_2d[5].split(" - ")]
    pruned_rule_dict['Lib']=[n.strip() for n in pruned_rule_toks_2d[6].split(" - ")]
    pruned_rule_dict['Sco']=[n.strip() for n in pruned_rule_toks_2d[7].split(" - ")]
    pruned_rule_dict['Sag']=[n.strip() for n in pruned_rule_toks_2d[8].split(" - ")]
    pruned_rule_dict['Cap']=[n.strip() for n in pruned_rule_toks_2d[9].split(" - ")]
    pruned_rule_dict['Aqu']=[n.strip() for n in pruned_rule_toks_2d[10].split(" - ")]
    pruned_rule_dict['Pis']=[n.strip() for n in pruned_rule_toks_2d[11].split(" - ")]
    print("match_chart_and_rule(): pruned_rule_dict = ", pruned_rule_dict)
    print("match_chart_and_rule(): sign_planets_dict_chart = ", sign_planets_dict_chart)
    patternindex = 1
    for k1,v1 in pruned_rule_dict.items():
        if v1 == ['Uno'] and sign_planets_dict_chart[k1] != []:
            print("1.sign_planets_dict_chart[k1] = ",sign_planets_dict_chart[k1],",v1 = ",v1)
            patternindex = -1
        else:
            if v1 != ['Uno'] and sign_planets_dict_chart[k1] != v1:
                 print("2.sign_planets_dict_chart[k1] = ",sign_planets_dict_chart[k1],",v1 = ",v1)
                 patternindex = -1
    return patternindex

def prune_rule(rule):
    rule_toks = rule.split(",")
    print("rule_toks:", rule_toks)
    pruned_rule_toks = [planet.strip()[:3] for planet in rule_toks]
    print("pruned_rule_toks:", pruned_rule_toks)
    return " , ".join(pruned_rule_toks)


if __name__ == "__main__":
    if SearchOption == 1:
        if ClassAssociationRuleSearch:
            rules_file = open("./MinedClassAssociationRules.txt", "r")
        elif PlanetariumSearch:
            rules_file = open("./CelestialConfiguration.txt", "r")
        rule_planets_list = []
        for rule in rules_file:
            print(len(rule.split(",")))
            if len(rule.split(" , ")) > 1:
                rule_planets = rule.strip().split(' ,')
                rule_planets_stripped = []
                for r in rule_planets:
                    rule_planets_stripped.append(r.strip())
                rule_planets_list.append(rule_planets_stripped)
        nextdatetimezonelonglat = NextDateTimeTimezoneLonglat()
        sign_planets_dict = defaultdict(list)

        for date_time_timezone_longlat in nextdatetimezonelonglat:
            # Example commandline1: /home/shrinivaasanka/Maitreya7_GitHub/martin-pe/maitreya7/releases/download/v7.1.1/maitreya-7.1.1/src/jyotish/maitreya_textclient --date="1851-06-25 00:00:00 5.5" --location="x 94:48:0 28:0:0" --planet-list
            # Example commandline2: /home/shrinivaasanka/Maitreya7_GitHub/martin-pe/maitreya7/releases/download/v7.1.1/maitreya-7.1.1/src/jyotish/maitreya_textclient  --date="2015-11-26 10:0:0 5.5"  --location=" x 80:0:0 13:0:0 " --planet-list
            #cmd="/media/shrinivaasanka/6944b01d-ff0d-43eb-8699-cca469511742/home/shrinivaasanka/Maitreya7_GitHub/martin-pe/maitreya7/releases/download/v7.1.1/maitreya-7.1.1/src/jyotish/maitreya_textclient "+ date_time_timezone_longlat + " 2>&1 > chartsummary.rulesearch"
            if MaitreyasDreams_Version == "8.0":
                #cmd="/home/shrinivaasanka/maitreya8-8.0/src/jyotish/maitreya8t "+ date_time_timezone_longlat + " 2>&1 > chartsummary.rulesearch"
                cmd = "/usr/bin/maitreya8t " + date_time_timezone_longlat + \
                    " 2>&1 > chartsummary.rulesearch"
            else:
                cmd = "/home/shrinivaasanka/Maitreya7_GitHub/martin-pe/maitreya7/releases/download/v7.1.1/maitreya-7.1.1/src/jyotish/maitreya_textclient " + \
                    date_time_timezone_longlat + " 2>&1 > chartsummary.rulesearch"
            print("cmd:",cmd)
            os.system(cmd)
            print("============================================")
            chart = open("chartsummary.rulesearch", "r")
            chart.readline()
            chart.readline()
            for row in chart:
                row_tokens = row.split()
                if row_tokens:
                    sign_planets_dict[row_tokens[3].strip()].append(
                        row_tokens[0].strip())
            print("sign_planets_dict=", sign_planets_dict)
            for rule_planets in rule_planets_list:
                for k, v in sign_planets_dict.items():
                    if (set(rule_planets[:-1]).issubset(set(v))):
                        print("{", date_time_timezone_longlat,
                              "} - There is a Class Association Rule match [", rule_planets[:-1], "] in sign ", k)
                    else:
                        print("{", date_time_timezone_longlat,
                              "} - There is no Class Association Rule match [", rule_planets[:-1], "] in sign ", k)
                sign_planets_dict = defaultdict(list)
    else:
        # SearchOption=2 - matches cross-cusp border patterns too
        if ClassAssociationRuleSearch:
            rules_file = open("./MinedClassAssociationRules.txt", "r")
        elif PlanetariumSearch:
            rules_file = open("./CelestialConfiguration.txt", "r")
        rule_planets_list = []
        nextdatetimezonelonglat = NextDateTimeTimezoneLonglat()
        print("nextdatetimezonelonglat:",list(nextdatetimezonelonglat))
        for rule in rules_file:
            ruletoks=rule.split(",")
            print("ruletoks:",ruletoks)
            if len(ruletoks) > 1:
                for date_time_timezone_longlat in nextdatetimezonelonglat:
                    print("date_time_timezone_longlat:",date_time_timezone_longlat)
                    # Example commandline1: /home/shrinivaasanka/Maitreya7_GitHub/martin-pe/maitreya7/releases/download/v7.1.1/maitreya-7.1.1/src/jyotish/maitreya_textclient --date="1851-06-25 00:00:00 5.5" --location="x 94:48:0 28:0:0" --planet-list
                    # Example commandline2: /home/shrinivaasanka/Maitreya7_GitHub/martin-pe/maitreya7/releases/download/v7.1.1/maitreya-7.1.1/src/jyotish/maitreya_textclient  --date="2015-11-26 10:0:0 5.5"  --location=" x 80:0:0 13:0:0 " --planet-list
                    if MaitreyasDreams_Version == "8.0":
                        #cmd="/media/ka_shrinivaasan/6944b01d-ff0d-43eb-8699-cca469511742/home/shrinivaasanka/maitreya8-8.0/src/jyotish/maitreya8t "+ date_time_timezone_longlat + " 2>&1 > chartsummary.rulesearch"
                        cmd = "/usr/bin/maitreya8t " + date_time_timezone_longlat + \
                            " 2>&1 > chartsummary.rulesearch"
                    else:
                        cmd = "/home/shrinivaasanka/Maitreya7_GitHub/martin-pe/maitreya7/releases/download/v7.1.1/maitreya-7.1.1/src/jyotish/maitreya_textclient " + \
                            date_time_timezone_longlat + " 2>&1 > chartsummary.rulesearch"
                    print("cmd:", cmd)
                    os.system(cmd)
                    print("============================================")
                    chart = open("chartsummary.rulesearch", "r")
                    sign_planets_dict = defaultdict(list)
                    chart.readline()
                    chart.readline()
                    encoded_chart = ""
                    for row in chart:
                        row_tokens = row.split()
                        print("chart row:", row_tokens)
                        if row_tokens:
                            sign_planets_dict[row_tokens[2].strip()].append(
                                row_tokens[0].strip())
                    print("signs_planets_dict:", sign_planets_dict)
                    encoded_chart += toString(sign_planets_dict["Ari"])
                    encoded_chart += " , Cusp , "
                    encoded_chart += toString(sign_planets_dict["Tau"])
                    encoded_chart += " , Cusp , "
                    encoded_chart += toString(sign_planets_dict["Gem"])
                    encoded_chart += " , Cusp , "
                    encoded_chart += toString(sign_planets_dict["Can"])
                    encoded_chart += " , Cusp , "
                    encoded_chart += toString(sign_planets_dict["Leo"])
                    encoded_chart += " , Cusp , "
                    encoded_chart += toString(sign_planets_dict["Vir"])
                    encoded_chart += " , Cusp , "
                    encoded_chart += toString(sign_planets_dict["Lib"])
                    encoded_chart += " , Cusp , "
                    encoded_chart += toString(sign_planets_dict["Sco"])
                    encoded_chart += " , Cusp , "
                    encoded_chart += toString(sign_planets_dict["Sag"])
                    encoded_chart += " , Cusp , "
                    encoded_chart += toString(sign_planets_dict["Cap"])
                    encoded_chart += " , Cusp , "
                    encoded_chart += toString(sign_planets_dict["Aqu"])
                    encoded_chart += " , Cusp , "
                    encoded_chart += toString(sign_planets_dict["Pis"])
                    print("Encoded chart to be searched:", encoded_chart)
                    pruned_rule = prune_rule(rule)
                    print("Rule to search:", pruned_rule)
                    if ClassAssociationRuleSearch:
                        patternindex = substring_find(encoded_chart, pruned_rule)
                    if PlanetariumSearch:
                        sign_planets_dict_chart=sign_planets_dict
                        patternindex=match_chart_and_rule(sign_planets_dict_chart, pruned_rule)
                    print("patternindex:", patternindex)
                    if ClassAssociationRuleSearch:
                        if patternindex != -1:
                          print("There is a Class Association Rule match for ",
                               date_time_timezone_longlat, " for pattern ", rule)
                        else:
                          print("There is No Class Association Rule match for ",
                               date_time_timezone_longlat, " for pattern ", rule)
                    if PlanetariumSearch:
                        if patternindex != -1:
                          print("There is a Planetarium Rule match for ",
                               date_time_timezone_longlat, " for pattern ", rule)
                          break
                        else:
                          print("There is No Planetarium Rule match for ",
                               date_time_timezone_longlat, " for pattern ", rule)
