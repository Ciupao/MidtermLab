from django.urls import path
from django.contrib.auth.views import LoginView
from .views import HomePageView, search_redirect, UserProfileListView, ScheduleListView, BarangayServiceListView, AppointmentListView, UserProfileDetailView, UserProfileCreateView, UserProfileUpdateView, UserProfileDeleteView, ScheduleDetailView, BarangayServiceDetailView, AppointmentDetailView, ScheduleCreateView, BarangayServiceCreateView, ScheduleUpdateView, BarangayServiceUpdateView, ScheduleDeleteView, BarangayServiceDeleteView, AppointmentCreateView, AppointmentUpdateView, AppointmentDeleteView
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('', HomePageView.as_view(), name='home'),
    path('search/', search_redirect, name='search_redirect'),
    
    path('userprofile/', UserProfileListView.as_view(), name='userprofile'),
    path('schedule/', ScheduleListView.as_view(), name='schedule'),
    path('barangayservice/', BarangayServiceListView.as_view(), name='barangayservice'),
    path('appointment/', AppointmentListView.as_view(), name='appointment'),

    path('userprofile/<int:pk>', UserProfileDetailView.as_view(), name='userprofiledetail'),
    path('schedule/<int:pk>', ScheduleDetailView.as_view(), name='scheduledetail'),
    path('barangayservice/<int:pk>', BarangayServiceDetailView.as_view(), name='barangayservicedetail'),
    path('appointment/<int:pk>', AppointmentDetailView.as_view(), name='appointmentdetail'),

    path('userprofile/create', UserProfileCreateView.as_view(), name='userprofilecreate'),
    path('schedule/create', ScheduleCreateView.as_view(), name='schedulecreate'),
    path('barangayservice/create', BarangayServiceCreateView.as_view(), name='barangayservicecreate'),
    path('appointment/create', AppointmentCreateView.as_view(), name='appointmentcreate'),

    path('userprofile/<int:pk>/edit', UserProfileUpdateView.as_view(), name='userprofileupdate'),
    path('schedule/<int:pk>/edit', ScheduleUpdateView.as_view(), name='scheduleupdate'),
    path('barangayservice/<int:pk>/edit', BarangayServiceUpdateView.as_view(), name='barangayserviceupdate'),
    path('appointment/<int:pk>/edit', AppointmentUpdateView.as_view(), name='appointmentupdate'),

    path('userprofile/<int:pk>/delete', UserProfileDeleteView.as_view(), name='userprofiledelete'),
    path('schedule/<int:pk>/delete', ScheduleDeleteView.as_view(), name='scheduledelete'),
    path('barangayservice/<int:pk>/delete', BarangayServiceDeleteView.as_view(), name='barangayservicedelete'),
    path('appointment/<int:pk>/delete', AppointmentDeleteView.as_view(), name='appointmentdelete'),
]
