from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
# from django.core.mail import send_mail
# from django.template.loader import get_template
from django.conf import settings
import random
import string
from django.db.models.signals import pre_save, post_save

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_key_generator(instance):
    size = random.randint(30, 50)
    key = random_string_generator(size=size)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('email is must')
        if not password:
            raise ValueError('password is must')
        if not full_name:
            raise ValueError('full name is required')
        user_obj = self.model(
            email = self.normalize_email(email),
            full_name = full_name
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(
                email,
                full_name=full_name,
                password=password,
                is_staff=True,
                is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, null=False)
    is_active   = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

# Create your models here.

# class EmailActivation(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     email = models.EmailField()
#     key = models.CharField(max_length=150, blank=True, null=True)
#     activated = models.BooleanField(default = False)
#     forced_expired = models.BooleanField(default = False)
#     expires = models.IntegerField(default=1)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     update = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.email

#     def regenerate(self):
#         self.key = None
#         self.save()
#         if self.key is not None:
#             return True
#         return False

#     def send_activation(self):
#         if not self.activated and not self.forced_expired:
#             if self.key:
#                 base_url = getattr(settings, 'BASE_URL', '127.0.0.1:8000')
#                 key_path = self.key
#                 path = '{base}{path}'.format(base=base_url, path=key_path)
#                 context = {
#                     'path': path,
#                     'email': self.email
#                 }
#                 txt_ = get_template('registration/emails/verity.txt').render(context)
#                 html_ = get_template('registration/emails/verity.html').render(context)
#                 subject = 'TendeRead email verification'
#                 from_email = settings.DEFAULT_FROM_EMAIL
#                 recipient_list = [self.email]
#                 sent_mail = send_mail(
#                     subject,
#                     txt_,
#                     from_email,
#                     recipient_list,
#                     html_message=html_,
#                     fail_silently=False,
#                 )
#                 return sent_mail
#         return False


# def pre_save_email_activation(sender, instance, *args, **kwargs):
#     if not instance.activated and not instance.forced_expired:
#         if not instance.key:
#             instance.key = unique_key_generator(instance)

# pre_save.connect(pre_save_email_activation, sender=EmailActivation)


# def post_save_user_create_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         obj = EmailActivation.objects.create(user=instance, email=instance.email)
#         obj.send_activation()

# post_save.connect(post_save_user_create_receiver, sender=User)