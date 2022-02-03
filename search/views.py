from django.db.models import Q
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from products.models import Product

# Create your views here.
@method_decorator(login_required, name='dispatch')
class SearchProductView(ListView):
    # queryset = Product.objects.all()
    template_name = 'search/view.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        print(request.GET)
        query = request.GET.get('q')
        if query is not None:
            lookups = Q(title__icontains=query) | Q(description__icontains=query) | Q(category__title__icontains=query)
            return Product.objects.filter(lookups).distinct()
        else:
            return Product.objects.none()



