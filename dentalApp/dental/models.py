from django.db import models
from datetime import datetime, timedelta
import re 

PROCEDURE_CHOICES = [
    ('Cleaning', 'Cleaning'),
    ('Filling', 'Filling'),
    ('Root Canal', 'Root Canal'),
    ('Crown', 'Crown'),
    ('Teeth Whitening', 'Teeth Whitening'),
]

class Clinic(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.name

    def doctor_count(self):
        return self.doctor_set.count()

    def patient_count(self):
        return sum(doctor.patient_set.count() for doctor in self.doctor_set.all())

class Doctor(models.Model):
    npi = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    specialty = models.CharField(max_length=255, default="General")
    clinic = models.ManyToManyField(Clinic)
    office_address = models.TextField(default="Unknown")
    working_schedule = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    def clinic_count(self):
        return self.clinic.count()

    def patient_count(self):
        return self.patient_set.count()
    
    def get_available_time_slots(self, clinic, date_str):
        if not self.working_schedule:
            return []
        
        available_time_slots = []
 
        day_regex = r'(?P<days>Mon|Tue|Wed|Thu|Fri|Sat|Sun)(?:-(?P<end_days>Mon|Tue|Wed|Thu|Fri|Sat|Sun))?'
        time_regex = r'(\d{1,2}:\d{2} (?:AM|PM)) - (\d{1,2}:\d{2} (?:AM|PM))'
        
        working_days = re.findall(day_regex, self.working_schedule)
        time_ranges = re.findall(time_regex, self.working_schedule)

        day_mapping = {
            'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4,
            'Sat': 5, 'Sun': 6
        }

        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        weekday = date.weekday()

        # Get booked time slots for the specific date
        booked_times = Appointment.objects.filter(
            doctor=self,
            date_booked=date
        ).values_list('time_slot', flat=True)

        # Flatten the booked_times into a single list
        booked_times_flat = [time for slot in booked_times for time in slot]

        for (days, end_days), (start_time, end_time) in zip(working_days, time_ranges):
            start_day = day_mapping[days]
            end_day = day_mapping[end_days] if end_days else start_day

            if start_day <= weekday <= end_day:
                start_time = datetime.strptime(start_time.strip(), '%I:%M %p').time()
                end_time = datetime.strptime(end_time.strip(), '%I:%M %p').time()

                current_time = datetime.combine(date, start_time)
                end_time = datetime.combine(date, end_time)

                while current_time.time() < end_time.time():

                    slot_hour = current_time.hour
                    
                    if slot_hour not in booked_times_flat:
                        available_time_slots.append(slot_hour)
                    
                    current_time += timedelta(hours=1)

        return available_time_slots

class Patient(models.Model):
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    ssn_last_4 = models.CharField(max_length=4, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

    def last_visit(self):
        return self.visit_set.last()
    
    def next_appointment(self):
        return self.appointment_set.filter(date__gte=models.functions.Now()).first()

class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    procedures_done = models.CharField(max_length=255, default="General")
    doctors_notes = models.TextField(default="No notes provided")

    def __str__(self):
        return f"Visit on {self.date_time} by {self.doctor.name}"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField()
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    procedure = models.CharField(max_length=255, choices=PROCEDURE_CHOICES)
    date_booked = models.DateField(auto_now_add=True)
    time_slot = models.PositiveIntegerField(blank=True, default=None)

    def __str__(self):
        return f"Appointment on {self.date} at {self.clinic.name}"
