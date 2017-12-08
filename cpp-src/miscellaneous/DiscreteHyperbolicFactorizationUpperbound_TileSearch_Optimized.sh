#!/bin/bash
g++ -g -o DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.cpp
./DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized $1

#NC Parallel - on Spark Cloud
datetime=`date`
/home/shrinivaasanka/spark-2.1.0-bin-hadoop2.7/bin/spark-submit /home/shrinivaasanka/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.py $1 2> /home/shrinivaasanka/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.log
