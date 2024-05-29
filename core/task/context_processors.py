from .forms import TaskForm

def task_form(request):
    if request.user.is_authenticated:
        return {'form': TaskForm()}
    return {}