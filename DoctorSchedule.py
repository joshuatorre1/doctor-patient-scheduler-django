import psycopg2

# Connect to database
connection = psycopg2.connect(host = "localhost",
                database = "DocKelan",
                user = "postgres",
                password = "LBYCPD2")

cursor = connection.cursor() # Pointer in the database

dict = '''create extension hstore'''

# Create dictionary
cursor.execute(dict)

# Define table
table = '''create table doctor_schedule(
   id serial primary key,
   doctor_id bigint,
   date date not null check(date >= current_date),
   start_time time not null,
   end_time time not null,
   break_start_time time not null,
   break_end_time time not null,
   consultation_time integer not null,
   schedule hstore,
   constraint fk_doctor
      foreign key(doctor_id) 
	  references doctor(id)
)'''

# Create table
cursor.execute(table)

# Close communication with the PostgreSQL database server
cursor.close()

# Commit the changes
connection.commit()

connection.close()
