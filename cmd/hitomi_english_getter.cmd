@echo off

rem Activate virtual environment
call D:\UDEMY_Workspace\GITHUB\python-hitomi-filters\.venv\Scripts\activate.bat

rem Run Python script with command-line argument
python D:\UDEMY_Workspace\GITHUB\python-hitomi-filters\src\english_filter.py %1

rem Deactivate virtual environment (optional)
deactivate
