from django.urls import path
from tracking import views

urlpatterns = [
    path('', views.TasksListView.as_view(), name="task-list"),
    path('<int:pk>/', views.TaskDetailView.as_view(), name="task-detail"),
    path('add-task/', views.TaskCreateView.as_view(), name="add-task")
]

app_name = "tasks"