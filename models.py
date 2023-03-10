from django.db import models
from django.contrib.postgres.fields import HStoreField
from .validation import *
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from django.db.models import Q


# Create your models here.
sexChoices = (("Male", "Male"), ("Female", "Female"), (("Others", "Others")))


class Patient(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    name_suffix = models.CharField(max_length=4, blank=True)
    username = models.CharField(validators=[validate_username], max_length=50, unique=True)
    password = models.TextField(validators=[validate_password])
    birthday = models.DateField(validators=[validate_birthday])
    sex = models.CharField(max_length=6, choices=sexChoices)
    cellphone_number = models.BigIntegerField(validators=[validate_cellphone_number])
    telephone_number = models.BigIntegerField(validators=[validate_telephone_number], blank=True)
    email = models.CharField(validators=[validate_email], max_length=50, unique=True)
    weight = models.IntegerField(validators=[validate_weight])
    height = models.IntegerField(validators=[validate_height])
    picture_file = models.ImageField(null=True, blank=True, default="default_profile_pic.png")
    date_joined = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_login = models.DateTimeField(blank=True, null=True)
    last_logout = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}. {} {}".format(self.first_name, self.middle_name[0], self.last_name, self.name_suffix)

    class Meta:
        db_table = "patient"

    # Function to hash password before saving to the database in admin site and to set default profile picture
    def save(self, *args, **kwargs):
        if self.picture_file == "":
            self.picture_file = "default_profile_pic.png"

        if 'pbkdf2_sha256$260000$' not in self.password:
            self.password = make_password(self.password)

        super().save(*args, **kwargs)


class Doctor(models.Model):
    regionChoices = (
        ("I", "I"), ("II", "II"), ("III", "III"), ("IV-A", "IV-A"), ("IV-B", "IV-B"), ("V", "V"), ("CAR", "CAR"),
        ("NCR", "NCR"), ("VI", "VI"), ("VII", "VII"),
        ("VIII", "VIII"), ("IX", "IX"), ("X", "X"), ("XI", "XI"), ("XII", "XII"), ("XIII", "XIII"), ("BARMM", "BARMM"))
    specialties = ["Allergy and immunology", "Anatomical pathology", "Anesthesiology", "Cardiology",
                   "Critical care medicine", "Dermatology", "Diagnostic radiology",
                   "Emergency medicine", "Endocrinology and metabolism", "Family medicine", "Gastroenterology",
                   "General internal medicine", "General surgery",
                   "General/Clinical pathology", "Geriatric Medicine", "Hematology" "Internal medicine",
                   "Medical genetics", "Medical microbiology and infectious diseases",
                   "Medical oncology", "Nephrology", "Neurology", "Nuclear medicine", "Obstetrics and gynecology",
                   "Occupational medicine", "Opthalmology", "Orthopedic",
                   "Otolaryngology", "Pathology", "Pediatrics", "Physical medicine and rehabilitation",
                   "Preventive medicine", "Psychiatry", "Public health and preventive medicine",
                   "Radiation oncology", "Respirology", "Rheumatology", "Urology"]
    specialtyChoices = tuple((specialty, specialty) for specialty in specialties)

    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    name_suffix = models.CharField(max_length=4, blank=True)
    username = models.CharField(validators=[validate_username], max_length=50, unique=True)
    password = models.TextField(validators=[validate_password])
    birthday = models.DateField(validators=[validate_birthday])
    sex = models.CharField(max_length=6, choices=sexChoices)
    region = models.CharField(max_length=5, choices=regionChoices)
    cellphone_number = models.BigIntegerField(validators=[validate_cellphone_number])
    telephone_number = models.BigIntegerField(validators=[validate_telephone_number], blank=True)
    email = models.CharField(validators=[validate_email], max_length=50, unique=True)
    specialty = models.CharField(max_length=50, choices=specialtyChoices)
    hospital = models.CharField(max_length=50)
    consultation_fee = models.DecimalField(validators=[validate_consultation_fee], max_digits=7, decimal_places=2)
    insurance_company = models.CharField(max_length=50, blank=True)
    license_number = models.CharField(validators=[validate_license], max_length=7, unique=True)
    description = models.TextField()
    picture_file = models.ImageField(null=True, blank=True, default="default_profile_pic.png")
    date_joined = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_login = models.DateTimeField(blank=True, null=True)
    last_logout = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}. {} {}".format(self.first_name, self.middle_name[0], self.last_name, self.name_suffix)

    class Meta:
        db_table = "doctor"

    # Function to hash password before saving to the database in admin site
    def save(self, *args, **kwargs):
        if self.picture_file == "":
            self.picture_file = "default_profile_pic.png"

        if 'pbkdf2_sha256$260000$' not in self.password:
            self.password = make_password(self.password)

        super().save(*args, **kwargs)


class DoctorSchedule(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.CASCADE, blank=True)
    date = models.DateField(validators=[validate_date])
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_start_time = models.TimeField()
    break_end_time = models.TimeField()
    consultation_time = models.IntegerField(validators=[validate_time])
    schedule = HStoreField(blank=True)

    class Meta:
        db_table = "doctor_schedule"

    # Function to generate schedule intervals for the doctor's schedule in admin site
    def save(self, *args, **kwargs):
        if self.schedule is None:
            scheduleIntervals = {}
            new_end_time = self.start_time

            while new_end_time < self.end_time and datetime.datetime.combine(datetime.date(1, 1, 1), self.end_time) - datetime.datetime.combine(datetime.date(1, 1, 1), new_end_time) >= timedelta(hours=0, minutes=self.consultation_time):
                new_start_time = new_end_time
                new_end_time = (datetime.datetime.combine(datetime.date(1, 1, 1), new_start_time) + timedelta(hours=0, minutes=self.consultation_time)).time()

                if (new_start_time < self.break_start_time and datetime.datetime.combine(datetime.date(1, 1, 1), self.break_start_time) - datetime.datetime.combine(datetime.date(1, 1, 1), new_start_time) >= timedelta(hours=0, minutes=self.consultation_time)) or new_start_time >= self.break_end_time:
                    scheduleIntervals[new_start_time] = True

                # After the break time, change new_end_time with break_end_time
                if self.break_start_time < new_start_time < self.break_end_time:
                    new_end_time = self.cleaned_data.get('break_end_time')

            self.schedule = scheduleIntervals
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


class Appointment(models.Model):
    statusChoices = (("PR", "Pending request"), ("CD", "Cancelled by doctor"), (("CP", "Cancelled by patient")),
                     (("D", "Declined")), (("F", "Future appointment")), (("P", "Past appointment")), (("R", "Rescheduled")))

    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE, blank=True)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.CASCADE, blank=True)
    date = models.DateField(validators=[validate_date])
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=2, choices=statusChoices)

    class Meta:
        db_table = "appointment"

    def save(self, *args, **kwargs):
        if DoctorSchedule.objects.all().filter(doctor_id=self.doctor.id).filter(date=self.date).count() > 0: # If doctor has existing schedul
            scheduleEntry = DoctorSchedule.objects.get(Q(doctor=self.doctor.id) & Q(date=self.date))
            scheduleEntry.schedule[self.start_time] = False
            scheduleEntry.save()
            super().save(*args, **kwargs)
        else: # If doctor does not have existing schedule
            super().save(*args, **kwargs)
