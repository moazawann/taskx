from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

from task.models import Task, Favourite, Comment
from accounts.models import Profile
from .forms import TaskForm
from .utils import get_filtered_tasks, check_task_permissions, base_context


@login_required
def get_current_profile(request):
    return request.user.profile


@login_required
def dashboard_page(request):
    current_profile = get_current_profile(request)
    tasks = Task.objects.filter(
        (Q(created_by=current_profile) | Q(assigned_to=current_profile)) & Q(deleted=False)
    )

    tasks = get_filtered_tasks(request, tasks)
    context = base_context( tasks)

    return render(request, 'task/dashboard.html', context)


@login_required
def mytasks(request):
    current_profile = get_current_profile(request)
    tasks = Task.objects.filter(assigned_to=current_profile, deleted=False)

    tasks = get_filtered_tasks(request, tasks)
    context = base_context(tasks)

    return render(request, 'task/mytasks.html', context)


@login_required
def myfavourites(request):
    current_profile = get_current_profile(request)
    fav_tasks = Favourite.objects.filter(
        profile_id=current_profile, favourite=True
    ).values_list('task_id', flat=True)
    
    tasks = Task.objects.filter(id__in=fav_tasks, deleted=False)
    tasks = get_filtered_tasks(request, tasks)
    context = base_context(tasks, is_favourites=True)

    return render(request, 'task/myfavourites.html', context)


@login_required
def add_task(request):
    current_profile = get_current_profile(request)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = current_profile
            task.updated_by = current_profile
            task.save()
            messages.success(request, 'Task Added Successfully.')
            return redirect('dashboard_page')

    return redirect('dashboard_page')


@login_required
def update_task(request, task_id):
    current_profile = get_current_profile(request)
    task = check_task_permissions(request, task_id)

    if task is None:
        return redirect('dashboard_page')

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.updated_by = current_profile
            task.save()
            messages.success(request, 'Task Updated Successfully.')
            return redirect('task_details', task_id)
    else:
        form = TaskForm(instance=task)

    return render(request, 'task/updatetask.html', {'update_form': form, 'task': task})


@login_required
def delete_task(request, task_id):
    current_profile = get_current_profile(request)
    task = check_task_permissions(request, task_id)

    if task is None:
        return redirect('dashboard_page')
    
    task.updated_by = current_profile
    task.deleted = True
    task.save()
    messages.success(request, 'Task Deleted Successfully.')

    return redirect('dashboard_page')


@login_required
def task_details(request, id):
    task = check_task_permissions(request, id)
    if task is None:
        return redirect('dashboard_page')

    current_profile = get_current_profile(request)
    comments_queryset = Comment.objects.filter(task_id=id, is_deleted=False).order_by('-updated_at')

    if request.method == 'POST':
        comment = request.POST.get('comment')
        Comment.objects.create(
            task_id=task,
            profile_id=current_profile,
            comment=comment,
            created_by=current_profile,
            updated_by= current_profile,
        )
        return redirect('task_details', id=id)

    context = {
        'comments': comments_queryset,
        'task': task,
    }

    return render(request, 'task/task_details.html', context)



@login_required
def makefavourite(request, task_id):
    current_profile = get_current_profile(request)

    task = check_task_permissions(request, task_id)
    if task is None:
        return redirect('dashboard_page')
    
    fav_task = Favourite.objects.filter(task_id=task_id, profile_id=current_profile).first()

    if fav_task:
        if fav_task.favourite == True:
             messages.warning(request, 'Task is Already in Favourites')
        else:
            fav_task.favourite = True
            fav_task.save()
            messages.success(request, 'Task Added to Favourites.')

    else:
        Favourite.objects.create(
            task_id=task,
            profile_id=current_profile,
            favourite=True,
        )
        messages.success(request, 'Task Added to Favourites.')

    return redirect('dashboard_page')


@login_required
def removefavourite(request, task_id):
    task = check_task_permissions(request, task_id)
    if task is None:
        return redirect('my_favourites')

    current_profile = Profile.objects.get(user=request.user.id)
    fav_task = Favourite.objects.get(task_id=task_id, profile_id=current_profile)
    fav_task.favourite = False
    fav_task.save()
    messages.success(request, 'Removed from Favourites')

    return redirect('my_favourites')


@login_required
def delete_comment(request, task_id, comment_id):
    current_profile = get_current_profile(request)
    comment_obj = Comment.objects.get(id=comment_id)

    if comment_obj.created_by != current_profile:
        messages.warning(request, 'You are not allowed to perform any action on this comment.')
        return redirect('task_details', id=task_id)
    
    else:
        comment_obj.is_deleted = True
        comment_obj.save()
        messages.success(request, 'Comment deleted successfully.')
        return redirect('task_details', id=task_id)

    
@login_required
def update_comment(request, task_id, comment_id):
    current_profile = get_current_profile(request)
    comment_obj = Comment.objects.get(id=comment_id)

    if comment_obj.created_by != current_profile:
        messages.warning(request, 'You are not allowed to perform any action on this comment.')
        return redirect('task_details', id=task_id)
    
    else:
        if request.method == 'POST':
            comment_update = request.POST.get('update_comment')
            comment_obj.comment = comment_update
            comment_obj.updated_by = current_profile
            messages.success(request, 'Comment updated successfully.')
            comment_obj.save()

    return redirect('task_details', id=task_id)


@login_required
def calendar(request):
    current_profile = get_current_profile(request)
    tasks = Task.objects.filter(
        (Q(created_by=current_profile) | Q(assigned_to=current_profile)) & Q(deleted=False)
    )

    context = {
        'tasks': tasks,
        'form': TaskForm()
    }

    return render(request, 'task/calendar.html', context)

