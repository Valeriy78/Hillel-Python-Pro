"""
My_shop application views
"""

from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render

from .models import Product, Category


def homepage(request: HttpRequest) -> HttpResponse:
    """Homepage view implementation"""

    products = Product.objects.all()
    categories = Category.objects.all()
    if request.method == "GET":
        category_slug = request.GET.get('category')
        if category_slug:
            products = products.filter(category=Category.objects.get(slug=category_slug))
    context = {'products_list': products, 'categories_list': categories}
    return render(request, 'homepage.html', context)


def product(request: HttpRequest, product: str) -> HttpResponse:
    """Product view implementation"""

    try:
        context = {'info': Product.objects.get(slug=product)}
        return render(request, 'product.html', context)
    except Product.DoesNotExist:
        raise Http404('No such product')
