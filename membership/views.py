from django.shortcuts import render

# Create your views here.

def membership_page(request):
    content = {
        
    }
    if request.user.is_authenticated:
        content['account'] = 'Premium'
    return render(request, 'membership/membership.html', content)