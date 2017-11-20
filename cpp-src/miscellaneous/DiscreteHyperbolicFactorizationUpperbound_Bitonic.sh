#!/bin/bash
g++ -g -o DiscreteHyperbolicFactorizationUpperbound_Bitonic DiscreteHyperbolicFactorizationUpperbound_Bitonic.cpp
./DiscreteHyperbolicFactorizationUpperbound_Bitonic $1 | grep mergedtiles | awk '{print $3}' 2>&1 > DiscreteHyperbolicFactorizationUpperbound_Bitonic.mergedtiles
./DiscreteHyperbolicFactorizationUpperbound_Bitonic $1 | grep coordinates | awk '{print $3}' 2>&1 > DiscreteHyperbolicFactorizationUpperbound_Bitonic.coordinates

#O(nlogn) Sequential
#python ../../python-src/DiscreteHyperbolicFactorizationUpperbound_Bitonic.py

#NC Parallel - on Spark Cloud
/home/shrinivaasanka/spark-2.1.0-bin-hadoop2.7/bin/spark-submit ../../python-src/DiscreteHyperbolicFactorizationUpperbound_Bitonic_Spark.py $1
