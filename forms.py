from django.forms import ModelForm
from django import forms
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
from .models import *


class PatientSignUpForm(ModelForm):
    retype_password = forms.CharField(widget=forms.PasswordInput, max_length=50)

    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'middle_name', 'name_suffix', 'birthday', 'sex', 'weight', 'height', 'cellphone_number', 'telephone_number',
                  'email', 'username', 'password', 'retype_password']
        widgets = {
            'password': forms.PasswordInput,
            'birthday': forms.DateInput(format=('%Y/%m/%d'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
        }

    # Function to confirm password
    def clean(self):
        cleaned_data = super(PatientSignUpForm, self).clean()
        password = cleaned_data.get('password')
        retype_password = cleaned_data.get('retype_password')

        if password != retype_password:
            raise forms.ValidationError("Passwords must be identical.")

    # Function to hash password before saving to the database
    def save(self, commit=True):
        user = super(PatientSignUpForm, self).save(commit=False)
        password = self.cleaned_data['password']
        user.password = make_password(password)

        if commit:
            user.save()


class PatientProfileForm(ModelForm):
    retype_password = forms.CharField(widget=forms.PasswordInput, max_length=50)

    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'middle_name', 'name_suffix', 'birthday', 'sex', 'weight', 'height', 'cellphone_number', 'telephone_number',
                  'email', 'username', 'password', 'retype_password', 'picture_file']
        widgets = {
            'password': forms.PasswordInput,
            'birthday': forms.DateInput(format=('%d/%m/%Y'),
                                        attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                               'type': 'date'}),
        }

    # Function to confirm password
    def clean(self):
        cleaned_data = super(PatientProfileForm, self).clean()
        password = cleaned_data.get("password")
        retype_password = cleaned_data.get("retype_password")

        if password != retype_password:
            raise forms.ValidationError("Passwords must be identical.")

    # Function to hash password before saving to the database
    def save(self, commit=True):
        user = super(PatientProfileForm, self).save(commit=False)
        password = self.cleaned_data['password']
        user.password = make_password(password)

        if commit:
            user.save()


class DoctorSignUpForm(ModelForm):
    retype_password = forms.CharField(widget=forms.PasswordInput, max_length=50)

    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'middle_name', 'name_suffix', 'birthday', 'sex', 'region',
                  'cellphone_number', 'telephone_number',
                  'email', 'username', 'password', 'retype_password', 'specialty', 'hospital', 'consultation_fee',
                  'insurance_company', 'license_number']
        widgets = {
            'password': forms.PasswordInput,
            'birthday': forms.DateInput(format=('%d/%m/%Y'),
                                        attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                               'type': 'date'}),
        }

    # Function to confirm password
    def clean(self):
        cleaned_data = super(DoctorSignUpForm, self).clean()
        password = cleaned_data.get("password")
        retype_password = cleaned_data.get("retype_password")

        if password != retype_password:
            raise forms.ValidationError("Passwords must be identical.")

    # Function to hash password before saving to the database
    def save(self, commit=True):
        user = super(DoctorSignUpForm, self).save(commit=False)
        password = self.cleaned_data['password']
        user.password = make_password(password)

        if commit:
            user.save()


class DoctorProfileForm(ModelForm):
    retype_password = forms.CharField(widget=forms.PasswordInput, max_length=50)

    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'middle_name', 'name_suffix', 'birthday', 'sex', 'region',
                  'cellphone_number', 'telephone_number',
                  'email', 'username', 'password', 'retype_password', 'specialty', 'hospital', 'consultation_fee',
                  'insurance_company', 'license_number', 'description', 'picture_file']
        widgets = {
            'password': forms.PasswordInput,
            'birthday': forms.DateInput(format=('%d/%m/%Y'),
                                        attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                               'type': 'date'}),
        }

    # Function to confirm password
    def clean(self):
        cleaned_data = super(DoctorProfileForm, self).clean()
        password = cleaned_data.get("password")
        retype_password = cleaned_data.get("retype_password")

        if password != retype_password:
            raise forms.ValidationError("Passwords must be identical.")

    # Function to hash password before saving to the database
    def save(self, commit=True):
        user = super(DoctorProfileForm, self).save(commit=False)
        password = self.cleaned_data['password']
        user.password = make_password(password)

        if commit:
            user.save()


class DoctorScheduleForm(ModelForm):
    class Meta:
        model = DoctorSchedule
        fields = ['date', 'start_time', 'end_time', 'break_start_time', 'break_end_time', 'consultation_time']
        widgets = {
            'date': forms.DateInput(format=('%d/%m/%Y'),
                                        attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                               'type': 'date'}),
            'start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'end_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'break_start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'break_end_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        self.doctorObj = kwargs.pop('doctorObj', None)
        super(DoctorScheduleForm, self).__init__(*args, **kwargs)

    # Function for extra validation of date, time range, and consultation_time
    def clean(self):
        doctor = self.doctorObj
        cleaned_data = super(DoctorScheduleForm, self).clean()
        date = cleaned_data.get("date")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        break_start_time = cleaned_data.get("break_start_time")
        break_end_time = cleaned_data.get("break_end_time")
        consultation_time = cleaned_data.get("consultation_time")

        schedule = DoctorSchedule.objects.all().filter(doctor=doctor).filter(date=date)

        if len(schedule) > 0:
            raise forms.ValidationError("Schedule already set for that day.")

        if start_time >= end_time:
            raise forms.ValidationError("End time cannot be before or equal to start time.")

        if break_start_time >= break_end_time:
            raise forms.ValidationError("Break end time cannot be before or equal to break start time.")

        if datetime.datetime.combine(datetime.date(1, 1, 1), end_time) - datetime.datetime.combine(datetime.date(1, 1, 1), start_time) < timedelta(hours=0, minutes=consultation_time):
            raise forms.ValidationError("Consultation time cannot fit in the given time range.")

    # Function to generate schedule intervals for the doctor's schedule
    def save(self, doctor, commit=True):
        form = super(DoctorScheduleForm, self).save(commit=False)
        form.doctor = doctor
        scheduleIntervals = {}
        new_end_time = self.cleaned_data.get('start_time')

        # While loop to generate the available schedules based on the constraints defined by the doctor
        while new_end_time < self.cleaned_data.get('end_time') and datetime.datetime.combine(datetime.date(1, 1, 1), self.cleaned_data.get('end_time')) - datetime.datetime.combine(datetime.date(1, 1, 1), new_end_time) >= timedelta(hours=0, minutes=self.cleaned_data.get('consultation_time')):
            new_start_time = new_end_time
            new_end_time = (datetime.datetime.combine(datetime.date(1, 1, 1), new_start_time) + timedelta(hours=0, minutes=self.cleaned_data.get('consultation_time'))).time()

            # Check if the time interval suits do not conflict with the break time of the doctor
            if (new_start_time < self.cleaned_data.get('break_start_time') and datetime.datetime.combine(datetime.date(1, 1, 1), self.cleaned_data.get('break_start_time')) - datetime.datetime.combine(datetime.date(1, 1, 1), new_start_time) >= timedelta(hours=0, minutes=self.cleaned_data.get('consultation_time'))) or new_start_time >= self.cleaned_data.get('break_end_time'):
                scheduleIntervals[new_start_time] = True

            # After the break time, change new_end_time with break_end_time
            if self.cleaned_data.get('break_start_time') < new_start_time < self.cleaned_data.get('break_end_time'):
                new_end_time = self.cleaned_data.get('break_end_time')

        form.schedule = scheduleIntervals

        if commit:
            form.save()

