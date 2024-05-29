from django.db.models import Q
from accounts.models import Profile
from task.models import Task
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import TaskForm


def get_filtered_tasks(request, tasks):
    status = request.GET.getlist('status')
    priority = request.GET.getlist('priority')
    due_date = request.GET.get('due_date')
    search = request.GET.get('search')

    if search:
        tasks = tasks.filter(Q(title__icontains=search) | Q(description__icontains=search))

    if status:
        tasks = tasks.filter(status__in=status)

    if priority:
        tasks = tasks.filter(priority__in=priority)

    if due_date:
        tasks = tasks.filter(due_date=due_date)

    return tasks


def check_task_permissions(request, task_id):
    current_profile = Profile.objects.get(user=request.user)
    task = get_object_or_404(Task, id=task_id)

        # Check if the user is authorized to update the task
    if task.created_by != current_profile and task.assigned_to != current_profile:
        messages.warning(request, 'You are not authorized to perform any action on this task.')
        return None
    
    # Check if the task is deleted
    if task.deleted:
        messages.warning(request, 'No such task exists.')
        return None

    return task


def base_context( tasks, is_favourites=False):
    return {
        'tasks': tasks,
        'is_favourites': is_favourites,
        'priority_choices': Task.PRIORITY_CHOICES,
        'status_choices': Task.STATUS_CHOICES,
    }

