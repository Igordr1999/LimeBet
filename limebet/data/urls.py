from django.urls import path

from . import views
from . import viewsets

urlpatterns = [
    path('countries/', views.CountryListView.as_view(), name="countries"),
    path('bookmakers/', views.BookmakerListView.as_view(), name="bookmakers"),
    path('sports/', views.SportListView.as_view(), name="sports"),
    path('teams/', views.TeamListView.as_view(), name="teams"),
    path('leagues/', views.LeagueListView.as_view(), name="leagues"),
    path('event/<int:id>/', views.EventDetailView.as_view(), name="event"),
    path('bet/<int:id>/', views.BetDetailView.as_view(), name="bet"),
    path('events/', views.EventListView.as_view(), name="events"),
    path('bets/', views.BetListView.as_view(), name="bets"),
    path('surebets/', views.surebets, name="surebets"),
    path('valuebets/', views.valuebets, name="valuebets"),
]
