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
@is_not_staff
@login_required
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


@is_not_staff
@login_required
def cart_item_delete_view(request: HttpRequest, pk: int) -> HttpResponse:
    """CartItem delete view implementation"""

    try:
        item = CartItem.objects.get(id=pk)
    except CartItem.DoesNotExist:
        raise Http404("The item not found")
    item.delete()
    return HttpResponseRedirect(reverse_lazy("cart_list"))


@is_not_staff
@login_required
def cart_list_view(request: HttpRequest) -> HttpResponse:
    """Cart content list view implementation"""

    user = request.user
    cart = user.carts.get(is_actual=True)
    total_cost = cart.calculate_sum
    context = {"cart_id": cart.id, "object_list": cart.items.all(), "total_cost": total_cost}
    return render(request, "cart_list.html", context)


@require_http_methods(["GET", "POST"])
@is_not_staff
@login_required
def purchase_view(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Customer's order create view implementation.
    After the purchase confirmation:
    1. Calculates the total cost of products.
    2. Gets from the user's account an amount of money equal to the total cost.
    3. Creates new order object.
    4. Diminishes the quantity of products that have been purchased.
    5. Current user's cart becomes inactual.
    6. Creates new actual cart for the user.
    """

    try:
        cart = Cart.objects.get(id=pk)
    except Cart.DoesNotExist:
        raise Http404("The cart not found")
    customer = cart.customer
    redirect_url = reverse_lazy("homepage")
    cart_items = cart.items.all()
    if cart_items.count() == 0:
        return HttpResponseRedirect(redirect_url)

    if request.method == "POST":

        total_cost = cart.calculate_sum()
        if total_cost <= customer.money:
            customer.get_money(total_cost)
        else:
            message = "You have not enough money!"
            return render(request, "confirm_purchase.html", {"message": message})

        new_order = Order(customer=customer, cart=cart)
        new_order.save()

        for item in cart_items:
            product = item.product
            quantity = item.quantity
            product.decrease_quantity(quantity)

        cart.make_inactual()
        new_cart = Cart(customer=customer)
        new_cart.save()

        return HttpResponseRedirect(redirect_url)

    else:
        return render(request, "confirm_purchase.html")


@is_not_staff
@login_required
def order_list_view(request: HttpRequest) -> HttpResponse:
    """Order list view implementation"""

    customer = request.user
    context = {"object_list": customer.orders.all()}
    return render(request, "order_list.html", context)


@is_not_staff
@login_required
def order_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    """Order detail view implementation"""

    try:
        order = Order.objects.get(id=pk)
        context = {"object": order, "items": order.cart.items.all()}
        return render(request, "order.html", context)
    except Order.DoesNotExist:
        raise Http404("The order not found")


@require_http_methods(["GET", "POST"])
@is_not_staff
@login_required
def order_return_request_view(request: HttpRequest, pk: int) -> HttpResponse:
    """Implementation of the order return request view"""

    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        raise Http404("The order not found")

    customer = order.customer

    if request.method == "POST":
        order_return = OrderReturn(customer=customer, order=order)
        order_return.save()
        return HttpResponseRedirect(reverse_lazy("order_list"))
    else:
        return render(request, "request_order_return.html")


@is_staff
@login_required
def order_return_list_view(request: HttpRequest) -> HttpResponse:
    """Implementation of the order return list view"""

    context = {"object_list": OrderReturn.objects.filter(status=False)}
    return render(request, "order_return_list.html", context)


@is_staff
@login_required
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
@is_staff
@login_required
def confirm_order_return_view(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Implementation of the order return request confirmation view.
    After the request confirmation:
    1. Returns money to the customer.
    2. The quantity of products returns to the previous values.
    3. The order status becomes 'Cancelled'.
    Removes the return order instance if the request is rejected.
    """

    try:
        order_return = OrderReturn.objects.get(id=pk)
    except OrderReturn.DoesNotExist:
        raise Http404("The order return request not found")
    customer = order_return.customer
    order = order_return.order
    redirect_url = reverse_lazy("return_order_list")

    if request.method == "POST":

        form = ConfirmForm(request.POST)
        if form.is_valid():
            decision = form.cleaned_data["decision"]

            if decision == "CONFIRM":
                total_cost = order.cart.calculate_sum()
                customer.add_money(total_cost)

                order_items = order.cart.items.all()
                for item in order_items:
                    product = item.product
                    quantity = item.quantity
                    product.increase_quantity(quantity)

                order.cancel()
                order_return.confirm()

            else:
                order_return.delete()

            return HttpResponseRedirect(redirect_url)

    else:
        form = ConfirmForm()

    return render(request, "confirm_order_return.html", {"form": form})
