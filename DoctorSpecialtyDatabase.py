import psycopg2

# Connect to database
connection = psycopg2.connect(host = "localhost",
                database = "DocKelan",
                user = "postgres",
                password = "LBYCPD2")

cursor = connection.cursor() # Pointer in the database

# Define table
table = '''create table doctorSpecialty(
   id serial primary key,
   specialty varchar(50) not null
)'''

# Create table
cursor.execute(table)

# Based on https://www.dr-bill.ca/blog/practice-management/complete-list-of-doctor-specialties-medical-subspecialties/ and
# https://www.sgu.edu/blog/medical/ultimate-list-of-medical-specialties/
specialty = ["Allergy and immunology", "Anatomical pathology", "Anesthesiology", "Cardiology", "Critical care medicine", "Dermatology", "Diagnostic radiology",
             "Emergency medicine", "Endocrinology and metabolism", "Family medicine", "Gastroenterology", "General internal medicine", "General surgery",
             "General/Clinical pathology", "Geriatric Medicine", "Hematology" "Internal medicine", "Medical genetics", "Medical microbiology and infectious diseases",
             "Medical oncology", "Nephrology", "Neurology", "Nuclear medicine", "Obstetrics and gynecology", "Occupational medicine", "Opthalmology", "Orthopedic",
             "Otolaryngology", "Pathology", "Pediatrics", "Physical medicine and rehabilitation", "Preventive medicine", "Psychiatry", "Public health and preventive medicine",
             "Radiation oncology", "Respirology", "Rheumatology", "Urology"]

for i in range(len(specialty)):
    # Define insert query
    insertQuery = "insert into doctorSpecialty(id, specialty) values(%s, %s)"

    data = (i + 1, specialty[i])

    # Insert data to database
    cursor.execute(insertQuery, data)

# Close communication with the PostgreSQL database server
cursor.close()

# Commit the changes
connection.commit()

connection.close()

