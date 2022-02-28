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

import sys
import math
import random
from collections import defaultdict
import hashlib
from passlib.hash import sha256_crypt
from threading import BoundedSemaphore
import json
import random
import numpy as np
from scipy.sparse.linalg import lsqr
from scipy.sparse.linalg import lsmr
from numpy.linalg import solve
from sympy.combinatorics.partitions import Partition
from sympy.combinatorics.partitions import random_integer_partition
from sympy.functions.combinatorial.numbers import nT
import subprocess
import operator
import cvxopt
from cvxopt.glpk import ilp
import cv2
from DigitalWatermarking import watermark_image
m = 0
Tower = [1, 2, 3, 4]
Tower[0] = []
Tower[1] = []
Tower[2] = []
Tower[3] = []

Voting_Machine1_dict = defaultdict(list)
Voting_Machine2_dict = defaultdict(list)
Voting_Machine3_dict = defaultdict(list)

Voted = []
evm_histograms = []
maxvoters = 1


def complementary_set_partition(partition, depth=1):
    maxlen = -1
    for part in partition:
        if maxlen < len(part):
            maxlen = len(part)
    equidepthlen = maxlen + depth
    complementarypartition = []
    equidepthpartition = []
    for part in partition:
        complementarypartition.append(np.zeros(equidepthlen - len(part)))
        equidepthpartition.append(
            list(part) + np.zeros(equidepthlen - len(part)).tolist())
    print("complementary partition of ", partition, ":", complementarypartition)
    print('equidepth partition:', equidepthpartition)
    return complementarypartition


def single_bin_sorted_LIFO_histogram_ToH(n, Neuro_Crypto_ProofOfWork=True):
    # Towers of Hanoi NP-Hard Neuro Cryptocurrency Proof-of-work - Towers of Hanoi are sorted LIFO single bucket histograms
    # Two recursions for x to z and z to y - following is a 3 towers recursive implementation printing the histogram towers
    # simpler recursion has been commented
    # global m
    # if n > 0:
    #	m=m+1
    #	print("Move " + str(m) + ": top disk of tower x to top disk of tower y through intermediary tower z")
    #	single_bin_sorted_LIFO_histogram_ToH(n-1,x,z,y)
    #	single_bin_sorted_LIFO_histogram_ToH(n-1,z,y,x)
    global Tower
    n = int(math.log(int(n),2))
    for x in reversed(range(n)):
        Tower[1].append(x)
    print("Tower:", Tower)
    print_Towers_of_Hanoi(n, 1, 2, 3)
    if Neuro_Crypto_ProofOfWork:
        imgtemplate = cv2.imread("testlogs/NeuroCurrencyTemplate.jpg")
        imgwatermark = cv2.imread("testlogs/NeuroCurrencyWatermark.jpg")
        cv2.putText(imgtemplate, str(math.pow(2,n)), (320, 200),
                    cv2.FONT_HERSHEY_TRIPLEX, 3.0, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(imgtemplate, sha256_crypt.hash(bin(n)), (5, 300),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imwrite("testlogs/NeuroCryptoCurrency.jpg", imgtemplate)
        imgcurrency = cv2.imread("testlogs/NeuroCryptoCurrency.jpg")
        watermark_image("testlogs/NeuroCryptoCurrency.jpg",
                        "testlogs/NeuroCurrencyWatermark.jpg")


def print_Towers_of_Hanoi(n, x, y, z):
    from scipy.stats import wasserstein_distance
    global Tower
    global m
    if n > 0:
        m += 1
        print_Towers_of_Hanoi(n-1, x, z, y)
        disk = Tower[x].pop()
        Tower[y].append(disk)
        print("======================= Move " + str(m) +
              " ================================================")
        print("Tower 1:", Tower[1])
        print("Tower 2:", Tower[2])
        print("Tower 3:", Tower[3])
        emd12 = 0
        emd23 = 0
        emd13 = 0
        if len(Tower[1]) > 0 and len(Tower[2]) > 0:
            emd12 = wasserstein_distance(Tower[1], Tower[2])
        if len(Tower[1]) > 0 and len(Tower[3]) > 0:
            emd13 = wasserstein_distance(Tower[1], Tower[3])
        if len(Tower[2]) > 0 and len(Tower[3]) > 0:
            emd23 = wasserstein_distance(Tower[2], Tower[3])
        print("Pairwise ToH Earth Mover Distance Triple:", (emd12, emd13, emd23))
        print_Towers_of_Hanoi(n-1, z, y, x)


def setpartition_to_tilecover(histogram_partition=None, number_to_factorize=1, solution="ILP", Neuro_Crypto_ProofOfWork=False):
    squaretiles_cover = []
    from complement import toint
    from sympy.solvers.diophantine.diophantine import diop_general_sum_of_squares
    from sympy.abc import a, b, c, d, e, f
    if not Neuro_Crypto_ProofOfWork:
        for hp in histogram_partition:
            tiles = diop_general_sum_of_squares(
                a**2 + b**2 + c**2 + d**2 - toint(hp))
            print(("square tiles for partition ", hp, ":", tiles))
            for t in list(tiles)[0]:
                squaretiles_cover.append((t, t*t))
        print(("Lagrange Four Square Tiles Cover reduction of Set Partition for ", number_to_factorize, ",",
               histogram_partition, ":", squaretiles_cover))
        subprocess.call(["/media/ksrinivasan/84f7d6fd-3d43-4215-8dcc-52b5fe1bffc6/home/ksrinivasan/spark-3.0.1-bin-hadoop3.2/bin/spark-submit",
                        "DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.py", number_to_factorize, "1", "False"], shell=False)
    else:
        histogram_partition = random_integer_partition(
            int(number_to_factorize))
        for hp in histogram_partition:
            tiles = diop_general_sum_of_squares(
                a**2 + b**2 + c**2 + d**2 - toint(hp))
            print(("square tiles for partition ", hp, ":", tiles))
            for t in list(tiles)[0]:
                squaretiles_cover.append((t, t*t))
        print(("Neuro Cryptocurrency Proof of Work - Rectangular Area (=Value of Neuro cryptocurrency mined) Factorized and Pair of Money Changing Frobenius Diophantines solved by ILP for factors of integer :", number_to_factorize))
        subprocess.call(["/media/ksrinivasan/84f7d6fd-3d43-4215-8dcc-52b5fe1bffc6/home/ksrinivasan/spark-3.0.1-bin-hadoop3.2/bin/spark-submit",
                        "DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.py", number_to_factorize, "1", "False"], shell=False)
    factorsfile = open(
        "DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.factors")
    factors = json.load(factorsfile)
    number_to_factorize = 0
    factorslist = []
    for k, v in list(factors.items()):
        number_to_factorize = k
        factorslist = v
    # c1*x1 + c2*x2 + ... + ck*xk + ... + cn*xn = p
    # d1*x1 + d2*x2 + ... + dk*xk + ... + dn*xn = q
    # solve AX=B:
    # X = [c1 c2 ... cn] - unknowns (boolean include or exclude)
    # A = [[x1 x2 ... xn]  - knowns (sides of the square tiles)
    #     permutation_of[x1 x2 ... xn]]
    # B = [p q] - factors
    equationsA = []
    equationsB = []
    equation = []
    init_guess = []
    for n in range(len(squaretiles_cover)):
        init_guess.append(0.00000000001)
    initial_guess = np.array(init_guess)
    for sqtc in squaretiles_cover:
        equation.append(sqtc[0])
    equationsA.append(equation)
    permutedequation = np.random.permutation(equation)
    equationsA.append(permutedequation)
    print(("factorslist:", factorslist))
    if len(factorslist) > 0:
        for factor in factorslist:
            if factor != 1 and factor != number_to_factorize:
                equationsB.append(factor)
                equationsB.append(int(number_to_factorize)/factor)
                break
    a = np.array(equationsA).astype(float)
    b = np.array(equationsB[:2]).astype(float)
    y = []
    for n in equationsA[0]:
        y.append(1)
    print(("Diophantine A =", a))
    print(("Diophantine B =", b))
    if solution == "ILP":
        C = cvxopt.matrix(y, tc='d')
        cnt = 0
        h = []
        g = []
        for v in equationsA[0]:
            row = np.zeros(len(equationsA[0])).tolist()
            row[cnt] = 1
            g.append(row)
            h.append(0)
            cnt += 1
        H = cvxopt.matrix(h, tc='d')
        G = cvxopt.matrix(g, tc='d')
        B = cvxopt.matrix(b, tc='d')
        A = cvxopt.matrix(a, tc='d')
        I = set(range(len(y)))
        print("C=", C)
        print("G=", G)
        print("H=", H)
        print("A=", A)
        print("B=", B)
        print("I=", I)
        (status, x) = cvxopt.glpk.ilp(C, -G.T, -H, A, B, I=I)
        print(("status = ", status, " : x = ", x))
        roundedx = x
        if x is None:
            return []
        if Neuro_Crypto_ProofOfWork:
            imgtemplate = cv2.imread("testlogs/NeuroCurrencyTemplate.jpg")
            imgwatermark = cv2.imread("testlogs/NeuroCurrencyWatermark.jpg")
            factorsuniqueid = "-".join(map(str, factorslist))
            cv2.putText(imgtemplate, number_to_factorize, (320, 200),
                        cv2.FONT_HERSHEY_TRIPLEX, 3.0, (255, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(imgtemplate, sha256_crypt.hash(factorsuniqueid), (5, 300),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imwrite("testlogs/NeuroCryptoCurrency.jpg", imgtemplate)
            imgcurrency = cv2.imread("testlogs/NeuroCryptoCurrency.jpg")
            watermark_image("testlogs/NeuroCryptoCurrency.jpg",
                            "testlogs/NeuroCurrencyWatermark.jpg")
    else:
        #x = lsqr(a,b,atol=0,btol=0,conlim=0,show=True)
        x = lsmr(a, b, atol=0, btol=0, conlim=0, show=True, x0=initial_guess)
        #x = solve(a,b)
        print(("x=", x))
        roundedx = []
        for t in x[0]:
            roundedx.append(abs(round(t)))
        print(("Randomized rounding:", roundedx))
    cnt = 0
    side1 = 0
    side2 = 0
    side1str = ""
    side2str = ""
    for t in roundedx:
        print(("t=", t, "; cnt=", cnt))
        side1 += (t*equationsA[0][cnt])
        side1str += str(t) + "*" + str(equationsA[0][cnt]) + "+"
        side2 += (t*equationsA[1][cnt])
        side2str += str(t) + "*" + str(equationsA[1][cnt]) + "+"
        cnt += 1
    print(("(Approximate if least squares is invoked) Rectangle periphery - ",
          side1str, " - side1:", side1))
    print(("(Approximate if least squares is invoked) Rectangle periphery - ",
          side2str, " - side2:", side2))
    return squaretiles_cover


def tocluster(histogram, datasource):
    cluster = []
    if datasource == "Text":
        for tupl in histogram:
            for x in tupl[1][0]:
                cluster.append(tupl[0])
    if datasource == "Dict":
        print(("histogram:", histogram))
        for k, v in list(histogram.items()):
            for x in v:
                cluster.append(k)
    print(("cluster:", cluster))
    return cluster


def electronic_voting_machine(Voting_Machine_dict, unique_id, voted_for, Streaming_Analytics_Bertrand=False, onetimepassword=None):
    semaphorelock = BoundedSemaphore(value=maxvoters)
    semaphorelock.acquire()
    uniqueidf = open(unique_id, "rb")
    publicuniqueidhex = ""
    publicuniqueid = uniqueidf.read()
    h = hashlib.new("ripemd160")
    h.update(publicuniqueid)
    publicuniqueidhex = h.hexdigest()
    if publicuniqueid not in Voted:
        if onetimepassword is not None:
            publicuniqueidhex += ":"
            publicuniqueidhex += onetimepassword
        print(("publicuniqueidhex:", publicuniqueidhex))
        if len(Voted) > 1 and len(Voting_Machine_dict[voted_for]) > 1:
            try:
                Voting_Machine_dict[voted_for].insert(sha256_crypt.hash(
                    publicuniqueidhex), random.randint(0, len(Voting_Machine_dict[voted_for])))
                Voted.insert(publicuniqueid, random.randint(0, len(Voted)))
            except:
                print("Encoding exception")
        else:
            Voting_Machine_dict[voted_for].append(sha256_crypt.hash(
                publicuniqueidhex))
            Voted.append(publicuniqueid)
        print(("Voting_Machine_dict:", Voting_Machine_dict))
    else:
        print("Voter Already Voted")
    if Streaming_Analytics_Bertrand == True:
        sortedEVM = sorted(list(Voting_Machine_dict.items()),
                           key=operator.itemgetter(1), reverse=True)
        print(("sortedEVM:", sortedEVM))
        if len(sortedEVM) > 1:
            p = len(sortedEVM[0][1])
            q = len(sortedEVM[1][1])
            tempp = p
            p = max(p, q)
            q = min(tempp, q)
            print(("Probability of ", sortedEVM[0][0], " winning over nearest rival ", sortedEVM[1][0], ":", abs(
                float(p-q)/float(p+q))))
    semaphorelock.release()


def electronic_voting_analytics(Voting_Machine_dicts):
    import Streaming_AbstractGenerator
    from scipy.stats import wasserstein_distance
    from sklearn.metrics.cluster import adjusted_rand_score
    from sklearn.metrics import adjusted_mutual_info_score
    #from cv2 import CalcEMD2
    #from cv2 import compareHist

    evmsf = open("testlogs/Streaming_SetPartitionAnalytics.EVMs.json", "w")
    evmid = 0
    for evm in Voting_Machine_dicts:
        evm_histogram = {}
        for k, v in list(evm.items()):
            # Bucket length is the counter
            evm_histogram[k] = len(v)
        # if len(evm_histogram) > 0:
        evm_histograms.append(evm_histogram)
        evmid += 1
    json.dump(evm_histograms, evmsf)
    evmsf.close()
    evmstream = Streaming_AbstractGenerator.StreamAbsGen(
        "DictionaryHistogramPartition", "testlogs/Streaming_SetPartitionAnalytics.EVMs.json")
    prev = {}
    for n1 in evmstream:
        try:
            if len(list(n1.values())) == len(list(prev.values())):
                ari = adjusted_rand_score(
                    list(n1.values()), list(prev.values()))
                print(("Adjusted Rand Index between histograms ", list(n1.values(
                )), " and ", list(prev.values()), ":", ari))
                ami = adjusted_mutual_info_score(
                    list(n1.values()), list(prev.values()))
                print(("Adjusted Mutual Information Index between histograms ", list(n1.values(
                )), " and ", list(prev.values()), ":", ami))
            emd = 0
            if len(list(n1.values())) > 0 and len(list(prev.values())) > 0:
                emd = wasserstein_distance(
                    list(n1.values()), list(prev.values()))
            print(("Earth Mover Distance between histograms ", list(n1.values(
            )), " and ", list(prev.values()), " - Wasserstein :", emd))
            prev = n1
        except Exception as e:
            print((
                "Exception - EMD error or Shape mismatch in sklearn computation of ARI and AMI:", e))
            continue


def adjusted_rand_index():
    import Streaming_AbstractGenerator
    from sklearn.metrics.cluster import adjusted_rand_score
    from sklearn.metrics import adjusted_mutual_info_score
    # The text file is updated by a stream of data
    # inputf=Streaming_AbstractGenerator.StreamAbsGen("USBWWAN_stream","USBWWAN")
    # inputf=Streaming_AbstractGenerator.StreamAbsGen("file","StreamingData.txt")
    # inputf=Streaming_AbstractGenerator.StreamAbsGen("Spark_Parquet","Spark_Streaming")
    # inputf=Streaming_AbstractGenerator.StreamAbsGen("AsFer_Encoded_Strings","NeuronRain")
    # inputf=Streaming_AbstractGenerator.StreamAbsGen("Socket_Streaming","localhost")
    # inputf1 = Streaming_AbstractGenerator.StreamAbsGen("TextHistogramPartition", [
    inputf1 = Streaming_AbstractGenerator.StreamAbsGen("TextHistogramPartition", [
                                                       "/var/log/kern.log", "/var/log/syslog", "/var/log/dmesg", "/var/log/ufw.log", "/var/log/kern.log"])
    histograms = []
    for p in inputf1:
        histograms.append(p)
    ari = adjusted_rand_score(tocluster(histograms[0], "Text")[
                              :20000], tocluster(histograms[1], "Text")[:20000])
    print(("Adjusted Rand Index of first two histogram set partitions(truncated):", ari))
    prev = 0
    for n in range(1, len(histograms)):
        truncatedlen = int(min(len(histograms[prev]), len(histograms[n]))*0.9)
        ari = adjusted_rand_score(tocluster(histograms[prev], "Text")[
                                  :truncatedlen], tocluster(histograms[n], "Text")[:truncatedlen])
        print(("Adjusted Rand Index(truncated):", ari))
        ami = adjusted_mutual_info_score(tocluster(histograms[prev], "Text")[
                                         :truncatedlen], tocluster(histograms[n], "Text")[:truncatedlen])
        print(("Adjusted Mutual Info Index(truncated):", ami))
        prev = n
    #################################################################
    histograms = []
    inputf2 = Streaming_AbstractGenerator.StreamAbsGen(
        "DictionaryHistogramPartition", "Streaming_SetPartitionAnalytics.txt")
    for p in inputf2:
        histograms.append(p)
    prev = 0
    print(("histograms:", histograms))
    for n in range(1, len(histograms)):
        truncatedlen = int(min(len(histograms[prev]), len(histograms[n]))*0.9)
        ari = adjusted_rand_score(tocluster(histograms[prev], "Dict")[
                                  :truncatedlen], tocluster(histograms[n], "Dict")[:truncatedlen])
        print(("Adjusted Rand Index (truncated):", ari))
        ami = adjusted_mutual_info_score(tocluster(histograms[prev], "Dict")[
                                         :truncatedlen], tocluster(histograms[n], "Dict")[:truncatedlen])
        print(("Adjusted Mutual Info Index (truncated):", ami))
        prev = n


if __name__ == "__main__":
    # ari=adjusted_rand_index()
    set1 = set(range(random.randint(1, int(sys.argv[1]))))
    number_of_partitions = nT(len(set1))
    processes_partitions = Partition(set1)
    randp = processes_partitions + random.randint(1, number_of_partitions)
    print(("Random Partition:", randp))
    complementary_set_partition(randp, 5)
    histogram = list(map(len, randp))
    setpartition_to_tilecover(histogram, str(sum(histogram)))
    candidates = ["NOTA", "CandidateA", "CandidateB"]
    idcontexts = ["testlogs/Streaming_SetPartitionAnalytics_EVM/PublicUniqueEVM_ID1.txt",
                  "testlogs/Streaming_SetPartitionAnalytics_EVM/PublicUniqueEVM_ID2.jpg", "testlogs/Streaming_SetPartitionAnalytics_EVM/PublicUniqueEVM_ID1.pdf"]
    voteridx = 0
    for voter in range(30):
        print("=============================")
        print("Electronic Voting Machine: 1")
        print("=============================")
        electronic_voting_machine(Voting_Machine1_dict, idcontexts[voteridx % len(idcontexts)],
                                  candidates[int(random.random()*100) % len(candidates)], Streaming_Analytics_Bertrand=True, onetimepassword="ff20a894-a2c4-4002-ac39-93dd53ea302f:100")
        print("=============================")
        print("Electronic Voting Machine: 2")
        print("=============================")
        electronic_voting_machine(Voting_Machine2_dict, idcontexts[voteridx*2 % len(idcontexts)],
                                  candidates[int(random.random()*100) % len(candidates)], Streaming_Analytics_Bertrand=True, onetimepassword="ff20a894-a3c4-4002-ac39-93d153ea3020:100")
        print("=============================")
        print("Electronic Voting Machine: 3")
        print("=============================")
        electronic_voting_machine(Voting_Machine3_dict, idcontexts[voteridx*3 % len(idcontexts)],
                                  candidates[int(random.random()*100) % len(candidates)], Streaming_Analytics_Bertrand=True, onetimepassword="ff20a894-a2c4-4102-ac39-93d353ea3020:100")
        voteridx += 1
    #setpartition_to_tilecover(None, sys.argv[1], solution="ILP",Neuro_Crypto_ProofOfWork=True)
    single_bin_sorted_LIFO_histogram_ToH(
        "1024", Neuro_Crypto_ProofOfWork=True)
    electronic_voting_analytics(
        [Voting_Machine1_dict, Voting_Machine2_dict, Voting_Machine3_dict])
