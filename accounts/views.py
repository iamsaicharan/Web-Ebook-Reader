from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic import CreateView, FormView, DetailView
from django.contrib.auth import authenticate, login, get_user_model
from .forms import LoginForm, RegisterForm
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.dispatch import Signal
from django.contrib import messages

# user_logged_in = Signal(providing_args=['instance', 'request'])
user_logged_in = Signal()

# @login_required
# def account_home_view(request):
#     return render(request, 'account_home.html', {})
    
# @method_decorator(login_required, name='dispatch')
# class AccountHomeView(DetailView):
#     template_name = 'account_home.html'
#     def get_object(self):
#         return self.request.user

class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'auth/login.html'

    def form_valid(self, form):
        request = self.request
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        print(user)
        print(request.user.is_authenticated)
        if user is not None:
            # if not user.is_active:
            #     messages.error(request, 'Inactive User')
            #     return super(LoginView, self).form_invalid(form)

            print(request.user.is_authenticated)
            login(request, user)
            user_logged_in.send(user.__class__, instance=user,  request=request)
            return redirect('/')
        else:
            print('error')
        return super(LoginView, self).form_invalid(form)

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'auth/register.html'
    success_url = '/login/'