from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic import CreateView, FormView, DetailView, TemplateView
from django.contrib.auth import authenticate, login, get_user_model
from .forms import ContactForm
from products.models import Product, RecentlyAdded, Top25, TrendingNow, PopularOnTendeRead
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.dispatch import Signal
from django.contrib import messages

def home_page(request):
    content = {
        
    }
    if request.user.is_authenticated:
        content['account'] = 'Premium'
    return render(request, 'home_page.html', content)

@method_decorator(login_required, name='dispatch')
class HomePage1(ListView):
    # queryset = Product.objects.all()
    template_name = 'home_page.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        print(Product.objects.all())
        print(RecentlyAdded.objects.all().prefetch_related('book'))
        return RecentlyAdded.objects.all()

@method_decorator(login_required, name='dispatch')
class HomePage(TemplateView):
    template_name = 'home.html'
    def get_context_data(self,*args, **kwargs):
        context = super(HomePage, self).get_context_data(*args, **kwargs)
        context["recently_added"] = RecentlyAdded.objects.all()
        context['popular_on_tenderead'] = PopularOnTendeRead.objects.all()
        context['trending_now'] = TrendingNow.objects.all()
        context['top25'] = Top25.objects.all()
        return context

def index_view1(request):
    recently_added = RecentlyAdded.objects.all()
    popular_on_tenderead = PopularOnTendeRead.objects.all()
    trending_now = TrendingNow.objects.all()
    top25 = Top25.objects.all()
    context = {
        'recently_added': recently_added, 
        'popular_on_tenderead': popular_on_tenderead,
        'trending_now': trending_now,
        'top25': top25
        
        }
    return render(request,'home.html', context)

def about_page(request):
    context = {
        'title': 'About TendeRead',
        'content': 'This is TendeRead, a user friendly library in your pocket. Read any book, any time and any where at free.'
    }
    return render(request, 'info.html', context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'title': 'Contact TendeRead',
        'content': 'email us for more details',
        'form': contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    return render(request, 'contact/view.html', context)
