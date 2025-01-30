from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import UserProfile, Schedule, BarangayService, Appointment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta


class HomePageView (LoginRequiredMixin, TemplateView):
    template_name = 'app/home.html'

class AboutPageView (TemplateView):
    template_name = 'app/about.html'

class ClearancePageView (TemplateView):
    template_name = 'app/clearance.html'

    def clearance_view(request):
        return render(request, 'app/clearance.html')

class IndigencyPageView (TemplateView):
    template_name = 'app/indigency.html'

    def indigency_view(request):
        return render(request, 'app/indigency.html')
    
class IDPageView (TemplateView):
    template_name = 'app/ID.html'

    def ID_view(request):
        return render(request, 'app/ID.html')

class UserProfileListView (LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'app/userprofile.html'
    context_object_name = 'userprofile_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        filtered_profiles = UserProfile.objects.filter(user=self.request.user)
        if query:
            filtered_profiles = filtered_profiles.filter(
                Q(user__username__icontains=query) |  
                Q(contact_number__icontains=query) |  
                Q(address__icontains=query)   
                )
        context['userprofile_list'] = filtered_profiles
        context['search_query'] = query 

        print(f"Logged-in User: {self.request.user}")
        print(f"Filtered Profiles: {filtered_profiles}")
        return context

class ScheduleListView (ListView):
    model = Schedule
    template_name = 'app/schedule.html'
    context_object_name = 'Schedule_list'

    def get_queryset(self):
        return Schedule.objects.filter(user=self.request.user)

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

class ScheduleDetailView (DetailView):
    model = Schedule
    template_name = 'app/scheduledetail.html'
    context_object_name = 'ScheduleDetail_list'

class BarangayServiceDetailView (DetailView):
    model = BarangayService
    template_name = 'app/barangayservicedetail.html'
    context_object_name = 'BarangayServiceDetail_list'

class AppointmentDetailView (DetailView):
    model = Appointment
    template_name = 'app/appointmentdetail.html'
    context_object_name = 'AppointmentDetail_list'

class UserProfileCreateView (CreateView):
    model = UserProfile
    fields = ['contact_number','address','birthdate']
    template_name = 'app/userprofilecreate.html'
    
    def form_valid(self, form):
        if UserProfile.objects.filter(user=self.request.user).exists():
            messages.error(self.request, "You already have a profile.")
            return redirect('userprofile') 
        
        form.instance.user = self.request.user

        user = self.request.user
        form.instance.save()
        
        user = self.request.user
        email = self.request.POST.get('email')
        user.email = email
        user.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('schedulecreate') 

class ScheduleCreateView(CreateView):
    model = Schedule
    fields = ['date', 'time_slot', 'is_available']
    template_name = 'app/schedulecreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        max_date = today + timedelta(days=7)

       
        time_slots = []
        for hour in range(8, 18):  
            time_slots.append(f"{hour}:00")

        context['today'] = today
        context['max_date'] = max_date
        context['time_slots'] = time_slots 

        return context

    def form_valid(self, form):
        selected_date = form.cleaned_data['date']
        today = timezone.now().date()
        max_date = today + timedelta(days=7)

        if not (today <= selected_date <= max_date):
            form.add_error('date', 'The date must be within the next 7 days.')
            return self.form_invalid(form)

        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('barangayservicecreate')

class BarangayServiceCreateView (CreateView):
    model = BarangayService
    fields = ['name','description',]
    template_name = 'app/barangayservicecreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['names'] = BarangayService.SERVICE_CHOICES 
        context['decriptions'] = BarangayService.objects.all()
        context['user'] = self.request.user
        return context
    
    def form_valid(self, form):
        if BarangayService.objects.filter(user=self.request.user, name=form.cleaned_data['name']).exists():
            messages.error(self.request, "You have already created this type of service.")
            return redirect('barangayservicecreate') 
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('appointmentcreate') 
    
class AppointmentCreateView (CreateView):
    model = Appointment
    fields = ['user','service','schedule','status',]
    template_name = 'app/appointmentcreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        context['users'] = User.objects.all()
        context['services'] = BarangayService.objects.all()
        context['schedules'] = Schedule.objects.all()
        context['status_choices'] = Appointment.STATUS_CHOICES 
        return context
    
    def form_valid(self, form):
        if Appointment.objects.filter(user=self.request.user, service=form.cleaned_data['service'], status__in=['pending', 'confirmed']).exists():
            messages.error(self.request, f"You already have an appointment for {form.cleaned_data['service'].name}.")
            return redirect('appointmentcreate')
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('appointment')

class UserProfileUpdateView (UpdateView):
    model = UserProfile
    fields = ['user','contact_number','address','birthdate']
    template_name = 'app/userprofileupdate.html'

class ScheduleUpdateView (UpdateView):
    model = Schedule
    fields = ['date','time_slot','is_available',]
    template_name = 'app/scheduleupdate.html'

class BarangayServiceUpdateView (UpdateView):
    model = BarangayService
    fields = ['name','description',]
    template_name = 'app/barangayserviceupdate.html'
    
class AppointmentUpdateView (UpdateView):
    model = Appointment
    fields = ['user','service','schedule','status']
    template_name = 'app/appointmentupdate.html'

class UserProfileDeleteView (DeleteView):
    model = UserProfile
    template_name = 'app/userprofiledelete.html'
    success_url = reverse_lazy('userprofile')

class ScheduleDeleteView (DeleteView):
    model = Schedule
    template_name = 'app/scheduledelete.html'
    success_url = reverse_lazy('schedule')

class BarangayServiceDeleteView (DeleteView):
    model = BarangayService
    template_name = 'app/barangayservicedelete.html'
    success_url = reverse_lazy('barangayservice')

class AppointmentDeleteView (DeleteView):
    model = Appointment
    template_name = 'app/appointmentdelete.html'
    success_url = reverse_lazy('appointment')

def search_redirect(request):
    query = request.GET.get('q', '').strip()

    if query:
        if UserProfile.objects.filter(
            Q(user__username__icontains=query) |
            Q(contact_number__icontains=query) |
            Q(address__icontains=query)
        ).exists():
            return redirect(f'/userprofile/?q={query}')

        if Schedule.objects.filter(
            Q(date__icontains=query) | 
            Q(time_slot__icontains=query)
        ).exists():
            return redirect(f'/schedule/?q={query}')

        if BarangayService.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        ).exists():
            return redirect(f'/barangayservice/?q={query}')

        if Appointment.objects.filter(
            Q(user__username__icontains=query) |
            Q(service__name__icontains=query)
        ).exists():
            return redirect(f'/appointment/?q={query}')

    messages.error(request, "No results found.")
    return redirect('home')

