from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name="landing"),
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('signup/patient', views.patientsignup, name="patientsignup"),
    path('signup/doctor', views.doctorsignup, name="doctorsignup"),
    path('home/<str:username>', views.home, name="home"),
    path('doctorschedule/', views.doctorschedule, name="doctorschedule"),
    path('doctor/<str:doctorUsername>', views.doctor_profile, name="doctorUsername"),
    path('patient/<str:patientUsername>', views.patient_profile, name="patientProfile"),
    path('appointment_request/<str:id>/<str:date>/<str:start_time>/<str:end_time>', views.appointment_request, name="appointmentRequest"),
    path('accept_appointment/<str:id>', views.accept_appointment, name="acceptAppointment"),
    path('decline_appointment/<str:id>', views.decline_appointment, name="declineAppointment"),
    path('reschedule_appointment/<str:id>', views.reschedule_appointment, name="rescheduleAppointment"),
    path('edit_appointment/<str:id>', views.edit_appointment, name="editAppointment"),
    path('past_appointments/<str:username>', views.past_appointments, name="pastAppointments"),
    path('past_appointment/<str:id>', views.view_past_appointment, name="pastAppointment"),
    path('profile_page/<str:username>', views.view_profile, name="viewProfile"),
    path('edit_page/<str:username>', views.edit_profile, name="editProfile"),
]
