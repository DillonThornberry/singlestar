@echo off

:: Run the first script in the background (hidden)
start /min "" python server.py

:: Run the second script in a new command prompt window
start "Single Star" cmd /k python cli.py