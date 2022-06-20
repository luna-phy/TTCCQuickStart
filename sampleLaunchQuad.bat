@echo off
set /p "district=District: "
if not defined district set "district=any"
start python main.py -a 0 -t 1 -d %district%
start python main.py -a 1 -t 1 -d %district%
start python main.py -a 2 -t 1 -d %district%
start python main.py -a 3 -t 1 -d %district%