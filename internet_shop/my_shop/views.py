from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render


products = [
    {
        "id": 1,
        "product": "Canon E500",
        "slug": "canon-e500",
        "available": False,
        "description": "some product description",
        "price": 50_000.00,
    },
    {
        "id": 2,
        "product": "Sony A7III",
        "slug": "sony-a7iii",
        "available": True,
        "description": "some product description",
        "price": 75_999.99
    },
]


def homepage(request: HttpRequest) -> HttpResponse:
    return render(request, 'homepage.html', {'products_list': products})


def product(request: HttpRequest, product: str) -> HttpResponse:
    for item in products:
        if item['slug'] == product:
            return render(request, 'product.html', {'info': item})
    raise Http404('No such product')
