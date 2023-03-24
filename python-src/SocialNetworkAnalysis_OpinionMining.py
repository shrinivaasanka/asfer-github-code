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

from GoogleNews import GoogleNews
from newspaper import Article
import pandas

def opinion_mining(query,fromdate,todate,maxpages=2):
    gn=GoogleNews(start=fromdate,end=todate)
    gn.search(query)
    opinion=[]
    for page in range(maxpages):
        gn.getpage(page)
        results=gn.result()
        df=pandas.DataFrame(results)
        for index in df.index:
            newsjson={}
            try:
                article=Article(df['link'][index])
                article.download()
                article.parse()
                article.nlp()
                newsjson['Date']=df['date'][index]
                newsjson['Media']=df['media'][index]
                newsjson['Title']=article.title
                newsjson['Article']=article.text
                print(article.text)
                newsjson['Summary']=article.summary
                opinion.append(newsjson)
            except Exception as ex:
                print(ex)
    opiniondf=pandas.DataFrame(opinion)
    print(opiniondf)
    return opiniondf

if __name__=="__main__":
    opinion_mining("Chennai Metropolitan Area Expansion","01/10/2022","01/03/2023")


