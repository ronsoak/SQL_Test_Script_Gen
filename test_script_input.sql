create table public.customer_table
(cust_id         bigint          encode  AZ64,
    startdateutc    timestamp       encode  AZ64,
    first_name      varchar(99)     encode  ZSTD,
    last_name       varchar(99)     encode  ZSTD,
    date_of_birth   date            encode  AZ64,
    address_line_1  varchar(300)    encode  ZSTD,
    address_line_2  varchar(300)    encode  ZSTD,
    address_line_3  varchar(300)    encode  ZSTD,
    region          varchar(300)    encode  ZSTD,
    city            varchar(300)    encode  ZSTD,
    postcode        int             encode  AZ64,
    paying_flag     bool            encode  ZSTD
)
diststyle       key
distkey         (cust_id)   
sortkey         (row_id,startdateutc)
;