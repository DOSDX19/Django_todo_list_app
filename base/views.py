from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView,CreateView
from django.views.generic.edit import UpdateView , DeleteView
from .models import Task
from .forms import TaskForm , RegisterForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.mail import send_mail
from todo_list import settings
# Create your views here.


class Register(CreateView):
    template_name = "base/register.html"
    form_class = RegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        user = form.save()
        email = [self.request.POST['email']] or ''
        username = self.request.POST['username'] or ''
        send_mail("Welcome" , "Hello " + username , settings.EMAIL_HOST_USER , email, fail_silently=True)
        print(email)
        login(self.request , user)
        if user is not None :
            return super().form_valid(form)


    def get(self ,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super().get(*args, **kwargs)


class Login(LoginView):
    template_name = "base/login.html"
    fields = "__all__"
    redirect_authenticated_user = True 

    def get_success_url(self) :
        return reverse_lazy("tasks")


class TaskList(LoginRequiredMixin , ListView):
    template_name = "base/task_list.html"
    context_object_name = "list"
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = context['list'].filter(user= self.request.user)
        context['count'] = context['list'].filter(complete = False).count()

        search = self.request.GET.get('search-area') or ''
        if search :
            context['list'] = context['list'].filter(title__startswith=search)
            context['search'] = search 
            
        return context

        


class TaskDetail(LoginRequiredMixin , DetailView):
    template_name = "base/detail_list.html"
    model = Task
    context_object_name = "item"


class CreatTask(LoginRequiredMixin , CreateView):
    template_name = "base/list_form.html"
    form_class = TaskForm
    context_object_name = "form"
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UpdateTask(LoginRequiredMixin , UpdateView):
    template_name = "base/list_form.html"
    model = Task
    fields = "__all__"
    context_object_name = "form"
    success_url = "/"
    


class DeleteTask( LoginRequiredMixin , DeleteView):
    template_name = "base/delete_task.html"
    model = Task
    fields = "__all__"
    context_object_name = "task"
    success_url = reverse_lazy("tasks")