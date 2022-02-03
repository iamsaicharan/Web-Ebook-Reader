from django.shortcuts import render, redirect
from .models import Library
from products.models import Product
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

@login_required
def library_home(request):
    library_obj, new_obj = Library.objects.new_or_get(request)
    # library = library_obj.products.all()
    # library_obj.save()
    print(new_obj)
    return render(request, 'library/home.html', {'library': library_obj})


@login_required
def library_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect('/library')
        library_obj, new_obj = Library.objects.new_or_get(request)
        if product_obj in library_obj.products.all():
            library_obj.products.remove(product_obj)
        else:    
            library_obj.products.add(product_obj)
            # library_obj.save()
        # return redirect(product_obj.get_absolute_url())
    return redirect('/library')