#IMPORTS
import pandas as pd
import re
import warnings
import sys
import os

#HOUSEKEEPING
warnings.filterwarnings("ignore", 'This pattern has match groups')

#LOAD FILES
#sql_load = pd.read_csv("ddl.sql",sep='\n',header=None, squeeze=1)
sql_load = pd.read_clipboard(sep='\n',header=None, squeeze=1)

#GET FIRST ROW OF DDL
sql_header = sql_load.iloc[0]

#VALIDATE THAT THIS IS A VALID DDL
sql_validate = re.search(r'^\w*\b',sql_header, flags=re.U)[0]
sql_validate = sql_validate.upper()
if sql_validate != 'CREATE':
    sys.exit("Not a valid DDL, must start with CREATE")
else: sql_table =  re.search(r'\w+\.\w+',sql_header, flags=re.U)[0] #if valid ddl then this gets the table name

#DICTIONARYS
red_types   = ("SMALLINT|INT2|INTEGER|INT|INT4|BIGINT|INT8|DECIMAL|NUMERIC|REAL|FLOAT4|DOUBLE|DOUBLE PRECISION|FLOAT8|FLOAT|BOOL|BOOLEAN|DATE|TIMESTAMP|TIMESTAMPTZ|CHAR|CHARACTER|NCHAR|BPCHAR|VARCHAR|CHARACTER VARYING|NVARCHAR|TEXT|GEOMETRY")
red_nums    = ("SMALLINT","INT2","INTEGER","INT","INT4","BIGINT","INT8","DECIMAL","NUMERIC","REAL","FLOAT4","DOUBLE","DOUBLE PRECISION","FLOAT8","FLOAT")
red_bool    = ("BOOL","BOOLEAN")
red_dates   = ("DATE","TIMESTAMP","TIMESTAMPTZ")
red_string  = ("CHAR","CHARACTER","NCHAR","BPCHAR","VARCHAR","CHARACTER VARYING","NVARCHAR","TEXT")
red_geo     = ("GEOMETRY")

#GET TABLE NAME
sql_header = sql_load.iloc[0]
sql_table =  re.search(r'\w+\.\w+',sql_header, flags=re.U)[0]

#FILE OUTPUT
sql_table_file = sql_table.replace(".","][")
filename = "[table_testing]["+sql_table_file+"].txt"
filename = filename.lower()
sql_output = open(filename,"w",)

#READ THE COL NAMES AND DATA TYPES
sql_load = pd.Series(sql_load)                                          #turn the SQL into a Series so we can convert to upper case
sql_load = sql_load.str.upper()                                         #convert all values to upper case
sql_load = sql_load.str.replace(r"\(\S*\)","")                          #finds data types with bracket numbers and strips them i.e varchar(45) -> varchar
sql_reduce = sql_load.loc[(sql_load.str.contains(fr'(\b({red_types})\b)', regex=True,case=False)==True)] #reduces the dataset to just the cols with data types in them
sql_reduce = sql_reduce.str.split(expand=True)                          #splitting the columns off
sql_cols = sql_reduce.loc[:,0:1]                                        #only need the first two columns
sql_cols = sql_cols.rename(columns = {0:'COL_NAME',1:'DATA_TYPE'})      #rename columns to col_name and data_type
sql_cols['COL_NAME'] = sql_cols['COL_NAME'].str.replace(',','')         #replace errant '
sql_cols['DATA_TYPE'] = sql_cols['DATA_TYPE'].str.replace(',','')       #replace errant '

#DEFINE FUNCTION FOR PRINTING
def col_func(a,b,c):
    if      b in red_nums:
        sql_output.write("select min("+a+"), avg("+a+"), max("+a+") from "+c+"; \n \n" )
        sql_output.write("select median("+a+") from "+c+"; \n \n" )

    elif    b in red_dates:
        sql_output.write("select min("+a+"), max("+a+") from "+c+"; \n \n" )

    elif    b in red_string:
        sql_output.write("select "+a+", count(*) from "+c+" group by 1 order by 2 desc limit 50; \n \n" )
        sql_output.write("select count(distinct("+a+")), count(*) from "+c+" limit 50; \n \n" )

    elif    b in red_bool:
        sql_output.write("select "+a+", count(*) from "+c+" group by 1 order by 2 desc limit 10; \n \n" )

    elif    b in red_geo:
        sql_output.write("Geospatial Data not currently supported. \n \n")
    else:
        sql_output.write("Column:"+a+"is not a know Datatype. Datatype passed was:"+b+"\n \n")

for index, row in sql_cols.iterrows():
    col_func(row['COL_NAME'], row['DATA_TYPE'], sql_table)

#CLOSE THEN OPEN THE FILE
sql_output.close
os.startfile(fr'{filename}')
