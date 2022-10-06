"""Purchase application views"""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from .forms import CartItemForm, ConfirmForm
from .models import Cart, CartItem, Order, OrderReturn
from my_shop.models import Product
from internet_shop.decorators import is_staff, is_not_staff


@require_http_methods(["GET", "POST"])
@login_required
@is_not_staff
def cart_item_create_view(request: HttpRequest, slug) -> HttpResponse:
    """CartItem create view implementation"""

    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        raise Http404("The product not found")

    if request.method == "POST":
        form = CartItemForm(request.POST, initial={"product_id": product.id, "quantity": 0})
        if form.is_valid():
            quantity = form.cleaned_data["quantity"]
            user = request.user
            cart = user.carts.get(is_actual=True)
            cart_item = CartItem(product=product, quantity=quantity, cart=cart)
            cart_item.save()
            redirect_url = reverse_lazy("homepage")
            return HttpResponseRedirect(redirect_url)
    else:
        form = CartItemForm(initial={"product_id": product.id, "quantity": 0})

    return render(request, "add_to_cart.html", {"form": form})


@login_required
@is_not_staff
def cart_item_delete_view(request: HttpRequest, pk: int) -> HttpResponse:
    """CartItem delete view implementation"""

    try:
        item = CartItem.objects.get(id=pk)
    except CartItem.DoesNotExist:
        raise Http404("The item not found")
    item.delete()
    return HttpResponseRedirect(reverse_lazy("cart_list"))


@login_required
@is_not_staff
def cart_list_view(request: HttpRequest) -> HttpResponse:
    """Cart content list view implementation"""

    user = request.user
    cart = user.carts.get(is_actual=True)
    total_cost = cart.calculate_sum
    context = {"cart_id": cart.id, "object_list": cart.items.all(), "total_cost": total_cost}
    return render(request, "cart_list.html", context)


@require_http_methods(["GET", "POST"])
@login_required
@is_not_staff
def purchase_view(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Customer's order create view implementation.
    """

    try:
        cart = Cart.objects.get(id=pk)
    except Cart.DoesNotExist:
        raise Http404("The cart not found")

    customer = cart.customer
    cart_items = cart.items.all()
    redirect_url = reverse_lazy("homepage")
    if cart_items.count() == 0:
        return HttpResponseRedirect(redirect_url)

    if request.method == "POST":

        total_cost = cart.calculate_sum()
        if total_cost > customer.money:
            message = "You have not enough money!"
            return render(request, "confirm_purchase.html", {"message": message})

        new_order = Order(cart=cart)
        new_order.save()
        return HttpResponseRedirect(redirect_url)

    else:
        return render(request, "confirm_purchase.html")


@login_required
@is_not_staff
def order_list_view(request: HttpRequest) -> HttpResponse:
    """Order list view implementation"""

    customer = request.user
    carts = customer.carts.filter(is_actual=False)
    orders = Order.objects.filter(cart__in=carts)
    context = {"object_list": orders}
    return render(request, "order_list.html", context)


@login_required
@is_not_staff
def order_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    """Order detail view implementation"""

    try:
        order = Order.objects.get(id=pk)
        context = {"object": order, "items": order.cart.items.all()}
        return render(request, "order.html", context)
    except Order.DoesNotExist:
        raise Http404("The order not found")


@require_http_methods(["GET", "POST"])
@login_required
@is_not_staff
def order_return_request_view(request: HttpRequest, pk: int) -> HttpResponse:
    """Implementation of the order return request view"""

    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        raise Http404("The order not found")

    redirect_url = reverse_lazy("order_list")

    if request.method == "POST":
        try:
            if OrderReturn.objects.get(order=order):
                return HttpResponseRedirect(redirect_url)
        except OrderReturn.DoesNotExist:
            order_return = OrderReturn(order=order)
            order_return.save()
            return HttpResponseRedirect(redirect_url)
    else:
        return render(request, "request_order_return.html")


@login_required
@is_staff
def order_return_list_view(request: HttpRequest) -> HttpResponse:
    """Implementation of the order return list view"""

    context = {"object_list": OrderReturn.objects.filter(status=False)}
    return render(request, "order_return_list.html", context)


@login_required
@is_staff
def order_return_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    """Implementation of the order return detail view"""

    try:
        order_return = OrderReturn.objects.get(id=pk)
        items = order_return.order.cart.items.all()
        context = {"object": order_return, "items": items}
        return render(request, "order_return.html", context)
    except OrderReturn.DoesNotExist:
        raise Http404("The order return request not found")


@require_http_methods(["GET", "POST"])
@login_required
@is_staff
def confirm_order_return_view(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Implementation of the order return request confirmation view.
    """

    try:
        order_return = OrderReturn.objects.get(id=pk)
    except OrderReturn.DoesNotExist:
        raise Http404("The order return request not found")

    redirect_url = reverse_lazy("return_order_list")

    if request.method == "POST":

        form = ConfirmForm(request.POST)
        if form.is_valid():
            decision = form.cleaned_data["decision"]

            if decision == "CONFIRM":
                order_return.confirm()
            else:
                order_return.reject()

            return HttpResponseRedirect(redirect_url)

    else:
        form = ConfirmForm()

    return render(request, "confirm_order_return.html", {"form": form})
