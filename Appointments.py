import psycopg2

# Connect to database
connection = psycopg2.connect(host = "localhost",
                database = "DocKelan",
                user = "postgres",
                password = "LBYCPD2")

cursor = connection.cursor() # Pointer in the database

# Define table
table = '''create table appointment(
   id serial primary key,
   patient_id bigint,
   doctor_id bigint,
   date date not null,
   start_time time not null,
   end_time time not null,
   status varchar(2) not null,
   constraint fk_patient
      foreign key(patient_id) 
	  references patient(id),
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
