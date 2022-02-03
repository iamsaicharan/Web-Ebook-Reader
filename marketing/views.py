from django.http import HttpResponse
from django.views.generic import UpdateView
from django.shortcuts import render, redirect

from .forms import MarketingPreferenceForm
from .models import MarketingPreference

class MarketingPreferenceUpdateView(UpdateView):
    form_class = MarketingPreferenceForm
    template_name = 'base/forms.html'
    success_url = '/settings/email/'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/login')
        return super(MarketingPreferenceUpdateView, self).dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(**args, **kwargs)
        context["title"] = 'Update Marketing Preferences'
        return context
    

    def get_object(self):
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user)
        return obj