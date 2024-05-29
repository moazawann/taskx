from django import forms
from .models import Task
from datetime import date

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'due_date', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Description', 'rows': '8'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        
        today = date.today().strftime('%Y-%m-%d')
        self.fields['due_date'].widget.attrs['min'] = today
        self.fields['assigned_to'].required = True
        self.fields['assigned_to'].empty_label = 'Select'
