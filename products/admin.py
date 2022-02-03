from django.contrib import admin
from .models import Product, RecentlyAdded, TrendingNow, PopularOnTendeRead, Top25

class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']
    class Meta:
        model = Product

# Register your models here.
admin.site.register(Product)
admin.site.register(RecentlyAdded)
admin.site.register(TrendingNow)
admin.site.register(PopularOnTendeRead)
admin.site.register(Top25)