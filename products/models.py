import random
import os
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
import ebooklib
from ebooklib import epub
from PIL import Image
import shutil
import urllib
import zipfile
from category.models import Category
from language.models import Language


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_ebook_path(instance, filename):
    # print(instance)
    # print(filename)
    new_filename = random.randint(1, 545646612323)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return 'products/{new_filename}/{final_filename}'.format(new_filename=new_filename, final_filename=final_filename)

class ProductManager(models.Manager):
    def featured(self):
        return self.get_queryset().filter(featured=True)
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=150, blank=True)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)
    ebook = models.FileField(upload_to=upload_ebook_path, null=True, blank=True)
    cover_image = models.ImageField(upload_to=upload_ebook_path, null=True, blank=True)
    author = models.TextField(blank=True)
    category = models.ManyToManyField(Category, blank=False)
    # language = models.ManyToManyField(Language, blank=False)
    language = models.ForeignKey(Language, null=True, blank=True, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.id:
            book = epub.read_epub(self.ebook)
            description = book.get_metadata('DC', 'description')
            title = book.get_metadata('DC', 'title')
            author = book.get_metadata('DC', 'creator')
            try:
                self.description = description[0][0]
                self.title = title[0][0]
                self.author = author[0][0]
            except Exception as e:
                pass

            new_folder_name = random.randint(0, 68764446643313679)
            folder_unzip = os.path.join(settings.MEDIA_ROOT, 'Unzipped')
            file_path = os.path.join(folder_unzip, str(new_folder_name))
            zip_file = zipfile.ZipFile(self.ebook)
            zip_file.extractall(file_path)
            for root, dirs, files in os.walk(file_path):
                for directory in dirs:
                    for filename in directory:
                        filename = os.path.join(root, filename)
                        if ("cover.png" in filename) or ("cover.jpeg" in filename) or ("cover.jpg" in filename):
                            path = os.path.join(root, filename)
                            path = path.replace('\\', '/')
                            print(path)
                            path1 = os.path.relpath(path, settings.MEDIA_ROOT)
                            self.cover_image = path1
                            break
                        else:
                            print('no')
                
                for filename in files:
                    if ("cover.png" in filename) or ("cover.jpeg" in filename) or ("cover.jpg" in filename):
                        path = os.path.join(root, filename)
                        path = path.replace('\\', '/')
                        print(path)
                        path1 = os.path.relpath(path, settings.MEDIA_ROOT)
                        self.cover_image = path1
                        break
                    else:
                        print('no')

            # path1 = os.path.relpath(path, settings.MEDIA_ROOT)
            # self.cover_image = path1

            super(Product, self).save(*args, **kwargs)
            
    objects = ProductManager()

    def get_absolute_url(self):
        return '/products/{pk}/'.format(pk=self.pk)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_stamp']

# def product_pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.pk:

    
class RecentlyAdded(models.Model):
    book = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title

class PopularOnTendeRead(models.Model):
    popular_book = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.popular_book.title

class TrendingNow(models.Model):
    trending_book = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.trending_book.title

class Top25(models.Model):
    top25_book = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.top25_book.title
    

