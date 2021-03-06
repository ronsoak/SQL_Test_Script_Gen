#imports
import re 

#LOAD THE DDL
load_file = open('test_script_input.sql','r')
file_contents = load_file.readlines()

#GET THE TABLE NAME
table_head = file_contents[0:1]
table_name = re.search(r'\w+\.\w+',str(table_head), flags=re.U)
table_name = table_name.group(0)
table_name = str(table_name)

#FILE OUTPUT
sql_table_file =  table_name.replace(".","][")
filename = "[table_testing]["+sql_table_file+"].txt" 
filename = filename.lower()
sql_output = open(filename,"w")

#SCRIPT_GEN FUNCTION
def script_gen(a,b,c):
    if      b == 'NUMBER':
        sql_output.write("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n")
        sql_output.write("-- Testing for Column: "+a+"\n")
        sql_output.write("-- Column Type: Number \n")
        sql_output.write("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n")
        sql_output.write("-- Testing counts of column \n")
        sql_output.write("select count(*) as row_count, count(distinct("+a+")) as distinct_values from "+c+"; \n \n" )
        sql_output.write("-- Checking for nulls, are you expecting nulls? \n")
        sql_output.write("select count(*) from "+c+" where "+a+" is null; \n \n" )
        sql_output.write("-- Testing mins, avgs and max values \n")
        sql_output.write("select min("+a+"), avg("+a+"), max("+a+") from "+c+"; \n \n" )
        sql_output.write("-- Testing median, redshift doesn't like doing medians with other calcs \n")
        sql_output.write("select median("+a+") from "+c+"; \n \n" )
        sql_output.write("-- Testing 25% quartile, can be slow \n")
        sql_output.write("select percentile_cont(.25) within group (order by "+a+") as low_quartile from "+c+"; \n \n" )
        sql_output.write("-- Testing 50% quartile, can be slow\n")
        sql_output.write("select percentile_cont(.50) within group (order by "+a+") as mid_quartile from "+c+"; \n \n" )
        sql_output.write("-- Testing 75% quartile, can be slow\n")
        sql_output.write("select percentile_cont(.75) within group (order by "+a+") as high_quartile from "+c+"; \n \n" )
    elif    b == 'DATES':
        sql_output.write("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n")
        sql_output.write("-- Testing for Column: "+a+"\n")
        sql_output.write("-- Column Type: Date \n")
        sql_output.write("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n")
        sql_output.write("-- Testing counts of column \n")
        sql_output.write("select count(*) as row_count, count(distinct("+a+")) as distinct_values from "+c+"; \n \n" )
        sql_output.write("-- Checking for nulls, are you expecting nulls? \n")
        sql_output.write("select count(*) from "+c+" where "+a+" is null; \n \n" )
        sql_output.write("-- Checking for highs and lows, are they as you expected? \n")
        sql_output.write("select min("+a+"), max("+a+") from "+c+"; \n \n" )
        sql_output.write("-- Checking how many dates are in the future. \n")
        sql_output.write("select count(*) from "+c+" where "+a+" >sysdate; \n \n" )
        sql_output.write("-- Checking how many dates have a timestamp. \n")
        sql_output.write("select count(*) from "+c+" where substring("+a+",12,8)<> '00:00:00'; \n \n" )
    elif    b == 'STRING':
        sql_output.write("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n")
        sql_output.write("-- Testing for Column: "+a+"\n")
        sql_output.write("-- Column Type: String \n")
        sql_output.write("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n")
        sql_output.write("-- Testing counts of column \n")
        sql_output.write("select count(*) as row_count, count(distinct("+a+")) as distinct_values from "+c+"; \n \n" )
        sql_output.write("-- Checking for nulls, are you expecting nulls? \n")
        sql_output.write("select count(*) from "+c+" where "+a+" is null; \n \n" )
        sql_output.write("-- Top 10 values \n")
        sql_output.write("select "+a+", count(*) from "+c+" group by 1 order by 2 desc limit 10; \n \n" )
        sql_output.write("-- Check string lengths \n")
        sql_output.write("select min(len("+a+")) as min_length,max(len("+a+")) as max_length  from "+c+"; \n \n" )
    elif    b == 'BOOL':
        sql_output.write("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n")
        sql_output.write("-- Testing for Column: "+a+"\n")
        sql_output.write("-- Column Type: BOOL \n")
        sql_output.write("-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n")
        sql_output.write("-- Testing counts of column \n")
        sql_output.write("select count(*) as row_count, count(distinct("+a+")) as distinct_values from "+c+"; \n \n" )
        sql_output.write("-- Checking for nulls, are you expecting nulls? \n")
        sql_output.write("select count(*) from "+c+" where "+a+" is null; \n \n" )
        sql_output.write("-- Breakdown of boolean \n")
        sql_output.write("select "+a+", count(*) from "+c+" group by 1 order by 2 desc limit 10; \n \n" )
    elif    b == 'GEO':
        sql_output.write("Geospatial Data not currently supported. Suggest Something?  \n \n")
    else:
        sql_output.write("Column:"+a+"is not a know Datatype. Datatype passed was:"+b+"\n \n")

#RESTRICT TO APPLICABLE COLUMNS
valid_rows = list(filter(lambda x: re.search(r'\b(SMALLINT|INT2|INTEGER|INT|INT4|BIGINT|INT8|DECIMAL|NUMERIC|REAL|FLOAT4|DOUBLE|DOUBLE PRECISION|FLOAT8|FLOAT|BOOL|BOOLEAN|DATE|TIMESTAMP|TIMESTAMPTZ|CHAR|CHARACTER|NCHAR|BPCHAR|VARCHAR|CHARACTER VARYING|NVARCHAR|TEXT|GEOMETRY)',x,flags=re.IGNORECASE),file_contents))

#CREATE TEST SCRIPT
for table_line in valid_rows:
    table_line = str(table_line)
    col_name = table_line.split()[0:1]
    col_name = str(col_name)[1:-1]
    col_name = col_name.replace("'","")
    col_name = col_name.replace("(","")
    col_name = col_name.replace(")","")
    dat_type = table_line.split()[1:2]
    dat_type = str(dat_type)
    if (re.search(r'\b(CHAR|CHARACTER|NCHAR|BPCHAR|VARCHAR|CHARACTER VARYING|NVARCHAR|TEXT)',dat_type,flags=re.IGNORECASE)): col_type= 'STRING'
    elif (re.search(r'\b(SMALLINT|INT2|INTEGER|INT|INT4|BIGINT|INT8|DECIMAL|NUMERIC|REAL|FLOAT4|DOUBLE|DOUBLE PRECISION|FLOAT8|FLOAT)',dat_type,flags=re.IGNORECASE)): col_type= 'NUMBER'
    elif (re.search(r'\b(BOOL|BOOLEAN)',dat_type,flags=re.IGNORECASE)): col_type = 'BOOL'
    elif (re.search(r'\b(DATE|TIMESTAMP|TIMESTAMPTZ)',dat_type,flags=re.IGNORECASE)): col_type = 'DATES'
    elif (re.search(r'\b(GEOMETRY)',dat_type,flags=re.IGNORECASE)): col_type = 'GEO'
    else: col_type= 'BAD'
    col_type = str(col_type)
    script_gen(col_name,col_type,table_name)

#CLOSE THEN OPEN THE FILE
sql_output.close
