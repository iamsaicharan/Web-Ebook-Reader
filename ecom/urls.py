"""ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include



from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from products.views import product_list_view, ProductListView, product_detail_view, ProductDetailSlugView, ProductDetailView, ProductFeaturedDetailView, ProductFeaturedListView, Reader, CategoryView
from django.contrib.auth.views import LogoutView
from search.views import SearchProductView
from .views import home_page, about_page, contact_page, HomePage
from accounts.views import LoginView, RegisterView
# , AccountHomeView, account_home_view
from library.views import library_home, library_update
from membership.views import membership_page
from marketing.views import MarketingPreferenceUpdateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage.as_view()),
    path('about/', about_page),
    path('contact/', contact_page),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('register/', RegisterView.as_view()),
    path('settings/email/', MarketingPreferenceUpdateView.as_view()),
    # path('account/', AccountHomeView.as_view()),
    # path('accounts/', include('accounts.passwords.urls')),
    path('products/', ProductListView.as_view()),
    path('library_update/', library_update),
    path('search/', SearchProductView.as_view()),
    path('category/', CategoryView.as_view()),
    # path('membership/', membership_page),
    path('library/', library_home),
    path('products/<int:pk>/reader', Reader),
    path('products/<int:pk>/', ProductDetailView.as_view()),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)