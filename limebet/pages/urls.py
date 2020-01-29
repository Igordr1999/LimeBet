from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('about/', views.about_page, name="about"),
    path('team/', views.team_page, name="team"),
    path('contacts/', views.contacts_page, name="contacts"),
    path('get-started/', views.get_started, name="get_started"),
    path('platform-status/', views.platform_status_page, name="platform_status"),
    path('bugtracker/create/', views.BugTrackerCreate.as_view(), name="bugtracker_create"),
    path('bugtracker/', views.BugTrackerReportListView.as_view(), name="bugtracker_reports"),
    path('bugtracker/my/', views.MyBugTrackerReportListView.as_view(), name="bugtracker_my_reports"),
    path('bugtracker/<int:id>/', views.BugTrackerReportDetailView.as_view(), name="bugtracker_report"),
]
