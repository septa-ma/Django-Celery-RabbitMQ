# 2- build a function for submitting the email form.
from app_email.forms import SuggestionForm
from django.views.generic.edit import FormView
from django.http import HttpResponse

class SuggestionEmailView(FormView):
    template_name = 'suggestion.html'
    form_class = SuggestionForm
    
    def form_valid(self, form):
        form.send_email()
        msg = "thanks for your suggestion."
        return HttpResponse(msg)
