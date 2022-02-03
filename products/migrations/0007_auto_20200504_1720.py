# Generated by Django 3.0.5 on 2020-05-04 11:50

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20200427_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='unzipped',
            field=models.FileField(blank=True, null=True, upload_to=products.models.upload_ebook_path),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
