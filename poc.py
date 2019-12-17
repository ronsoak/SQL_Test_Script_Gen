#IMPORTS
import pandas as pd
import re

#LOAD FILES
#sql_load = pd.read_csv("C:\\Users\\CHRIS\\Documents\\Development\\SQL_Test_Script_Gen\\ddl.sql",sep='\n',header=None, squeeze=1)
sql_load = pd.read_clipboard(sep='\n',header=None, squeeze=1)

#GET TABLE NAME
sql_header = sql_load.iloc[0]
sql_table =  re.search(r'\S+\.\S+',sql_header, flags=re.U)[0]

#FILE OUTPUT
sql_table_file = sql_table.replace(".","_")
filename = sql_table_file+"_testing_script.txt"
sql_output = open(filename,"w",newline='\n')

#REDSHIFT DATA TYPES
red_nums    = ("SMALLINT","INT2","INTEGER","INT","INT4","BIGINT","INT8","DECIMAL","NUMERIC","REAL","FLOAT4","DOUBLE","DOUBLE PRECISION","FLOAT8","FLOAT")
red_bool    = ("BOOL","BOOLEAN")
red_dates   = ("DATE","TIMESTAMP","TIMESTAMPTZ")
red_string  = ("CHAR","CHARACTER","NCHAR","BPCHAR","VARCHAR","CHARACTER VARYING","NVARCHAR","TEXT")
red_geo     = ("GEOMETRY")

#READ THE COL NAMES AND DATA TYPES
sql_load = pd.Series(sql_load)                                          #turn the SQL into a Series so we can convert to upper case
sql_load = sql_load.str.upper()                                         #convert all values to upper case
sql_load = pd.DataFrame(sql_load)                                       #convert the series into a Data Frame
sql_load.columns = ['INPUT']                                            #rename the first column as 'INPUT'
sql_load_start = sql_load.loc[sql_load['INPUT']=='('].index.values[0]   #get the row that has the (
sql_load_end = sql_load.loc[sql_load['INPUT']==')'].index.values[0]     #get the row that has the )
sql_cols = sql_load.iloc[sql_load_start+1:sql_load_end]                 #limit the range down to just the rows between ( )
sql_cols.reset_index(drop=1, inplace=True)                              #resets the index
sql_cols = sql_cols['INPUT'].str.split(expand=True)                     #splitting the columns off
sql_cols = sql_cols.loc[:,0:1]                                          #reducing just down to cols 1 & 2, dropping 3&4
sql_cols = sql_cols.rename(columns = {0:'COL_NAME',1:'DATA_TYPE'})      #rename columns to col_name and data_type
sql_cols['DATA_TYPE'] = sql_cols['DATA_TYPE'].str.extract(r'(^\w*)')     #this will strip off bracketed numbers at the end varchar(45)->varchar

#DEFINE FUNCTION FOR PRINTING
def col_func(a,b,c):
    if      b in red_nums:
        sql_output.write("select min("+a+"), avg("+a+"), max("+a+") from "+c+"; \n" )

    elif    b in red_nums:
        sql_output.write("select "+a+", count(*) from "+c+" group by 1 order by 1; \n" )

    elif    b in red_dates:
        sql_output.write("select min("+a+"), max("+a+") from "+c+"; \n" )

    elif    b in red_string:
        sql_output.write("select "+a+", count(*) from "+c+" group by 1 order by 2 desc limit 50; \n" )
        sql_output.write("select count(distinct("+a+")), count(*) from "+c+" group by 1 order by 2 desc limit 50; \n" )

    elif    b in red_bool:
        sql_output.write("select "+a+", count(*) from "+c+" group by 1 order by 2 desc limit 10; \n" )

    else:
        sql_output.write("Column:"+a+"is not a know Datatype. Datatype passed was:"+b+"\n")

for index, row in sql_cols.iterrows():
    col_func(row['COL_NAME'], row['DATA_TYPE'], sql_table)

#close file
sql_output.close
#End Message
print(" Script Complete")
