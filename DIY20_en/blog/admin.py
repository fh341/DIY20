from django.contrib import admin
from blog.models import Product, Category, Recipe, RecipeComment

# Register the Admin classes for Product using the decorator
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Administration object for Product models. 
    Defines:
     - fields to be displayed in list view (list_display)
    """
    list_display = ('name', 'display_category',)
    list_filter = ('category',)

# Register the Admin class for Category 
admin.site.register(Category)

class CategoryAdmin(admin.ModelAdmin):
    """
    Administration object for Category models. 
    Defines:
     - fields to be displayed in list view (list_display)
    """
    list_display = ('name',)

admin.site.register(RecipeComment)
admin.site.register(Recipe)

class RecipeCommentsInline(admin.TabularInline):
    """
    Used to show 'existing' comments inline below associated recipes
    """
    model = RecipeComment
    max_num=0


class RecipeAdmin(admin.ModelAdmin):
    """
    Administration object for Category models. 
    Defines:
     - fields to be displayed in list view (list_display)
    """
    list_display = ('title', 'display_product',)
    inlines = [RecipeCommentsInline]
