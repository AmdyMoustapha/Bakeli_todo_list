from base import models
from turtle import title
from .models import Task
from dataclasses import fields
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# --------------------------------------api fonction
from rest_framework import viewsets

from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from django.http import JsonResponse

from.serializers import TaskSerializer

# ---------------------------------------------------------------------------django api rest class


# class TaskViewsets(viewsets.ModelViewSet):
#     #queryset = Task.objects.all().order_by()
#     queryset = models.Task.objects.all()
#     serializer_class = TaskSerializer
# ---------------------------------------------------------------------------django api rest fonction


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'all_tasks': '/',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/task/pk/delete',
        # 'Task-detail': '/task-detail/pk',
    }

    return Response(api_urls)


@api_view(['GET'])
def view_tasks(request):

    # checking for the parameters from the URL
    if request.query_params:
        tasks = Task.objects.filter(**request.query_param.dict())
    else:
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)

    # if there is something in items else raise error
    if tasks:
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def taskDetail(request, pk):
    tasks = Task.objects.get(id=pk)
    serializer = TaskSerializer(tasks, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def add_tasks(request):
    task = TaskSerializer(data=request.data)

    # validating for already existing data
    if Task.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if task.is_valid():
        task.save()
        return Response(task.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_tasks(request, pk):
    task = Task.objects.get(pk=pk)
    data = TaskSerializer(instance=task, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_tasks(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


# ---------------------------------------------------------------------------django todo list


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = ['title', 'description', 'complete']
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
