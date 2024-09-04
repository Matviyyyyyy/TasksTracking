from django.shortcuts import render, redirect
from tracking.models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.views import LoginView, LogoutView
from auth_system.forms import CustomUserCreationForm, CustomUserAuthenticationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class CustomLoginView(LoginView):
    template_name = "tasks/login.html"
    redirect_authenticated_user = True
    form_class = CustomUserAuthenticationForm


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = "auth_system:login"


class RegisterView(CreateView):
    template_name = "tasks/register.html"
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse_lazy("auth_system:login"))