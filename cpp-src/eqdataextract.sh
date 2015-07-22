#!/bin/sh
grep "headers=\"t2" *html | cut -d ">" -f 2 | cut -d "<" -f 1 2>&1 > earthquakesFrom1900with8plusmag.txt 
