from django.urls import path
from tracking import views

urlpatterns = [
    path('', views.TasksListView.as_view(), name="task-list"),
    path('<int:pk>/', views.TaskDetailView.as_view(), name="task-detail"),
    path('add-task/', views.TaskCreateView.as_view(), name="add-task"),
    path('<int:pk>/update', views.TaskUpdateView.as_view(), name="update-task"),
    path('<int:pk>/delete', views.TaskDeleteView.as_view(), name="delete-task"),
]

app_name = "tasks"