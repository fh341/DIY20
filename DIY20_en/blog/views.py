from django.shortcuts import render
from blog.models import Product, Category, Recipe, RecipeComment
from django.views import generic
from django.contrib.auth.models import User #Recipe commenter
from django.shortcuts import get_object_or_404 
from django.contrib.auth.decorators import login_required

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_products = Product.objects.all().count()

    # The 'all()' is implied by default.    
    num_categories = Category.objects.count()

    num_recipes = Recipe.objects.all().count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_products': num_products,
        'num_categories': num_categories,
        'num_recipes' : num_recipes,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class ProductListView(generic.ListView):
    """
    Generic class-based view for a list of products.
    """
    model = Product
    paginate_by = 20
    ontext_object_name = 'my_product_list'   # your own name for the list as a template variable
    template_name = 'products/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    def get_queryset(self):
        return Product.objects.order_by('name')
    #def get_queryset(self):
        #return Product.objects.filter(name__icontains='oil')[:5] # Get 5 products containing the name oil

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ProductListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class ProductDetailView(generic.DetailView):
    """
    Generic class-based detail view for a product.
    """
    model = Product

class CategoryListView(generic.ListView):
    """
    Generic class-based view for a list of categories.
    """
    model = Category
    ontext_object_name = 'my_category_list'   # your own name for the list as a template variable
    template_name = 'categories/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    def get_queryset(self):
        return Category.objects.order_by('name')
    
class CategoryDetailView(generic.DetailView):
    """
    Generic class-based detail view for a category.
    """
    model = Category

class RecipeListView(generic.ListView):
    """
    Generic class-based view for a list of products.
    """
    model = Recipe
    paginate_by = 20
    ontext_object_name = 'my_recipe_list'   # your own name for the list as a template variable
    template_name = 'products/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    def get_queryset(self):
        return Recipe.objects.order_by('title')
    #def get_queryset(self):
        #return Product.objects.filter(name__icontains='oil')[:5] # Get 5 products containing the name oil

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(RecipeListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class RecipeDetailView(generic.DetailView):
    """
    Generic class-based detail view for a product.
    """
    model = Recipe

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse

class RecipeCommentCreate(CreateView):
    """
    Form for adding a blog comment. 
    """
    model = RecipeComment
    fields = ['author', 'description',]

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super(RecipeCommentCreate, self).get_context_data(**kwargs)
        # Get the recipe from id and add it to the context
        context['recipe'] = get_object_or_404(Recipe, pk = self.kwargs['pk'])
        return context
        
    def form_valid(self, form):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        #Add logged-in user as author of comment
        #form.instance.author = self.request.user
        #Associate comment with blog based on passed id
        form.instance.recipe=get_object_or_404(Recipe, pk = self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super(RecipeCommentCreate, self).form_valid(form)

    def get_success_url(self): 
        """
        After posting comment return to associated blog.
        """
        return reverse('recipe-detail', kwargs={'pk': self.kwargs['pk'],})

def add_comment_to_post(request, pk):
    post = get_object_or_404(Recipe, pk=pk)
    if request.method == "POST":
        form = RecipeComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('recipe_detail', pk=post.pk)
    else:
        form = RecipeComment()
    return render(request, 'recipe/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('recipe_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('recipe_detail', pk=comment.post.pk)
