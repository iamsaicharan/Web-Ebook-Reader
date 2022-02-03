
from django.contrib import admin
from django.urls import path


from django.conf import settings
from django.conf.urls.static import static

from .views import product_list_view, ProductListView, product_detail_view, ProductDetailSlugView, ProductDetailView, ProductFeaturedDetailView, ProductFeaturedListView


urlpatterns = [
    path('products/', ProductListView.as_view()),
    # path('featured/', ProductFeaturedListView.as_view()),
    # path('featured/<int:pk>/', ProductFeaturedDetailView.as_view()),

    # re_path(r'^products/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view()),

    # path('products-fbv/', product_list_view),
    path('products/<int:pk>/', ProductDetailView.as_view()),
    # path('products-fbv/<int:pk>/', product_detail_view),
]
