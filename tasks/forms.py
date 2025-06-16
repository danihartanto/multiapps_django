from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date', 'is_completed']
