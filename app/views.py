from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import UserProfile, Schedule, BarangayService, Appointment
from django.urls import reverse_lazy

class HomePageView (TemplateView):
    template_name = 'app/home.html'

class AboutPageView (TemplateView):
    template_name = 'app/about.html'

class ClearancePageView (TemplateView):
    template_name = 'app/clearance.html'

class IndigencyPageView (TemplateView):
    template_name = 'app/indigency.html'

class UserProfileListView (ListView):
    model = UserProfile
    template_name = 'app/userprofile.html'
    context_object_name = 'UserProfile_list'

class ScheduleListView (ListView):
    model = Schedule
    template_name = 'app/schedule.html'
    context_object_name = 'Schedule_list'

class BarangayServiceListView (ListView):
    model = BarangayService
    template_name = 'app/barangayservice.html'
    context_object_name = 'BarangayService_list'

class AppointmentListView (ListView):
    model = Appointment
    template_name = 'app/appointment.html'
    context_object_name = 'Appointment_list'

class UserProfileDetailView (DetailView):
    model = UserProfile
    template_name = 'app/userprofiledetail.html'
    context_object_name = 'UserProfileDetail_list'

class UserProfileCreateView (CreateView):
    model = UserProfile
    fields = ['user','contact_number','address','birthdate']
    template_name = 'app/userprofilecreate.html'

class UserProfileUpdateView (UpdateView):
    model = UserProfile
    fields = ['user','contact_number','address','birthdate']
    template_name = 'app/userprofileupdate.html'

class UserProfileDeleteView (DeleteView):
    model = UserProfile
    template_name = 'app/userprofiledelete.html'
    success_url = reverse_lazy('userprofile')