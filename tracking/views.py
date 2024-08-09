from django.shortcuts import render
from django.urls import reverse_lazy
from tracking.models import *
from django.views.generic import ListView, DetailView, CreateView
from tracking.forms import TaskForm

class TasksListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/task-list.html"

class TaskDetailView(DetailView):
    model = Task
    context_object_name = "task"
    template_name = "tasks/task-detail.html"

class TaskCreateView(CreateView):
    model = Task
    template_name = "tasks/task-creating.html"
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")
