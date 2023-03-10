from axes.decorators import axes_dispatch
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.urls import reverse
from .forms import *
from .models import *
from django.db.models import Q
from .filters import DoctorFilter

import datetime
import calendar
from calendar import HTMLCalendar


# Create your views here.
def landing(request):
    set_past_appointments()
    return render(request, 'dockelan/landing.html')


@axes_dispatch
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if user is a patient and credentials are valid
        if Patient.objects.filter(username=username).count() == 1 and check_password(password, Patient.objects.get(
                username=username).password):
            user = Patient.objects.get(username=username)
            user.last_login = datetime.datetime.now()
            user.is_active = True
            user.save()

            request.session['username'] = user.username

            return redirect('home', username=user.username)

        # Check if user is a doctor and credentials are valid
        elif Doctor.objects.filter(username=username).count() == 1 and check_password(password, Doctor.objects.get(
                username=username).password):
            user = Doctor.objects.get(username=username)
            user.last_login = datetime.datetime.now()
            user.is_active = True
            user.save()

            request.session['username'] = user.username

            return redirect('home', username=user.username)

        # User does not exists
        else:
            authenticate(request=request, username=username, password=password)  # For recording failed login attempts
            messages.info(request,
                          'The username and password you entered did not match our records. Please double-check and try again.')

    context = {}
    return render(request, 'dockelan/signin.html', context)


def signup(request):
    return render(request, 'dockelan/signup.html')


def patientsignup(request):
    form = PatientSignUpForm()

    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)

        if form.is_valid() and Doctor.objects.filter(username=form.cleaned_data.get('username')).count() == 0:
            form.save()

            # Record login and update status
            user = Patient.objects.get(username=form.cleaned_data.get('username'))
            user.last_login = datetime.datetime.now()
            user.is_active = True
            user.save()

            request.session['username'] = form.cleaned_data.get('username')
            return redirect('home', username=form.cleaned_data.get('username'))

        if Doctor.objects.filter(username=form.cleaned_data.get('username')).count() > 0:
            messages.info(request, 'Doctor with this Username already exists.')

    context = {'form': form}
    return render(request, 'dockelan/patientsignup.html', context)


def doctorsignup(request):
    form = DoctorSignUpForm()

    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)

        if form.is_valid() and Patient.objects.filter(username=form.cleaned_data.get('username')).count() == 0:
            form.save()

            # Record login and update status
            user = Doctor.objects.get(username=form.cleaned_data.get('username'))
            user.description = "I am a doctor that specializes in {}.".format(user.specialty.lower())
            user.last_login = datetime.datetime.now()
            user.is_active = True
            user.save()

            request.session['username'] = form.cleaned_data.get('username')
            return redirect('home', username=form.cleaned_data.get('username'))

        if Patient.objects.filter(username=form.cleaned_data.get('username')).count() > 0:
            messages.info(request, 'Patient with this Username already exists.')

    context = {'form': form}
    return render(request, 'dockelan/doctorsignup.html', context)


def home(request, username):
    set_past_appointments()

    month = int(datetime.datetime.now().month)
    month_name = calendar.month_name[month]
    year = int(datetime.datetime.now().year)
    cal = HTMLCalendar().formatmonth(year, month)

    # User is a patient
    if Patient.objects.filter(username=username).count() > 0:
        user = get_object_or_404(Patient, username=username)
        # user = Patient.objects.get(username=username)
        userType = "Patient"

        # Built-in filters based on Doctor model
        doctors = Doctor.objects.all().order_by('first_name')
        doctorFilter = DoctorFilter(request.GET, queryset=doctors)
        doctors = doctorFilter.qs

        # Access appointments to view status
        appointmentStatus = Appointment.objects.all().filter(patient=user.id).filter(
            date__gte=datetime.datetime.now()).order_by('date')

        # Access future appointments
        futureAppointments = Appointment.objects.all().filter(patient=user.id).filter(date__gte=datetime.datetime.now()).filter(Q(status="F") | Q(status="R")).order_by('date', 'start_time')

        if 'filter' in request.GET:
            # Search functionality based on name or email or hospital
            search = request.GET.get('search')

            if search is not None and len(search) != 0:  # Make sure request is not none
                keywords = search.split()
                # searchResults = None

                # if len(keywords) == 4:  # Full name search
                #     searchResults = Doctor.objects.all().filter(first_name__iexact=keywords[0]).filter(
                #         middle_name__iexact=keywords[1]).filter(last_name__iexact=keywords[2]).filter(
                #         name_suffix__iexact=keywords[3])
                #
                # elif len(keywords) == 3 and searchResults is None:  # Name search excluding name suffix
                #     searchResults = Doctor.objects.all().filter(first_name__iexact=keywords[0]).filter(
                #         middle_name__iexact=keywords[1]).filter(last_name__iexact=keywords[2])
                #
                # elif len(keywords) == 2 and searchResults is None:  # Name search including only first and last names
                #     searchResults = Doctor.objects.all().filter(first_name__iexact=keywords[0]).filter(
                #         last_name__iexact=keywords[1])

                # if searchResults is None or len(
                        #         searchResults) == 0:  # If user inputs other parameters than specified above
                        #     for word in keywords:
                        #         searchResults = Doctor.objects.all().filter(
                        #             Q(first_name__icontains=word) | Q(middle_name__icontains=word) | Q(
                        #                 last_name__icontains=word) |
                        #             Q(name_suffix__icontains=word) | Q(email=word))
                for word in keywords:
                    searchResults = Doctor.objects.all().filter(Q(hospital__iexact=word) | Q(first_name__icontains=word)
                        | Q(middle_name__icontains=word) | Q( last_name__icontains=word) | Q(name_suffix__icontains=word) | Q(email=word))

                doctors = doctors.intersection(searchResults)

        context = {'user': user, 'userType': userType, 'doctors': doctors, 'doctorFilter': doctorFilter,
                   'appointmentStatus': appointmentStatus, 'futureAppointments': futureAppointments, "year": year, "month": month, "month_name": month_name, "cal": cal}

    # User is a doctor
    else:
        user = get_object_or_404(Doctor, username=username)
        userType = "Doctor"
        patients = []

        # Access appointments to view status
        appointmentRequests = Appointment.objects.all().filter(doctor=user.id).filter(status="PR").filter(
            date__gte=datetime.datetime.now()).order_by('date', 'start_time')

        # Access future appointments
        futureAppointments = Appointment.objects.all().filter(doctor=user.id).filter(date__gte=datetime.datetime.now()).\
            filter(Q(status="F") | Q(status="R")).order_by('date', 'start_time')

        # Access all appointments to access patients
        allAppointments = Appointment.objects.all().filter(doctor=user.id).filter(Q(status="PR") | Q(status="F") |
            Q(status="P") | Q(status="R")).order_by('patient__first_name')

        for appointment in allAppointments:
            if appointment.patient not in patients:
                patients.append(appointment.patient)

        if 'filter' in request.GET:
            # Search functionality based on patient name
            search = request.GET.get('search')

            if search != "":
                keywords = request.GET.get('search').split(' ')
                patients = []

                for word in keywords:
                    allAppointments = Appointment.objects.all().filter(doctor=user.id).filter(
                        Q(status="PR") | Q(status="F") | Q(status="P") | Q(status="R")).filter(
                        Q(patient__first_name__icontains=word) | Q(patient__middle_name__icontains=word) |
                        Q(patient__last_name__icontains=word) | Q(patient__email=word)).order_by('patient__first_name')

                for appointment in allAppointments:
                    if appointment.patient not in patients:
                        patients.append(appointment.patient)

        context = {'user': user, 'userType': userType, 'appointmentRequest': appointmentRequests,
                   'futureAppointments': futureAppointments, 'patients': patients, "year": year, "month": month, "month_name": month_name, "cal": cal}

    if 'signout' in request.GET:
        user.last_logout = datetime.datetime.now()
        user.is_active = False
        user.save()

        return redirect('landing')

    if 'home' in request.GET:
        return redirect('home', username=username)

    if 'profile' in request.GET:
        return redirect('viewProfile', username=username)

    return render(request, 'dockelan/home.html', context)


def view_profile(request, username):
    if Patient.objects.filter(username=username).count() > 0:
        user = get_object_or_404(Patient, username=username)
        userType = "Patient"
    else:
        user = get_object_or_404(Doctor, username=username)
        userType = "Doctor"

    if 'signout' in request.GET:
        user.last_logout = datetime.datetime.now()
        user.is_active = False
        user.save()

        return redirect('landing')

    if 'home' in request.GET:
        return redirect('home', username=username)

    if 'profile' in request.GET:
        return redirect('viewProfile', username=username)

    context = {'user': user, 'userType': userType}
    return render(request, 'dockelan/profile_page.html', context)


def edit_profile(request, username):
    if Patient.objects.filter(username=username).count() > 0:
        user = get_object_or_404(Patient, username=username)
        userType = "Patient"
        form = PatientProfileForm(instance=user)

        if request.method == 'POST':
            form = PatientProfileForm(request.POST, request.FILES, instance=user)

            if form.is_valid() and Doctor.objects.filter(username=form.cleaned_data.get('username')).count() == 0:
                form.save()

                request.session['username'] = form.cleaned_data.get('username')
                return redirect('home', username=form.cleaned_data.get('username'))

            if Doctor.objects.filter(username=form.cleaned_data.get('username')).count() > 0:
                messages.info(request, 'Doctor with this Username already exists.')

    else:
        user = get_object_or_404(Doctor, username=username)
        userType = "Doctor"
        form = DoctorProfileForm(instance=user)

        if request.method == 'POST':
            form = DoctorProfileForm(request.POST, request.FILES, instance=user)

            if form.is_valid() and Patient.objects.filter(username=form.cleaned_data.get('username')).count() == 0:
                form.save()

                request.session['username'] = form.cleaned_data.get('username')
                return redirect('home', username=form.cleaned_data.get('username'))

            if Patient.objects.filter(username=form.cleaned_data.get('username')).count() > 0:
                messages.info(request, 'Patient with this Username already exists.')

    if 'signout' in request.GET:
        user.last_logout = datetime.datetime.now()
        user.is_active = False
        user.save()

        return redirect('landing')

    if 'home' in request.GET:
        return redirect('home', username=username)

    if 'profile' in request.GET:
        return redirect('viewProfile', username=username)

    context = {'user': user, 'userType': userType, 'form': form}

    return render(request, 'dockelan/edit_profile.html', context)

def doctorschedule(request):
    doctor = Doctor.objects.get(username=request.session['username'])
    form = DoctorScheduleForm()

    if request.method == 'POST':
        form = DoctorScheduleForm(request.POST, doctorObj=doctor)

        if form.is_valid():
            form.save(doctor)

            return HttpResponseRedirect(reverse('home', args=[request.session['username']]))

    if 'signout' in request.GET:
        doctor.last_logout = datetime.datetime.now()
        doctor.is_active = False
        doctor.save()

        return redirect('landing')

    if 'home' in request.GET:
        return redirect('home', username=doctor.username)

    if 'profile' in request.GET:
        return redirect('viewProfile', username=doctor.username)

    context = {'form': form, 'doctor': doctor}

    return render(request, 'dockelan/doctorschedule.html', context)


def patient_profile(request, patientUsername):
    user = Doctor.objects.get(username=request.session['username'])
    userType = "Doctor"
    patient = Patient.objects.get(username=patientUsername)

    context = {'patient': patient, 'userType': userType}

    if 'signout' in request.GET:
        user.last_logout = datetime.datetime.now()
        user.is_active = False
        user.save()

        return redirect('landing')

    if 'home' in request.GET:
        return redirect('home', username=user.username)

    if 'profile' in request.GET:
        return redirect('viewProfile', username=user.username)

    return render(request, 'dockelan/patient_profile.html', context)

def doctor_profile(request, doctorUsername):
    month = int(datetime.datetime.now().month)
    month_name = calendar.month_name[month]
    year = int(datetime.datetime.now().year)
    cal = HTMLCalendar().formatmonth(year, month)

    user = Patient.objects.get(username=request.session['username'])
    doctor = get_object_or_404(Doctor, username=doctorUsername)
    profilePic = "/images/" + str(doctor.picture_file)
    doctorSchedule = DoctorSchedule.objects.all().filter(doctor=doctor.id).filter(
        date__gte=datetime.datetime.now()).order_by('date')

    availableSchedules = {}
    dates = []

    # If doctor has a schedule
    if len(doctorSchedule) != 0:
        # For loop to access the schedule entries of the doctor in the database
        for entry in doctorSchedule:
            schedules = {}
            timeIntervals = []

            # For loop to access the individual schedules of the doctor
            for start_time in entry.schedule:
                # Get only the available ones
                if entry.schedule[start_time] == "True" and datetime.datetime.combine(entry.date,
                                                                                      datetime.datetime.strptime(
                                                                                              start_time,
                                                                                              '%H:%M:%S').time()) > datetime.datetime.now():
                    if entry.date not in dates:
                        dates.append(entry.date)

                    end_time = (datetime.datetime.combine(datetime.date(1, 1, 1),
                                                          datetime.datetime.strptime(start_time,
                                                                                     '%H:%M:%S').time()) + timedelta(
                        hours=0, minutes=entry.consultation_time)).time()
                    timeIntervals.append([start_time, str(end_time)])

                schedules[entry.id] = timeIntervals
            availableSchedules[entry.date] = schedules

        context = {'doctor': doctor, 'profilePic': profilePic, 'doctorSchedule': doctorSchedule, 'dates': dates,
                   'availableSchedules': availableSchedules, 'timeIntervals': timeIntervals, "year": year, "month": month, "month_name": month_name, "cal": cal}

    else:
        context = {'doctor': doctor, 'profilePic': profilePic, "year": year, "month": month, "month_name": month_name, "cal": cal}

    if 'chooseDate' in request.POST:
        date = request.POST.get('schedule')

        if date is not None:  # If filter is present
            availableSchedules = {}
            if len(doctorSchedule) != 0:  # If doctor has a schedule
                # For loop to access the schedule entries of the doctor in the database
                for entry in doctorSchedule:
                    schedules = {}
                    timeIntervals = []

                    if datetime.datetime.strptime(date,
                                                  '%B %d, %Y').date() == entry.date:  # Access only the dates based on the filter
                        # For loop to access the individual schedules of the doctor
                        for start_time in entry.schedule:
                            # Get only the available ones
                            if entry.schedule[start_time] == "True" and datetime.datetime.combine(entry.date,
                                                                                                  datetime.datetime.strptime(
                                                                                                          start_time,
                                                                                                          '%H:%M:%S').time()) > datetime.datetime.now():
                                end_time = (datetime.datetime.combine(datetime.date(1, 1, 1),
                                                                      datetime.datetime.strptime(start_time,
                                                                                                 '%H:%M:%S').time()) + timedelta(
                                    hours=0, minutes=entry.consultation_time)).time()
                                timeIntervals.append([start_time, str(end_time)])

                            schedules[entry.id] = timeIntervals
                        availableSchedules[entry.date] = schedules

        context = {'doctor': doctor, 'profilePic': profilePic, 'doctorSchedule': doctorSchedule, 'dates': dates,
                   'availableSchedules': availableSchedules, 'timeIntervals': timeIntervals, "year": year, "month": month, "month_name": month_name, "cal": cal}

    if 'signout' in request.GET:
        user.last_logout = datetime.datetime.now()
        user.is_active = False
        user.save()

        return redirect('landing')

    if 'home' in request.GET:
        return redirect('home', username=user.username)

    if 'profile' in request.GET:
        return redirect('viewProfile', username=user.username)

    return render(request, 'dockelan/doctor_profile.html', context)


def appointment_request(request, id, date, start_time, end_time):
    user = Patient.objects.get(username=request.session['username'])
    doctor = Doctor.objects.get(id=id)
    scheduleEntry = DoctorSchedule.objects.get(Q(doctor=doctor.id) & Q(date=date))  # Get schedule entry

    schedDetails = [scheduleEntry.date, start_time, end_time]

    if 'confirmAppointment' in request.POST:
        scheduleEntry.schedule[start_time] = False  # Set schedule availablity to false
        scheduleEntry.save()

        # Create appointment request
        newAppointment = Appointment(patient_id=user.id, doctor_id=doctor.id, date=date, start_time=start_time,
                                     end_time=end_time, status="PR")
        newAppointment.save()

        return HttpResponseRedirect(reverse('home', args=[request.session['username']]))

    if 'signout' in request.GET:
        user.last_logout = datetime.datetime.now()
        user.is_active = False
        user.save()

        return redirect('landing')

    if 'home' in request.GET:
        return redirect('home', username=user.username)

    if 'profile' in request.GET:
        return redirect('viewProfile', username=user.username)

    context = {'doctor': doctor, 'user': user, 'schedDetails': schedDetails}

    return render(request, 'dockelan/appointment_request.html', context)


def accept_appointment(request, id):
    appointment = Appointment.objects.get(id=id)

    if 'acceptAppointment' in request.POST:  # Accept appointment
        appointment.status = "F"
        appointment.save()

        return HttpResponseRedirect(reverse('home', args=[request.session['username']]))

    if 'signout' in request.GET:
        appointment.doctor.last_logout = datetime.datetime.now()
        appointment.doctor.is_active = False
        appointment.doctor.save()

        return redirect('landing')

    if 'home' in request.GET:
        return redirect('home', username=appointment.doctor.username)

    if 'profile' in request.GET:
        return redirect('viewProfile', username=appointment.doctor.username)

    context = {'appointment': appointment}

    return render(request, 'dockelan/accept_appointment.html', context)


def decline_appointment(request, id):
    appointment = Appointment.objects.get(id=id)

    if 'declineAppointment' in request.POST:  # Decline appointment
        appointment.status = "D"
        appointment.save()

        scheduleEntry = DoctorSchedule.objects.get(Q(doctor=appointment.doctor) & Q(date=appointment.date))
        scheduleEntry.schedule[appointment.start_time] = True  # Set schedule availablity to true
        scheduleEntry.save()

        return HttpResponseRedirect(reverse('home', args=[request.session['username']]))

    if 'signout' in request.GET:
        appointment.doctor.last_logout = datetime.datetime.now()
        appointment.doctor.is_active = False
        appointment.doctor.save()

        return redirect('landing')

    if 'home' in request.GET:
        return redirect('home', username=appointment.doctor.username)

    if 'profile' in request.GET:
        return redirect('viewProfile', username=appointment.doctor.username)

    context = {'appointment': appointment}

    return render(request, 'dockelan/decline_appointment.html', context)


def reschedule_appointment(request, id):
    user = Doctor.objects.get(username=request.session['username'])
    appointment = Appointment.objects.get(id=id)
    doctorSchedule = DoctorSchedule.objects.all().filter(doctor=user.id).filter().order_by('date')

    availableSchedules = {}

    # If doctor has a schedule
    if len(doctorSchedule) != 0:
        # For loop to access the schedule entries of the doctor in the database
        for entry in doctorSchedule:
            scheduleId = []
            timeIntervals = []

            if entry.date >= datetime.date.today():  # Get the for the present and the future
                scheduleId.append(entry.id)

                # For loop to access the individual schedules of the doctor
                for start_time in entry.schedule:
                    # Get only the available ones
                    if entry.schedule[start_time] == "True" and datetime.datetime.combine(entry.date,
                                                                                          datetime.datetime.strptime(
                                                                                                  start_time,
                                                                                                  '%H:%M:%S').time()) > datetime.datetime.now():
                        end_time = (datetime.datetime.combine(datetime.date(1, 1, 1),
                                                              datetime.datetime.strptime(start_time,
                                                                                         '%H:%M:%S').time()) + timedelta(
                            hours=0, minutes=entry.consultation_time)).time()
                        timeIntervals.append([start_time, str(end_time)])

                    availableSchedules[entry.date] = timeIntervals

        context = {'appointment': appointment, 'availableSchedules': availableSchedules}

    else:
        context = {'appointment': appointment}

    if 'rescheduleAppointment' in request.POST and request.POST.get('schedule') is not None:
        # Previous schedule
        previousScheduleEntry = DoctorSchedule.objects.get(Q(doctor=user.id) & Q(date=appointment.date))
        previousScheduleEntry.schedule[appointment.start_time] = True  # Set schedule availability to true
        previousScheduleEntry.save()

        # New schedule
        newScheduleDetails = request.POST.get('schedule').split('-')
        date = datetime.datetime.strptime(newScheduleDetails[0], '%B %d, %Y')

        # Record new schedule
        newScheduleEntry = DoctorSchedule.objects.get(Q(doctor=user.id) & Q(date=date))  # Get schedule entry
        newScheduleEntry.schedule[newScheduleDetails[1]] = False  # Set schedule availability to false
        newScheduleEntry.save()

        # Edit appointment request
        appointment.date = date
        appointment.start_time = newScheduleDetails[1]
        appointment.end_time = newScheduleDetails[2]
        appointment.status = 'R'  # Set status to rescheduled
        appointment.save()

        return HttpResponseRedirect(reverse('home', args=[request.session['username']]))

    if 'signout' in request.GET:
        user.last_logout = datetime.datetime.now()
        user.is_active = False
        user.save()

        return redirect('landing')

    if 'home' in request.GET:
        return redirect('home', username=user.username)

    if 'profile' in request.GET:
        return redirect('viewProfile', username=user.username)

    return render(request, 'dockelan/reschedule_appointment.html', context)


def edit_appointment(request, id):
    appointment = Appointment.objects.get(id=id)
    doctorSchedule = DoctorSchedule.objects.all().filter(doctor=appointment.doctor.id).filter().order_by('date')

    if Patient.objects.filter(username=request.session['username']).count() > 0:
        user = Patient.objects.get(username=request.session['username'])
        userType = "Patient"
    else:
        user = Doctor.objects.get(username=request.session['username'])
        userType = "Doctor"

    availableSchedules = {}

    # If doctor has a schedule
    if len(doctorSchedule) != 0:
        # For loop to access the schedule entries of the doctor in the database
        for entry in doctorSchedule:
            scheduleId = []
            timeIntervals = []

            if entry.date >= datetime.date.today():  # Get the for the present and the future
                scheduleId.append(entry.id)

                # For loop to access the individual schedules of the doctor
                for start_time in entry.schedule:
                    # Get only the available ones
                    if entry.schedule[start_time] == "True" and datetime.datetime.combine(entry.date,
                                                                                          datetime.datetime.strptime(
                                                                                              start_time,
                                                                                              '%H:%M:%S').time()) > datetime.datetime.now():
                        end_time = (datetime.datetime.combine(datetime.date(1, 1, 1),
                                                              datetime.datetime.strptime(start_time,
                                                                                         '%H:%M:%S').time()) + timedelta(
                            hours=0, minutes=entry.consultation_time)).time()
                        timeIntervals.append([start_time, str(end_time)])

                    availableSchedules[entry.date] = timeIntervals

        context = {'userType': userType, 'appointment': appointment, 'availableSchedules': availableSchedules}

    else:
        context = {'userType': userType, 'appointment': appointment}

    if 'rescheduleAppointment' in request.POST and request.POST.get('schedule') is not None:
        # Previous schedule
        previousScheduleEntry = DoctorSchedule.objects.get(Q(doctor=appointment.doctor.id) & Q(date=appointment.date))
        previousScheduleEntry.schedule[appointment.start_time] = True  # Set schedule availability to true
        previousScheduleEntry.save()

        # New schedule
        newScheduleDetails = request.POST.get('schedule').split('-')
        date = datetime.datetime.strptime(newScheduleDetails[0], '%B %d, %Y')

        # Record new schedule
        newScheduleEntry = DoctorSchedule.objects.get(Q(doctor=appointment.doctor.id) & Q(date=date))  # Get schedule entry
        newScheduleEntry.schedule[newScheduleDetails[1]] = False  # Set schedule availability to false
        newScheduleEntry.save()

        # Edit appointment request
        appointment.date = date
        appointment.start_time = newScheduleDetails[1]
        appointment.end_time = newScheduleDetails[2]

        if userType == "Patient":
            appointment.status = "PR"  # Set status to pending request
        else:
            appointment.status = "R"  # Set status to rescheduled

        appointment.save()

        return HttpResponseRedirect(reverse('home', args=[request.session['username']]))

    if 'cancelAppointment' in request.POST: # Cancel appointment
        if userType == "Patient":
            appointment.status = "CP"  # Set status to cancelled by patient
        else:
            appointment.status = "CD"  # Set status to cancelled by doctor

        appointment.save()

        scheduleEntry = DoctorSchedule.objects.get(Q(doctor=appointment.doctor) & Q(date=appointment.date))
        scheduleEntry.schedule[appointment.start_time] = True  # Set schedule availablity to true
        scheduleEntry.save()

        return HttpResponseRedirect(reverse('home', args=[request.session['username']]))

    if 'signout' in request.GET:
        user.last_logout = datetime.datetime.now()
        user.is_active = False
        user.save()

        return redirect('landing')

    if 'home' in request.GET:
        return redirect('home', username=user.username)

    if 'profile' in request.GET:
        return redirect('viewProfile', username=user.username)

    return render(request, 'dockelan/edit_appointment.html', context)


def past_appointments(request, username):
    if Patient.objects.filter(username=username).count() > 0:
        user = Patient.objects.get(username=username)
        userType = "Patient"
        pastAppointments = Appointment.objects.all().filter(patient=user.id).filter(status="P").order_by('date', 'start_time')

    else:
        user = Doctor.objects.get(username=username)
        userType = "Doctor"
        pastAppointments = Appointment.objects.all().filter(doctor=user.id).filter(status="P").order_by('date', 'start_time')

    if 'signout' in request.GET:
        user.last_logout = datetime.datetime.now()
        user.is_active = False
        user.save()

        return redirect('landing')

    if 'home' in request.GET:
        return redirect('home', username=user.username)

    if 'profile' in request.GET:
        return redirect('viewProfile', username=user.username)

    context = {'userType': userType, 'pastAppointments': pastAppointments}

    return render(request, 'dockelan/past_appointments.html', context)


def view_past_appointment(request, id):
    appointment = Appointment.objects.get(id=id)

    if Patient.objects.filter(username=request.session['username']).count() > 0:
        user = Patient.objects.get(username=request.session['username'])
        userType = "Patient"
    else:
        user = Doctor.objects.get(username=request.session['username'])
        userType = "Doctor"

    context = {'userType': userType, 'appointment': appointment}

    if 'signout' in request.GET:
        user.last_logout = datetime.datetime.now()
        user.is_active = False
        user.save()

        return redirect('landing')

    if 'home' in request.GET:
        return redirect('home', username=user.username)

    if 'profile' in request.GET:
        return redirect('viewProfile', username=user.username)

    return render(request, 'dockelan/indiv_past_appointment.html', context)


def set_past_appointments():
    pastAppointmentsByDate = Appointment.objects.all().filter(Q(status="F") | Q(status="R")).filter(date__lt=datetime.datetime.now())
    pastAppointmentsByTime = Appointment.objects.all().filter(Q(status="F") | Q(status="R")).filter(
        date__lte=datetime.datetime.now()).filter(start_time__lt=datetime.datetime.now().time())

    for appointment in pastAppointmentsByDate:
        appointment.status = "P"
        appointment.save()

    for appointment in pastAppointmentsByTime:
        appointment.status = "P"
        appointment.save()
