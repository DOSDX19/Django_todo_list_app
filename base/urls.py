from django.urls import path 
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.TaskList.as_view(), name = "tasks"),
    path("task/<int:pk>", views.TaskDetail.as_view() , name="task"),
    path("add-task", views.CreatTask.as_view(), name="add-task"),
    path("update-task/<int:pk>", views.UpdateTask.as_view(), name="update-task"),
    path("delete-task/<int:pk>", views.DeleteTask.as_view(), name="delete-task"),
    path("login", views.Login.as_view(), name="login"),
    path("logout", LogoutView.as_view(next_page="login"), name="logout"),
    path("register",views.Register.as_view(), name="register")
]
