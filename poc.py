#IMPORTS
import pandas as pd
import re

#LOAD FILES
sql_load = pd.read_csv("C:\\Users\\CHRIS\\Documents\\Development\\SQL_Test_Script_Gen\\ddl.sql",sep='\n',header=None, squeeze=1)
data_types_redshift = pd.read_csv("C:\\Users\\CHRIS\\Documents\\Development\\SQL_Test_Script_Gen\\data_types_redshift.csv",sep='\n',header=None)


#GET TABLE NAME
sql_header = sql_load.iloc[0]
sql_table =  re.search('\S+\.\S+',sql_header, flags=re.U)[0]

#READ THE COL NAMES AND DATA TYPES
sql_load = pd.Series(sql_load)                                          #turn the SQL into a Series so we can conver to upper case
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
#print (sql_cols)

def col_func(a,b,c):
    if      b == 'BIGINT': 
        print("select min(",a,"), avg(",a,"), max(",a,") from",c,";" )
    elif    b == 'TIMESTAMP': 
        print("select min(",a,"), max(",a,") from",c,";" )
    elif    b == 'VARCHAR(36)': 
        print("select",a,", count(*) from",c,"group by 1 order by 2 desc limit 50;" )
        print("select count(distinct(",a,")), count(*) from",c,"group by 1 order by 2 desc limit 50;" )
    elif    b == 'BOOL': 
        print("select",a,", count(*) from",c,"group by 1 order by 1;" )

for index, row in sql_cols.iterrows():
    col_func(row['COL_NAME'], row['DATA_TYPE'], sql_table)

    