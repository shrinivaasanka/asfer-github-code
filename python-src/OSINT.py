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

def osint(urls,ports):
    from osint import QBDns,QBScan,QBExtract,QBTraceRoute,QBWhois
    targets = QBDns().convert_to_ips(urls)
    targets = QBScan().run(targets,ports)
    targets = QBExtract().run(targets,function="text")
    print(targets)
    #targets = QBDns().convert_to_ips(urls)
    #targets = QBTraceRoute().run(targets)
    #print(targets)
    #targets = QBDns().convert_to_ips(urls)
    #targets = QBWhois.run(targets)
    #print(targets)

if __name__=="__main__":
    osint(["www.google.com"],[80,443])
