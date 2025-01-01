from django.urls import path
from .views import HomePageView, AboutPageView, ClearancePageView, IndigencyPageView, UserProfileListView, ScheduleListView, BarangayServiceListView, AppointmentListView, UserProfileDetailView, UserProfileCreateView, UserProfileUpdateView, UserProfileDeleteView
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('clearance/', ClearancePageView.as_view(), name='clearance'),
    path('indigency/', IndigencyPageView.as_view(), name='indigency'),
    path('userprofile/', UserProfileListView.as_view(), name='userprofile'),
    path('schedule/', ScheduleListView.as_view(), name='schedule'),
    path('barangayservice/', BarangayServiceListView.as_view(), name='barangayservice'),
    path('appointment/', AppointmentListView.as_view(), name='appointment'),
    path('userprofile/<int:pk>', UserProfileDetailView.as_view(), name='userprofiledetail'),
    path('userprofile/create', UserProfileCreateView.as_view(), name='userprofilecreate'),
    path('userprofile/<int:pk>/edit', UserProfileUpdateView.as_view(), name='userprofileupdate'),
    path('userprofile/<int:pk>/delete', UserProfileDeleteView.as_view(), name='userprofiledelete'),
]
