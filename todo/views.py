from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.forms import ModelForm
from django.contrib import messages
from .models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['task_text']

# Create your views here.
def index(request):
    tasks = Task.objects.order_by('created_at')
    form = TaskForm()
    return render(request, 'todo/index.html', {'tasks': tasks, 'form':form})

def new(request):
    if request.method == 'POST':
        f = TaskForm(request.POST)
        if f.is_valid():
            f.save()
            messages.info(request, 'Task created succesfully.')
            return redirect(reverse('todo:index'))
        else:
            messages.info(request, 'Failed to create Task.')
            return redirect(reverse('todo:index'))

def task(request, id):
    task_id = int(id)
    task = Task.objects.get(id=task_id)
    return render(request, 'todo/show.html', {'task': task})

def edit(request, id):
    task_id = int(id)
    task = Task.objects.get(id=task_id)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        messages.info(request, 'Task updated succesfully.')
        return redirect('todo:index')

    return render(request, 'todo/edit.html', {'form':form, 'id':task_id})

def delete(request, id):
    task_id = int(id)
    task = Task.objects.filter(id=task_id).delete()
    messages.info(request, 'Task deleted succesfully.')
    return redirect(reverse('todo:index'))

