"""limebet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as drf

from data import views, viewsets

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('', include('pages.urls')),
    path('', include('data.urls')),
    path('profile/', include('profiles.urls')),
    path('accounts/', include("account.urls")),
    path('dev/methods/', schema_view),
    path('admin/', admin.site.urls),
    path('api/GetToken/', drf.obtain_auth_token, name="get_token"),

    path('api/CountryListView/', viewsets.CountryListView.as_view()),
    path('api/BookmakerListView/', viewsets.BookmakerListView.as_view()),
    path('api/SportListView/', viewsets.SportListView.as_view()),
    path('api/BookmakerTeamNameListView/', viewsets.BookmakerTeamNameListView.as_view()),
    path('api/TeamListView/', viewsets.TeamListView.as_view()),
    path('api/HandicapListView/', viewsets.HandicapListView.as_view()),
    path('api/TotalListView/', viewsets.TotalListView.as_view()),
    path('api/ResultListView/', viewsets.ResultListView.as_view()),
    path('api/HandicapQuoteListView/', viewsets.HandicapQuoteListView.as_view()),
    path('api/TotalQuoteListView/', viewsets.TotalQuoteListView.as_view()),
    path('api/ResultQuoteListView/', viewsets.ResultQuoteListView.as_view()),
    path('api/QuotesListView/', viewsets.QuotesListView.as_view()),
    path('api/BookmakerUrlListView/', viewsets.BookmakerUrlListView.as_view()),
    path('api/LeagueListView/', viewsets.LeagueListView.as_view()),
    path('api/EventListView/', viewsets.EventListView.as_view()),
    path('api/EventShortListView/', viewsets.EventShortListView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
