create table adhoc.test_593843_customers(
row_id bigint   encode  AZ64,
startdateutc timestamp  encode  AZ64,
customer_name varchar(36)  encode  ZSTD,
paying_flag     bool encode  ZSTD)
diststyle       even 
sortkey         (row_id,startdateutc)
;
