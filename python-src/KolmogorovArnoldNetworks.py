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

from kan import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint

def kolmogorov_arnold_fit(function,n_var=2,x=[],y=[],trainnum=1000,testnum=1000):
    print("-------------------------------------------------------")
    model = KAN(width=[2,1,1], grid=3, k=3)
    dataset = create_dataset(function, n_var,train_num=trainnum,test_num=testnum)
    results=model.train(dataset, opt="LBFGS", steps=20)
    model.plot()
    print("KAN training and test datasets")
    pprint(results)
    plt.plot(results["train_loss"])
    plt.plot(results["test_loss"])
    plt.savefig("testlogs/KolmogorovArnoldNetworks.fit.jpeg")
    if len(x) > 0 and len(y) > 0:
        param_fit=fit_params(x,y,function)
        print("KAN parameter fit")
        pprint(param_fit)

if __name__=="__main__":
    function1 = lambda x: torch.exp(torch.sin(torch.pi*x[:,[0]]) + x[:,[1]]**2)
    function2 = lambda x: torch.exp(torch.sin(torch.pi*x[:]))
    x = torch.linspace(1,10,1)
    y = torch.linspace(1,10,1)
    kolmogorov_arnold_fit(function1,2)
    kolmogorov_arnold_fit(function2,2,x,y,trainnum=2000,testnum=2000)
