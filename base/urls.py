from django.contrib.auth.views import LogoutView
from django.urls import include, path

from knox import views as knox_views
from .views import LoginAPI
# from rest_framework import routers
from . import views

from.views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage, RegisterAPI


# router = routers.DefaultRouter()   utilisé pour les class
# router.register('tasks', views.TaskViewsets)   utilisé pour les class


urlpatterns = [

    # path('', include(router.urls)),  # utilisé pour les class
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # ----------------------api class path------------------------------------------
    path('login/', LoginAPI.as_view(), name='Connexion'),
    path('logout/', knox_views.LogoutView.as_view(), name='Déconnxion'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='Tout déconnecter'),

    # ----------------------api fonction path------------------------------------------
    path('register/', RegisterAPI.as_view(), name='register'),
    path('', views.apiOverview, name='home'),
    path('all/', views.view_tasks, name='view_tasks'),
    path('task-detail/<int:pk>/', views.taskDetail, name="task-detail"),
    path('create/', views.add_tasks, name='add-tasks'),
    path('update/<int:pk>/', views.update_tasks, name='update-tasks'),
    path('task/<int:pk>/delete/', views.delete_tasks, name='delete-Tasks'),

    # ----------------------todolist---------------------------------------------------
    # path('login/', CustomLoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    # path('register/', RegisterPage.as_view(), name='register'),

    # path('', TaskList.as_view(), name='tasks'),
    # path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    # path('task-create/', TaskCreate.as_view(), name='task-create'),
    # path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    # path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
]
