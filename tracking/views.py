from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from tracking.models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from tracking.forms import TaskForm, TaskFilterForm, CommentForm,UserForm, TaskSearchForm
from tracking.mixing import UserIsOwnerMixin, UserIsHisProfileMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from datetime import date

class TasksListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/task-list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        for task in queryset:
            if task.due_date < date.today():
                comments_to_task = Comment.objects.filter(task=task).all()
                comments_to_task.delete()
                task.delete()
        status = self.request.GET.get('status', '')
        priority = self.request.GET.get('priority', '')
        task_name = self.request.GET.get('name', '')
        if status and priority:
            queryset = queryset.filter(status=status, priority=priority)
        if task_name:
            queryset = queryset.filter(name=task_name)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_filter_form"] = TaskFilterForm(self.request.GET)
        context["task_search_form"] = TaskSearchForm(self.request.GET)
        return context

class TaskDetailView(DetailView):
    model = Task
    context_object_name = "task"
    template_name = "tasks/task-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context["comments"] = Comment.objects.filter(task=task)
        context["comment_form"] = CommentForm()
        return context
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.task = self.get_object()
            comment.save()
            return redirect('tasks:task-detail', pk=comment.task.pk)
        else:
            # Тут можна обробити випадок з невалідною формою
            pass

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

    def form_valid(self, form):
        comments = Comment.objects.filter(task=self.get_object())
        comments.delete()
        return super().form_valid(form)

class CommentUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Comment
    template_name = "tasks/comment_update.html"
    form_class = CommentForm
    context_object_name = "comment"

    def get_success_url(self):
        return reverse_lazy("tasks:task-detail", kwargs={'pk': self.object.task.pk})
class CommentDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Comment
    template_name = "tasks/comment-delete-confirmation.html"
    context_object_name = "comment"
    def get_success_url(self):
        return reverse_lazy("tasks:task-detail", kwargs={'pk': self.object.task.pk})
class TaskCompleteView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = "done"
        task.save()
        return HttpResponseRedirect(reverse_lazy("tasks:task-list"))

    def get_object(self):
        task_id = self.kwargs.get('pk')
        return get_object_or_404(Task, pk=task_id)

class TaskSearchView(View):
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = "done"
        task.save()
        return HttpResponseRedirect(reverse_lazy("tasks:task-list"))

    def get_object(self):
        task_id = self.kwargs.get('pk')
        return get_object_or_404(Task, pk=task_id)

def home_page(request):
    return render(
        request,
        template_name="tasks/home.html")

class CommentLikeToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        like_qs = Like.objects.filter(comment=comment, user=request.user)
        if like_qs.exists():
            like_qs.delete()
        else:
            Like.objects.create(comment=comment, user=request.user)
        return redirect('tasks:task-detail', pk=comment.task.pk)

# class CustomLoginView(LoginView):
#     template_name = "tasks/login.html"
#     redirect_authenticated_user = True
#     form_class = CustomUserAuthenticationForm
#
#
# class CustomLogoutView(LogoutView):
#     next_page = "tasks:login"
#
#
# class RegisterView(CreateView):
#     template_name = "tasks/register.html"
#     form_class = CustomUserCreationForm
#
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect(reverse_lazy("tasks:login"))
#
class UserPageView(DetailView):
    model = CustomUser
    context_object_name = "user"
    template_name = "tasks/user-page.html"

class UserTasksListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "user_tasks"
    template_name = "tasks/user-tasks.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.kwargs['pk']
        user = User.objects.get(id=user_id)
        queryset = queryset.filter(user=user)
        return queryset

class UpdateUserView(LoginRequiredMixin, UserIsHisProfileMixin, UpdateView):
    model = CustomUser
    template_name = "tasks/update-user.html"
    form_class = UserForm
    context_object_name = "user"
    def get_success_url(self):
        return reverse_lazy("tasks:user-page", kwargs={'pk': self.object.pk})

class SurbscribeUserView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        subscribe_to = get_object_or_404(User, pk=self.kwargs.get('pk'))
        subscribe = Subscribe.objects.filter(user=subscribe_to, subscriber=request.user)
        if subscribe.exists():
            subscribe.delete()
        else:
            Subscribe.objects.create(user=subscribe_to, subscriber=request.user)
        return redirect('tasks:user-page', pk=subscribe_to.pk)

class UserSubscribersView(ListView):
    model = Subscribe
    context_object_name = "subscribes"
    template_name = "tasks/subscribes.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.kwargs['pk']
        user = CustomUser.objects.get(pk=user_id)
        queryset = queryset.filter(user=user)
        return queryset

class UserSubscribersToView(ListView):
    model = Subscribe
    context_object_name = "subscribes"
    template_name = "tasks/subscribes-to.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.kwargs['pk']
        user = CustomUser.objects.get(pk=user_id)
        queryset = queryset.filter(subscriber=user)
        return queryset




