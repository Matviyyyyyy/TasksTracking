from django import forms
from tracking.models import *

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "priority", "due_date", "user"]