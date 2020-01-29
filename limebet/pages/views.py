from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from profiles.models import Profile
from pages.models import BugTrackerStatus, BugTrackerReport
from django_filters.views import FilterView
from .forms import ReportForm, ReportParamForm


def home_page(request):
    return render(request, 'pages/home.html')


def about_page(request):
    return render(request, 'pages/about.html')


def team_page(request):
    return render(request, 'pages/our_team.html')


def contacts_page(request):
    return render(request, 'pages/contacts.html')


def platform_status_page(request):
    return render(request, 'pages/platform_status.html')


def get_started(request):
    return render(request, 'pages/get_started.html')


class BugTrackerCreate(LoginRequiredMixin, CreateView):
    form_class = ReportForm
    template_name = 'pages/bugtracker_create_report.html'
    success_url = reverse_lazy('bugtracker_create')

    def form_valid(self, form):
        form_url = form.save(commit=False)
        form_url.owner = Profile.objects.get(id=self.request.user.id)
        form_url.status = BugTrackerStatus.objects.get(id=1)
        form_url.save()
        return super().form_valid(form)


class BugTrackerReportListView(LoginRequiredMixin, FilterView):
    template_name = "pages/bugtracker_reports.html"
    filterset_class = ReportParamForm
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        return BugTrackerReport.objects.filter(visible=True)


class MyBugTrackerReportListView(LoginRequiredMixin, FilterView):
    template_name = "pages/bugtracker_reports.html"
    filterset_class = ReportParamForm
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        return BugTrackerReport.objects.filter(visible=True,
                                               owner=Profile.objects.get(id=self.request.user.id))


class BugTrackerReportDetailView(LoginRequiredMixin, DetailView):
    model = BugTrackerReport
    slug_field = "id"
    slug_url_kwarg = "id"
    template_name = "pages/bugtracker_report.html"

    def get_queryset(self, *args, **kwargs):
        return BugTrackerReport.objects.filter(visible=True)
