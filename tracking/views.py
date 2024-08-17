from django.shortcuts import render
from django.urls import reverse_lazy
from tracking.models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from tracking.forms import TaskForm, TaskFilterForm
from tracking.mixing import UserIsOwnerMixin
from django.contrib.auth.mixins import LoginRequiredMixin

class TasksListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/task-list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status', '')
        priority = self.request.GET.get('priority', '')
        if status and priority:
            queryset = queryset.filter(status=status, priority=priority)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskFilterForm(self.request.GET)
        return context

class TaskDetailView(DetailView):
    model = Task
    context_object_name = "task"
    template_name = "tasks/task-detail.html"

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "tasks/task-creating.html"
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Task
    template_name = "tasks/task-updating.html"
    form_class = TaskForm
    context_object_name = "task"
    success_url = reverse_lazy("tasks:task-list")

class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Task
    template_name = "tasks/task-delete-confirmation.html"
    context_object_name = "task"
    success_url = reverse_lazy("tasks:task-list")
