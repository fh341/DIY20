# Generated by Django 2.1.2 on 2018-11-19 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter one category for the product (e.g. Food)', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(help_text='Enter a description of the product')),
                ('category', models.ManyToManyField(help_text='Select a category for this product', to='blog.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=500)),
                ('description', models.TextField(help_text='Enter the recipe', max_length=10000)),
                ('product', models.ManyToManyField(help_text='Select a product used for this recipe', to='blog.Product')),
            ],
        ),
    ]
