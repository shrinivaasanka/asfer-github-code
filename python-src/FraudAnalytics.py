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
import csv
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn import metrics
import pandas

class FraudAnalytics(object):
    def __init__(self,csvfile):
        csvf=open(csvfile,'rb')
        self.csvreader=csv.reader(csvf,delimiter=' ',quotechar=']')

    def creditcard_fraud_analytics(self):
        transactions=[]
        rowcnt = 0
        for row in self.csvreader:
            if rowcnt > 0 and rowcnt < 500:
                modrow=[]
                for x in row[0].split(',')[:-1]:
                    modrow.append(float(x))
                transactions.append(modrow)
            rowcnt = rowcnt + 1
        transactions_np=np.asarray(transactions)
        print "transactions_np=",transactions_np
        kmeans_estimator=KMeans(init="k-means++",n_clusters=2,n_init=1)
        transactions_np_train=transactions_np[0:149]
        transactions_np_test=transactions_np[150:499]
        kmeansfit=kmeans_estimator.fit(transactions_np_train)
        print "kmeans estimator fit():",kmeansfit
        print "kmeans estimator fit() labels:",kmeans_estimator.labels_
        kmeanspred=kmeans_estimator.predict(transactions_np_test)
        print "kmeans estimator pred() labels:",kmeanspred
        #print "kmeans estimator inertia:",kmeans_estimator.inertia_
        print "kmeans estimator cluster centers:",kmeans_estimator.cluster_centers_
        #print  "metrics.homogeneity_score:",metrics.homogeneity_score(labels, estimator.labels_)
        #print  "metrics.completeness_score:",metrics.completeness_score(labels, estimator.labels_)
        #print  "metrics.v_measure_score:",metrics.v_measure_score(labels, estimator.labels_)
        #print  "metrics.adjusted_rand_score:",metrics.adjusted_rand_score(labels, estimator.labels_)
        #print  "metrics.adjusted_mutual_info_score:",metrics.adjusted_mutual_info_score(labels,  estimator.labels_, average_method='arithmetic')
        #print  "metrics.silhoutte_score:",metrics.silhouette_score(data, estimator.labels_, metric='euclidean', sample_size=sample_size)
        pca=PCA(n_components=2)
        transactions_np_train_pca=pca.fit_transform(transactions_np_train)
        print "transactions_np_train pca.singular_values_:",pca.singular_values_
        transactions_np_test_pca=pca.fit_transform(transactions_np_test)
        print "transactions_np_test pca.singular_values_:",pca.singular_values_
        kmeanspcafit=kmeans_estimator.fit(transactions_np_train_pca)
        print "kmeans estimator pca fit():",kmeanspcafit
        print "kmeans estimator pca fit() labels:",kmeans_estimator.labels_
        kmeanspred=kmeans_estimator.predict(transactions_np_test_pca)
        print "kmeans estimator pca pred() labels:",kmeanspred
        #print "kmeans estimator inertia:",kmeans_estimator.inertia_
        print "kmeans estimator pca cluster centers:",kmeans_estimator.cluster_centers_
        pandasDF=pandas.DataFrame(transactions_np)
        print "Pandas DataFrame Correlation Matrix for Dataset:",pandasDF.corr()

if __name__=="__main__":
    fa=FraudAnalytics("./creditcard.csv")
    fa.creditcard_fraud_analytics()

