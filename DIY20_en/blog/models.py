from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
from datetime import date, datetime

class Category(models.Model):
    """Model representing a product category."""
    name = models.CharField(max_length=200, help_text='Enter one category for the product (e.g. Food)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this product."""
        return reverse('category-detail', args=[str(self.id)])


class Product(models.Model):
    """Model representing a product"""
    name = models.CharField(max_length=255, unique = True)

    description = models.TextField(help_text='Enter a description of the product')

    # ManyToManyField used because category can contain many products. Products can have several categories.
    # Category class has already been defined so we can specify the object above.
    category = models.ManyToManyField(Category, help_text='Select a category for this product')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this product."""
        return reverse('product-detail', args=[str(self.id)])    

    def display_category(self):
        """Create a string for the Category. This is required to display category in Admin."""
        return ', '.join(category.name for category in self.category.all()[:3])

    display_category.short_description = 'Category'


class Recipe(models.Model):
    """Model representing a recipe."""
    title = models.TextField(max_length=500)

    description = models.TextField(max_length=10000, help_text='Enter the recipe')

    # ManyToManyField used because recipe can contain many products. Products can be used in many recipes.
    # Product class has already been defined so we can specify the object above.
    product = models.ManyToManyField(Product, help_text='Select a product used for this recipe')

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this recipe."""
        return reverse('recipe-detail', args=[str(self.id)])

    def display_product(self):
        """Create a string for the Category. This is required to display category in Admin."""
        return ', '.join(product.name for product in self.product.all()[:3])

    display_product.short_description = 'Product'

class RecipeComment(models.Model):
    """
    Model representing a comment against a recipe post.
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    author = models.CharField(max_length=200, help_text='Author', default = "guest")
    description = models.TextField(max_length=1000)
    post_date = models.DateTimeField(default=datetime.now, blank=True)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        ordering = ["post_date"]

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.description
