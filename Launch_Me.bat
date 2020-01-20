ECHO OFF
COLOR de
REM This script exists to promt the user to copy the DDL and to launch the script.
ECHO Using CTRL+C Copy JUST your table create script, don't include any other SQL.
ECHO This is only for FULL table build statements, will not work on 'Create Table as....' 
ECHO i.e you need to have defined your columns AND DATA TYPES
ECHO Once you have copied your table script, press Enter.
PAUSE
ECHO Generating Test Script.... 
C:/<path to your python install>/Python38-32/python.exe c:/<path to this script>/Gen_Test_Script.py