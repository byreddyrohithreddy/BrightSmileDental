from django.shortcuts import render, get_object_or_404, redirect
from .models import Clinic, Doctor, Patient, Visit, Appointment, PROCEDURE_CHOICES
from .forms import ClinicForm, DoctorForm, PatientForm, AppointmentForm
from datetime import datetime, time
from django.contrib import messages
from django.utils import timezone


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login') 

def dashboard(request):
    return render(request, 'dashboard.html')

def clinic_list(request):
    clinics = Clinic.objects.all()
    return render(request, 'clinic_list.html', {'clinics': clinics})

def clinic_detail(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    doctors = Doctor.objects.filter(clinic=clinic)
    
    if request.method == 'POST':
        form = ClinicForm(request.POST, instance=clinic)
        if form.is_valid():
            form.save()
            return redirect('clinic_detail', clinic_id=clinic.id)
    else:
        form = ClinicForm(instance=clinic)

    return render(request, 'clinic_detail.html', {
        'clinic': clinic,
        'doctors': doctors,
        'form': form,
    })

def add_clinic(request):
    if request.method == 'POST':
        form = ClinicForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Clinic added successfully!')
            return redirect('clinic_list')
        else:
            messages.error(request, 'Error saving clinic: ' + str(form.errors))
    else:
        form = ClinicForm()

    return render(request, 'add_clinic.html', {'form': form})

def add_doctor_to_clinic(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    print(clinic)
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.save()
            doctor.clinic.add(clinic)
            doctor.save()
            return redirect('clinic_detail', clinic_id=clinic.id)
    else:
        form = DoctorForm()

    return render(request, 'add_doctor_to_clinic.html', {'form': form, 'clinic': clinic, 'procedures': PROCEDURE_CHOICES})

def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('clinic_detail', clinic_id=doctor.clinic.id)
    else:
        form = DoctorForm(instance=doctor)

    return render(request, 'edit_doctor.html', {
        'form': form,
        'doctor': doctor,
    })

def remove_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        doctor.delete()
        return redirect('clinic_detail', clinic_id=doctor.clinic.id)

    return render(request, 'remove_doctor.html', {
        'doctor': doctor,
    })


def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})

def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm()

    return render(request, 'add_doctor.html', {
        'form': form, 
        'procedures': PROCEDURE_CHOICES
    })

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    patients = Patient.objects.filter(doctor=doctor)
    
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_detail', doctor_id=doctor.id)
    else:
        form = DoctorForm(instance=doctor)

    return render(request, 'doctor_detail.html', {
        'doctor': doctor,
        'patients': patients,
        'form': form,
    })

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})

def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    visits = Visit.objects.filter(patient=patient)
    
    now = timezone.now()
    next_appointment = Appointment.objects.filter(patient=patient,date__gte=now).order_by('date').first()

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = PatientForm(instance=patient)

    return render(request, 'patient_detail.html', {
        'patient': patient,
        'visits': visits,
        'next_appointment': next_appointment,
        'form': form,
    })

def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()

    return render(request, 'add_patient.html', {'form': form})

def convert_time(time_str):
    try:
        time_parts = time_str[0].split()
        if len(time_parts) != 2:
            return None 
        time, period = time_parts[0], time_parts[1].upper()
        hour, minute = map(int, time.split(':'))

        if period == 'AM':
            if hour == 12: 
                hour = 0
        elif period == 'PM':
            if hour != 12:
                hour += 12
        else:
            return None

        return hour

    except ValueError:
        return None 

def schedule_appointment(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    clinics = []
    doctors = []
    available_time_slots = []

    if request.method == 'POST':
        procedure_id = request.POST.get('procedure')
        clinic_id = request.POST.get('clinic')
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        time_slot = convert_time(request.POST.getlist('time_slot'))

        if procedure_id and clinic_id and doctor_id and appointment_date and time_slot:
            appointment = Appointment(
                doctor=Doctor.objects.get(id=doctor_id),
                patient=patient,
                procedure=procedure_id,
                clinic=Clinic.objects.get(id=clinic_id),
                date=appointment_date,
                time_slot=time_slot
            )
            appointment.save()
            messages.success(request, "Appointment booked successfully!")
            return redirect('patient_detail', patient_id=patient_id)

        messages.error(request, "There was an error booking the appointment. Please try again.")

    procedure_id = request.GET.get('procedure')
    clinic_id = request.GET.get('clinic')
    doctor_id = request.GET.get('doctor')
    selected_date = request.GET.get('appointment_date')

    if procedure_id:
        clinics = Clinic.objects.filter(doctor__specialty=procedure_id).distinct()

    if clinic_id:
        doctors = Doctor.objects.filter(clinic__id=clinic_id, specialty=procedure_id)

        if doctor_id and selected_date:
            selected_doctor = Doctor.objects.get(id=doctor_id)
            available_time_slots = selected_doctor.get_available_time_slots(
                Clinic.objects.get(id=clinic_id), date_str=selected_date
            )

            available_time_slots = [ (time(slot).strftime("%I:%M %p")) for slot in available_time_slots]
            print(available_time_slots)

    return render(request, 'schedule_appointment.html', {
        'patient': patient,
        'procedure_choices': PROCEDURE_CHOICES,
        'clinics': clinics,
        'doctors': doctors,
        'available_time_slots': available_time_slots,
    })

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ClinicSerializer, DoctorSerializer, PatientSerializer
from rest_framework import status

@api_view(['POST'])
def api_add_clinic(request):
    if request.method == 'POST':
        serializer = ClinicSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def api_add_doctor(request):
    if request.method == 'POST':
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def api_add_patient(request):
    if request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def api_clinic_info(request):
    clinics = Clinic.objects.all()
    clinic_data = []

    for clinic in clinics:
        clinic_data.append({
            'id': clinic.id,
            'name': clinic.name,
            'phone_number': clinic.phone_number,
            'city': clinic.city,
            'state': clinic.state,
            'address': clinic.address,
            'email': clinic.email,
            'doctor_count': clinic.doctor_count(),
            'patient_count': clinic.patient_count(),
        })

    return JsonResponse(clinic_data, safe=False)
