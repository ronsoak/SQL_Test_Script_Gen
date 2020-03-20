ECHO OFF
COLOR de
REM This script exists to promt the user to copy the DDL into the text file
ECHO A blank text file will open, copy your DDL into this file, save and close it and hit enter in his window
ECHO > test_script_input.sql
test_script_input.sql
ECHO Waiting for you to save and close file
Echo Press Enter when ready
PAUSE 
ECHO Generating Test Script.... 
C:/<path to your python install>/python.exe c:/<path to this script>/Gen_Test_Script.py