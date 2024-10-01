from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('clinics/', views.clinic_list, name='clinic_list'),
    path('clinics/<int:clinic_id>/', views.clinic_detail, name='clinic_detail'),
    path('clinics/add_clinic', views.add_clinic, name='add_clinic'),
    path('clinics/<int:clinic_id>/add_doctor/', views.add_doctor_to_clinic, name='add_doctor_to_clinic'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/add_doctor/', views.add_doctor, name='add_doctor'),
    path('doctors/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('doctors/<int:doctor_id>/edit/', views.edit_doctor, name='edit_doctor'),
    path('doctors/<int:doctor_id>/remove/', views.remove_doctor, name='remove_doctor'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add_patient', views.add_patient, name='add_patient'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:patient_id>/schedule-appointment/', views.schedule_appointment, name='schedule_appointment'),
]
