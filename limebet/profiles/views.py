from django.urls import reverse_lazy
from django.views import generic

from .forms import ProfileCreationForm, ProfileLoginForm


class Registration(generic.CreateView):
    form_class = ProfileCreationForm
    success_url = reverse_lazy('login')
    template_name = 'profiles/registration.html'


class Login(generic.FormView):
    form_class = ProfileLoginForm
    success_url = reverse_lazy('home')
    template_name = 'profiles/login.html'
