#!/bin/bash
g++ -g -o DiscreteHyperbolicFactorizationUpperbound_Bitonic DiscreteHyperbolicFactorizationUpperbound_Bitonic.cpp
./DiscreteHyperbolicFactorizationUpperbound_Bitonic | grep mergedtiles | awk '{print $3}' 2>&1 > DiscreteHyperbolicFactorizationUpperbound_Bitonic.mergedtiles
python ../../python-src/DiscreteHyperbolicFactorizationUpperbound_Bitonic.py
