#!/bin/bash
g++ -g -o DiscreteHyperbolicFactorizationUpperbound_Bitonic DiscreteHyperbolicFactorizationUpperbound_Bitonic.cpp
./DiscreteHyperbolicFactorizationUpperbound_Bitonic | grep mergedtiles | awk '{print $3}' 2>&1 > DiscreteHyperbolicFactorizationUpperbound_Bitonic.mergedtiles
./DiscreteHyperbolicFactorizationUpperbound_Bitonic | grep coordinates | awk '{print $3}' 2>&1 > DiscreteHyperbolicFactorizationUpperbound_Bitonic.coordinates

#O(nlogn) Sequential
#python ../../python-src/DiscreteHyperbolicFactorizationUpperbound_Bitonic.py

#NC Parallel - on Spark Cloud
#/home/shrinivaasanka/www.us.apache.org/dist/spark/spark-1.5.2/spark-1.5.2/bin/spark-submit ../../python-src/DiscreteHyperbolicFactorizationUpperbound_Bitonic_Spark.py
#/home/shrinivaasanka/spark-2.1.0-bin-hadoop2.7/bin/spark-submit ../../python-src/DiscreteHyperbolicFactorizationUpperbound_Bitonic_Spark.py
