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

from splearn import Spectral
from splearn.datasets.data_sample import SplearnArray
from graphviz import Source
from splearn.automaton import Automaton

def music_weighted_automaton(sample=None,splarray=None,rows=10,columns=10):
    sp = Spectral()
    sp.set_params(partial=True, lcolumns=columns, lrows=rows, smooth_method='trigram')
    print(sp)
    if sample is None:
        sample={'abad':2,'aaddb':3,'bb':5,'f':1,'':1}
    pref={}
    suff={}
    fact={}
    if splarray is None:
        splarray=SplearnArray([[0,1,0,3,-1],[0,0,3,3,1],[1,1,-1,-1,-1],[5,-1,-1,-1,-1],[-1,-1,-1,-1,-1]],rows,columns,sample,pref,suff,fact)
    print(splarray)
    sp.fit(splarray)
    print("Initial automaton:")
    print(sp.automaton.initial)
    print("Learnt automaton:")
    prediction1=sp.predict(splarray)
    print(prediction1)
    prediction2=sp.predict_proba(splarray)
    print(prediction2)
    print("Automaton Graph DOT file creation:")
    dot=sp.automaton.get_dot(threshold = 0.2, title = "MusicWeightedAutomaton.dot")
    src=Source(dot)
    src.render("MusicWeightedAutomaton.gv",view=True)

if __name__=="__main__":
    sample={'cddefffgb':10,'deffggaabc':9,'cccdddaaab':8,'gggabc':3,'cdddffff':5}
    pref={}
    suff={}
    fact={}
    splarray=SplearnArray([[-1,2,3,3,4,5,5,5,6,1],[3,4,5,5,6,6,0,0,1,2],[2,2,2,3,3,3,0,0,0,1],[-1,-1,-1,-1,6,6,6,0,1,2],[2,3,3,3,5,5,5,5,-1,-1]],10,10,sample,pref,suff,fact)
    music_weighted_automaton(sample,splarray,10,10)
