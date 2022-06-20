@echo off
title Corporate Clash - Command-Line Launcher
set /p account="Account ID: "
set /p toon="Toon ID: "
set /p district="District: "

if not defined toon set "toon=-1"
if not defined district set "district=any"

python main.py -a %account% -t %toon% -d %district%
pause