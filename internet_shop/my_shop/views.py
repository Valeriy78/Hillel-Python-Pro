from django.http import HttpRequest, HttpResponse
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

user = {
    "id": 1,
    "username": "shorodilov",
    "first_name": "Serhii",
    "last_name": "Horodilov"
}


def homepage(request: HttpRequest) -> HttpResponse:
    products_list = []
    for item in products:
        products_list.append({'product': item['product'], 'slug': item['slug']})
    return render(request, 'homepage.html', {'products_list': products_list})


def product(request: HttpRequest, product: str) -> HttpResponse:
    for item in products:
        if item['slug'] == product:
            info = item
    return render(request, 'product.html', {'info': info})


def user_profile(request: HttpRequest) -> HttpResponse:
    return render(request, 'user.html', user)
