from django import forms
from tracking.models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "priority", "due_date"]
        widgets = {
            'due_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'min': date.today().strftime('%Y-%m-%d'),
                }
            )
        }
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text", "media"]
        widgets = {
            "media": forms.FileInput()
        }
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields["text"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Text..."
        })
        self.fields["media"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Media..."
        })


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

class TaskSearchForm(forms.Form):
    name = forms.CharField(max_length=256)

    def __init__(self, *args, **kwargs):
        super(TaskSearchForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {"class": "form-control",
            "placeholder": "Enter name of task..."}
        )

# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email")
#
#     def __init__(self, *args, **kwargs):
#         super(CustomUserCreationForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs.update({"class": "form-control"})
#
# class CustomUserAuthenticationForm(AuthenticationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'password')
#
#     def __init__(self, *args, **kwargs):
#         super(CustomUserAuthenticationForm, self).__init__(*args, **kwargs)
#         self.fields["username"].widget.attrs.update({"class": "form-control"})
#         self.fields["password"].widget.attrs.update({"class": "form-control"})

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})