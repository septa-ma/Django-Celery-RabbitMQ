# 1- create forms.py and make a form for sending email.
from django import forms
from app_email.tasks import send_suggestion_email_task

class SuggestionForm(forms.Form):
    name = forms.CharField(label='firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'firstname', 'id': 'form-firstname'}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email'}))
    suggestion = forms.CharField(label="Suggestion", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}))

    # 3- make the send_email function.
    # it's the task which send to celery to run.
    def send_email(self):
        # 'send_suggestion_email_task' -> it's the actual task name that will be run.
        send_suggestion_email_task.delay(
            self.cleaned_data['name'], 
            self.cleaned_data['email'], 
            self.cleaned_data['suggestion']
        )
