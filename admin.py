from django.contrib import admin

# Register your models here.

from .models import *


class User(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'middle_name', 'last_name', 'is_active')
    search_fields = ('first_name', 'middle_name', 'last_name', 'username', 'email')
    readonly_fields = ('date_joined', 'last_login', 'last_logout')


class Schedule(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'start_time', 'end_time', 'consultation_time', 'schedule')
    search_fields = ('doctor__first_name', 'doctor__middle_name', 'doctor__last_name', 'date', 'consultation_time')


class AppointmentSchedule(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'date', 'start_time', 'end_time', 'status')
    search_fields = ('doctor__first_name', 'doctor__middle_name', 'doctor__last_name', 'patient__first_name',
                     'patient__middle_name', 'patient__last_name', 'date', 'start_time', 'status',)


admin.site.register(Patient, User)
admin.site.register(Doctor, User)
admin.site.register(DoctorSchedule, Schedule)
admin.site.register(Appointment, AppointmentSchedule)
