from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed
from products.models import Product

User = settings.AUTH_USER_MODEL

class LibraryManager(models.Manager):
    def new_or_get(self, request):
        library_id = request.session.get('library_id', None)
        qs = self.get_queryset().filter(id=library_id)
        if qs.count() == 1:
            new_obj = False
            library_obj = qs.first()
            if request.user.is_authenticated and library_obj is None:
                user_library = self.model.objects.filter(user=request.user).first()
                if user_library is not None:
                    library_obj.products.add(*user_library.products.all())
                    library_obj.user = request.user
                    library_obj.save()
                    user_library.delete()
                else:
                    library_obj.user = request.user
                    library_obj.save()
        else:
            library_obj = Library.objects.new(user=request.user)
            new_obj = True
            request.session['library_id'] = library_obj.id
        return library_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                library_obj = self.model.objects.filter(user=user).first()
                if library_obj is not None:
                    return library_obj
                user_obj = user
        return self.model.objects.create(user=user_obj)



# Create your models here.
class Library(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)

    objects = LibraryManager()

    def save(self, *args, **kwargs):
        super(Library, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)
    

# def m2m_changed_library_receiver(sender, instance, action, *args, **kwargs):
#     if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
#         products = instance.products.all()
#         instance.save()
# m2m_changed.connect(m2m_changed_library_receiver, sender=Library.products.through)


# def pre_save_library_receiver(sender, instance, *args, **kwargs):
#     # print(action)
#     # print(instance.products.all())
#     library = instance.products.all()

# # m2m_changed.connect(pre_save_library_receiver, sender=Library.products.through)

# pre_save.connect(pre_save_library_receiver, sender=Library)
