﻿# SQL Test Script Generator

*For Redshift Table Builds*

## What is this?
This is a python script that reads a table build written in Redshift Syntax and then for every column outputs a text file with some basic test scripts.

## Why?
Part of thorough testing in SQL is ensuring that each column you have pulled through is operating as expected, this script quickly creates the basic tests you should run, leaving you to write more personalised tests. 

## Pre-requisites 
- Latest version of Python 3.0+ and the ability to call the following libraries:
  - Pandas
  - Regex (re)
  - Warnings
  - System (sys)
  - Operating System (os)
- Tables built using Redshift, will not (currently) work on tables built in Oracle, TSQL,Postgresql,MySQL etc.....

## Instalation / Configuration
1. Download the git as a Zip, you only really need 'Launch_Me.bat' and 'Gen_Test_Script.py'
2. Place these two files in the folder of your choosing
3. Edit 'Launch_Me.bat' and go to line ten
4. Edit 'C:/<path to your python install>/python.exe' to be where your python.exe is installed
5. Edit 'c:/<path to this script>/Gen_Test_Script.py' to be where you've stored this script
6. Providing the above is all done properly, then your done.

## How to Use 
1. Double Click 'Launch_Me.bat'
2. A CMD window will pop up with some usage notes
3. Highlight your create table statement (see below for acceptable format) and copy it to your clipboard (CTRL+C/CMD+C)
4. Click on the open CMD window and hit enter
5. If you've configured it properly AND copied the right thing a text file should open up a text file with your test scripts.
6. A copy of that text file will be saved to the same folder you saved these scripts to
