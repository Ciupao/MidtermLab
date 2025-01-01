from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class BarangayService(models.Model):
    SERVICE_CHOICES = [
        ('clearance', 'Barangay Clearance'),
        ('id', 'Barangay ID'),
        ('indigency', 'Indigency Certificate'),
    ]
    
    name = models.CharField(max_length=50, choices=SERVICE_CHOICES, unique=True)
    description = models.TextField() 

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    birthdate = models.DateField()
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    def get_absolute_url(self):
        return reverse("userprofiledetail", kwargs={"pk": self.pk})

class Schedule(models.Model):
    date = models.DateField()
    time_slot = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.date} {self.time_slot}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    service = models.ForeignKey(BarangayService, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.name} - {self.status}"
    

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

