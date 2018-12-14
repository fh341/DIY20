from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>', views.CategoryDetailView.as_view(), name='category-detail'),
    path('recipes/', views.RecipeListView.as_view(), name='recipes'),
    path('recipe/<int:pk>', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipe/<int:pk>/comment/', views.RecipeCommentCreate.as_view(), name='recipe_comment'),
    url(r'^recipe/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),

]
