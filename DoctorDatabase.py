import psycopg2

# Connect to database
connection = psycopg2.connect(host = "localhost",
                database = "DocKelan",
                user = "postgres",
                password = "LBYCPD2")

cursor = connection.cursor() # Pointer in the database

# Define table
table = '''create table doctor(
   id serial primary key,
   last_name varchar(50) not null,
   first_name varchar(50) not null,
   middle_name varchar(50) not null,
   name_suffix varchar(4),
   username  varchar(50) unique not null,
   password text not null,
   birthday date not null,
   sex varchar(6) not null,
   region varchar(5) not null,
   cellphone_number bigint not null check(cellphone_number >= 639000000000 and cellphone_number <= 639999999999),
   telephone_number bigint check(telephone_number >= 63280000000 and telephone_number <= 63289999999),
   email varchar(50) unique not null,
   specialty varchar(50) not null,
   hospital varchar(50) not null,
   consultation_fee numeric(7, 2) not null check(consultation_fee >= 0),
   insurance_company varchar(50),
   license_number char(7) unique not null,
   description text,
   picture_file varchar(50),
   date_joined timestamp with time zone,
   last_login timestamp with time zone,
   last_logout timestamp with time zone,
   is_active boolean
)'''

# Create table
cursor.execute(table)

# Close communication with the PostgreSQL database server
cursor.close()

# Commit the changes
connection.commit()

connection.close()

