from django.urls import path
from tracking import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('tasks/', views.TasksListView.as_view(), name="task-list"),
    path('<int:pk>/', views.TaskDetailView.as_view(), name="task-detail"),
    path('add-task/', views.TaskCreateView.as_view(), name="add-task"),
    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name="update-task"),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name="delete-task"),
    path('<int:pk>/complete/', views.TaskCompleteView.as_view(), name="task-complete"),
    path('<int:pk>/update-comment/', views.CommentUpdateView.as_view(), name="update-comment"),
    path('<int:pk>/delete-comment/', views.CommentDeleteView.as_view(), name="delete-comment"),
    path('comment/like/<int:pk>/', views.CommentLikeToggle.as_view(), name='comment-like-toggle'),
    path("user/<int:pk>/", views.UserPageView.as_view(), name="user-page"),
    path("user/<int:pk>/tasks/", views.UserTasksListView.as_view(), name="user-tasks"),
    path("user-update/<int:pk>/", views.UpdateUserView.as_view(), name="update-user"),
    path("subscribe/<int:pk>/", views.SurbscribeUserView.as_view(), name="subscribe"),
    path('user/<int:pk>/subscribers/', views.UserSubscribersView.as_view(), name='user-subscribers'),
    path('user/<int:pk>/subscribers-to/', views.UserSubscribersToView.as_view(), name='user-subscribers-to'),

]

app_name = "tasks"