from django.contrib import admin
from .models import BarangayService, UserProfile, Schedule, Appointment, AppointmentHistory

admin.site.register(BarangayService)
admin.site.register(UserProfile)
admin.site.register(Schedule)
admin.site.register(Appointment)
admin.site.register(AppointmentHistory)