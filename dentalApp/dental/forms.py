from django import forms
from .models import Patient, Visit, Appointment, Doctor, Clinic

class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['name', 'phone_number', 'city', 'state', 'address', 'email']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['npi', 'name', 'email', 'phone_number', 'office_address', 'working_schedule']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'date_of_birth', 'phone_number', 'address', 'ssn_last_4', 'gender', 'doctor']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['procedure', 'clinic', 'doctor', 'date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        procedure = kwargs.pop('procedure', None)
        clinic = kwargs.pop('clinic', None)
        super(AppointmentForm, self).__init__(*args, **kwargs)

        PROCEDURE_CHOICES = [
            ('Cleaning', 'Cleaning'),
            ('Filling', 'Filling'),
            ('Root Canal', 'Root Canal'),
            ('Crown', 'Crown'),
            ('Teeth Whitening', 'Teeth Whitening'),
        ]
        self.fields['procedure'] = forms.ChoiceField(choices=PROCEDURE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    
        if procedure:
            self.fields['clinic'].queryset = Clinic.objects.filter(doctor__specialty=procedure).distinct()
        else:
            self.fields['clinic'].queryset = Clinic.objects.none()

        if clinic:
            self.fields['doctor'].queryset = Doctor.objects.filter(clinic=clinic, specialty=procedure).distinct()
        else:
            self.fields['doctor'].queryset = Doctor.objects.none()

        self.fields['clinic'].widget.attrs.update({'class': 'form-control'})
        self.fields['doctor'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update({'class': 'form-control'})
