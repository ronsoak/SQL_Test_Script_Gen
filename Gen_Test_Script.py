#IMPORTS
import pandas as pd                                                         #Pandas Library: Used for Series, Data Frames, and a few string manipulations
import re                                                                   #Regex Library: Primarily used for re.search functionality
import warnings                                                             #Warnings Library: Used to surpress a messy regex grouping error
import sys                                                                  #System Library: Used to hard exit proc if it's not a valid DDL
import os                                                                   #Operating System Library: Used to open up the file thats been written

#SUPRESS WARNINGS
warnings.filterwarnings("ignore", 'This pattern has match groups')          #ignore regex warning caused by looking inside red_types

#INPUT DATA
sql_load = pd.read_clipboard(sep='\n',header=None, squeeze=1)               #Pulling DDL off of clipboard

#GET FIRST ROW OF DDL
sql_header = sql_load.iloc[0]                                               #The first line of ddl has the tablename or will tell if the data is invalid

#VALIDATE THAT THIS IS A VALID DDL
sql_validate = re.search(r'^\w*\b',sql_header, flags=re.U)[0]               #Whats the first word in the first line, should be CREATE
sql_validate = sql_validate.upper()                                         #Convert the first word to uppercase
if sql_validate != 'CREATE':                                                #If the first word is not CREATE kill the proc
    filename = "script_terminated_with_error.txt"
    error_output = open(filename,"w")
    error_output.write("If you are reading this message, the python script has terminated. \n")   
    error_output.write("Reason? The first word on the clipboard wasn't CREATE.\n")
    error_output.write("This means you have not copied a valid Redshift SQL Table Create Statement to your clipboard. \n")
    error_output.write("For more help refer to: https://github.com/ronsoak/SQL_Test_Script_Gen.\n")
    error_output.close
    os.startfile(fr'{filename}')
    sys.exit("Not a valid DDL, must start with CREATE")
else: sql_table =  re.search(r'\w+\.\w+',sql_header, flags=re.U)[0]         #If valid ddl then this gets the table name

#DICTIONARYS
red_types   = ("SMALLINT|INT2|INTEGER|INT|INT4|BIGINT|INT8|DECIMAL|NUMERIC|REAL|FLOAT4|DOUBLE|DOUBLE PRECISION|FLOAT8|FLOAT|BOOL|BOOLEAN|DATE|TIMESTAMP|TIMESTAMPTZ|CHAR|CHARACTER|NCHAR|BPCHAR|VARCHAR|CHARACTER VARYING|NVARCHAR|TEXT|GEOMETRY")
red_nums    = ("SMALLINT","INT2","INTEGER","INT","INT4","BIGINT","INT8","DECIMAL","NUMERIC","REAL","FLOAT4","DOUBLE","DOUBLE PRECISION","FLOAT8","FLOAT")
red_bool    = ("BOOL","BOOLEAN")
red_dates   = ("DATE","TIMESTAMP","TIMESTAMPTZ")
red_string  = ("CHAR","CHARACTER","NCHAR","BPCHAR","VARCHAR","CHARACTER VARYING","NVARCHAR","TEXT")
red_geo     = ("GEOMETRY")

#GET TABLE NAME
sql_table =  re.search(r'\w+\.\w+',sql_header, flags=re.U)[0]               #Finds the tablename in the format schema.table

#FILE OUTPUT
sql_table_file = sql_table.replace(".","][")                                #Can't have a . in a file name ie schema.table so have replaced it with ][
filename = "[table_testing]["+sql_table_file+"].txt"                        #File name should look like [table_testing][schema][tablename].txt
filename = filename.lower()                                                 #Make the whole thing lower case, I just like it to be consistent
sql_output = open(filename,"w")                                            #Create a new file in the directory

#READ THE COL NAMES AND DATA TYPES
sql_load = pd.Series(sql_load)                                              #Turn the SQL into a Series so we can convert to upper case
sql_load = sql_load.str.upper()                                             #Convert all values to upper case
sql_load = sql_load.str.replace(r"\(\S*\)","")                              #Finds data types with bracket numbers and strips them i.e varchar(45) -> varchar
sql_reduce = sql_load.loc[(sql_load.str.contains(fr'(\b({red_types})\b)', regex=True,case=False)==True)] #Reduces the dataset to just the cols with data types in them
sql_reduce = sql_reduce.str.split(expand=True)                              #Splitting the columns off
sql_cols = sql_reduce.loc[:,0:1]                                            #Only need the first two columns
sql_cols = sql_cols.rename(columns = {0:'COL_NAME',1:'DATA_TYPE'})          #Rename columns to col_name and data_type
sql_cols['COL_NAME'] = sql_cols['COL_NAME'].str.replace(',','')             #Replace errant ' in column name
sql_cols['DATA_TYPE'] = sql_cols['DATA_TYPE'].str.replace(',','')           #Replace errant ' in data type

#DEFINE FUNCTION FOR PRINTING
def col_func(a,b,c):
    if      b in red_nums:                                                  #For number data types
        sql_output.write("select min("+a+"), avg("+a+"), max("+a+") from "+c+"; \n \n" )
        sql_output.write("select median("+a+") from "+c+"; \n \n" )

    elif    b in red_dates:                                                 #For date data types
        sql_output.write("select min("+a+"), max("+a+") from "+c+"; \n \n" )

    elif    b in red_string:                                                #For string data types
        sql_output.write("select "+a+", count(*) from "+c+" group by 1 order by 2 desc limit 50; \n \n" )
        sql_output.write("select count(distinct("+a+")), count(*) from "+c+" limit 50; \n \n" )

    elif    b in red_bool:                                                  #For boolean data types
        sql_output.write("select "+a+", count(*) from "+c+" group by 1 order by 2 desc limit 10; \n \n" )

    elif    b in red_geo:                                                   #For Geo data types
        sql_output.write("Geospatial Data not currently supported. \n \n")
    else:                                                                   #For Data Types that can't be detected
        sql_output.write("Column:"+a+"is not a know Datatype. Datatype passed was:"+b+"\n \n")

for index, row in sql_cols.iterrows():                                      #Run through the data set
    col_func(row['COL_NAME'], row['DATA_TYPE'], sql_table)                  #Pass into the custom function a=Col_name, b=Data_type, C=Table Name

#CLOSE THEN OPEN THE FILE
sql_output.close                                                            #Close off the open file, i.e stop writing
os.startfile(fr'{filename}')                                                #Open up the file for the user to see
