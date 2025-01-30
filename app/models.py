from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError

class BarangayService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    SERVICE_CHOICES = [
        ('clearance', 'Barangay Clearance'),
        ('id', 'Barangay ID'),
        ('indigency', 'Indigency Certificate'),
    ]
    
    name = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    description = models.TextField() 

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("barangayservicedetail", kwargs={"pk": self.pk})

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    birthdate = models.DateField()

    def __str__(self):
        return self.user.username
    def get_absolute_url(self):
        return reverse("userprofiledetail", kwargs={"pk": self.pk})

class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    time_slot = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.date} {self.time_slot}"
    def get_absolute_url(self):
        return reverse("scheduledetail", kwargs={"pk": self.pk})
    def clean(self):
     
        overlapping_schedules = Schedule.objects.filter(
            user=self.user, date=self.date, time_slot=self.time_slot
        )
        if self.pk:
            overlapping_schedules = overlapping_schedules.exclude(pk=self.pk)

        if overlapping_schedules.exists():
            raise ValidationError('You already have a schedule at this time.')

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    service = models.ForeignKey(BarangayService, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.SET_NULL, null=True,) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.name} - {self.status}"
    def get_absolute_url(self):
        return reverse("appointmentdetail", kwargs={"pk": self.pk})
    def clean(self):
        if Appointment.objects.filter(user=self.user, service=self.service, status__in=['pending', 'confirmed']).exists():
            raise ValidationError(f"You already have an appointment for {self.service.name}.")

class AppointmentHistory(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE) 
    old_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    new_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    changed_at = models.DateTimeField(auto_now_add=True) 
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='changed_by_user')

    def __str__(self):
        return f"History for {self.appointment} - {self.old_status} -> {self.new_status}"

