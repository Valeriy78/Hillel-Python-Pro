from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render

from .models import Product


def homepage(request: HttpRequest) -> HttpResponse:
    context = {'products_list': Product.objects.all()}
    return render(request, 'homepage.html', context)


def product(request: HttpRequest, product: str) -> HttpResponse:
    try:
        context = {'info': Product.objects.get(slug=product)}
        return render(request, 'product.html', context)
    except Product.DoesNotExist:
        raise Http404('No such product')
