from django import forms
from tracking.models import *

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "priority", "due_date"]
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [
        ("", "All"),
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]

    PRIORITY_CHOICES = [
        ("", "All"),
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High")
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label="Status")
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False, label="Priority")

    def __init__(self, *args, **kwargs):
        super(TaskFilterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})