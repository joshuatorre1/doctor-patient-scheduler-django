# Doc Kelan

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![PyCharm](https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white)

Doc Kelan is an online doctor appointment web application. It is a platform where people can look up and schedule appointments with a doctor that fits their needs. Doc Kelan also serves as a tool for doctors to widen the reach of their medical services and organize appointments. An adminstrator also exists in this system as a custodian of the whole doctor appointment web application with access to pertinent patient and doctor information.

During these times of the COVID-19 pandemic, Doc Kelan would prove beneficial as a self-contained software product to aid in the accessibility of medical care and mitigating the risk of people transmitting the virus.

# Requirements and Dependencies

* Operating system: Windows
*	Programming language: Python, HTML, CSS, JavaScript
*	IDE: PyCharm
*	Web framework: Django
*	Database system: PostgreSQL
*	Version control software: GitHub
*	Database adapter: pscopg2
*	Unit testing framework: unittest
*	Django imports: ModelForm, forms, render, redirect, timezone, messages, ValidationError, gettext_lazy, admin
*	Other imports: datetime, unittest 

# Environment Setup

### Prerequisites 
1. [Install PyCharm Professional](https://www.jetbrains.com/help/pycharm/installation-guide.html#silent)
2. [Install PostgreSQL](https://www.postgresql.org/docs/12/tutorial-install.html)
3. [Install Python](https://www.jetbrains.com/help/pycharm/python.html)

### [Django Environment Setup in PyCharm](https://www.youtube.com/watch?v=xv_bwpA_aEA&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=)
1. Install Django `<pip install django>`
2. Create new Django project in PyCharm
3. Start project `<django-admin startproject <project_name>>`
4. Test server using run button or `<python manage.py runserver>`
5. Install django-axes `<pip install django-axes>`
6. Install django-filters `<pip install django-filters>`
7. Install pillow `<pip install pillow>`

### [Connecting Database to Django in PyCharm](https://www.youtube.com/watch?v=mOu9fpfzyUg&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=)
1. Install psycopg2 `<pip install psycopg2>`
2. Configure Database setting in settings.py
3. Save configuration `<python manage.py migrate>`
4. Create admin/superuser in Django database `<python manage.py createsuperuser>`
5. Create Django model
6. Migrate model `<python manage.py makemigrations>` then `<python manage.py migrate>`


# Revision Logs

Access revision logs [here](https://www.notion.so/ce2618f2b10e4de0bfec7b052a16c8fb?v=d399da88f4b24fa694d47d6ae9017540)


# File List

### Python Files
admin.py  <br />
asgi.py <br />
filters.py <br />
forms.py <br />
models.py <br />
settings.py <br />
urls.py <br />
validation.py <br />
validationTest.py <br />
views.py <br />


### CSS Files
appointmentrequest.css <br />
doctorprofile.css <br />
doctorschedule.css <br />
doctorsignup.css <br />
edit_profile.css <br />
home.css <br />
landing.css <br />
landing-resize.css <br />
pastappointments.css <br />
patientsignup.css <br />
profile_page.css <br />
sidebar.css <br />
sign.css <br />
signup.css <br />
topbar.css <br />

### HTML Files
accept_appointment.html <br />
appointment_request.html <br />
decline_appointment.html <br />
doctor_profile.html <br />
doctorschedule.html <br />
doctorsignup.html <br />   
edit_appointment.html <br />
edit_profile.html <br />
home.html <br />
indiv_past_appointment.html <br />
landing.html <br />
lockout.html <br />
past_appointments.html <br />
patient_profile.html <br />
patientsignup.html <br /> 
profile_page.html <br />
reschedule_appointment.html <br />
sidebar.html <br />
signin.html  <br />
signup.html <br />
topbar.html <br />

### Other Files
appointment_page.png <br />
cover-photo.png <br />
default_profile_pic.png <br />
doctor_dashboard.png <br />
intro_image.png <br />
nurse.png <br />
patient.png <br />
patient_dashboard.png <br />
Mont-Heavy.otf <br />
Mont-Semibold.otf <br />  
README.md

# Contributors

## Fidelino, John Ira R.  
De La Salle University Manila  
Department of Electronics and Communications Engineering  
ira_fidelino@dlsu.edu.ph  
## Sim, Matthea Flynne T.  
De La Salle University Manila  
Department of Electronics and Communications Engineering  
matthea_sim@dlsu.edu.ph  
## Torre, Joshua Emmanuel R.
De La Salle University Manila  
Department of Electronics and Communications Engineering  
joshua_emmanuel_torre@dlsu.edu.ph

