"""
My_shop application views
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Product, Category


class ProductListView(ListView):
    """Homepage view implementation"""

    model = Product
    template_name = "homepage.html"

    def get_queryset(self):
        if self.request.method == "GET":
            category_slug = self.request.GET.get('category')
            if category_slug:
                return Product.objects.filter(category=Category.objects.get(slug=category_slug))
            else:
                return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        categories_list = []
        products = Product.objects.all()
        for product in products:
            if product.category not in categories_list:
                categories_list.append(product.category)
        context["categories_list"] = categories_list
        return context


class ProductDetailView(DetailView):
    """Product view implementation"""

    http_method_names = "get"
    model = Product
    template_name = "product.html"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Product create view implementation"""

    http_method_names = "get", "post"
    model = Product
    fields = "__all__"
    template_name = "product_form.html"

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Product update view implementation"""

    http_method_names = "get", "post"
    model = Product
    fields = "__all__"
    template_name = "product_form.html"


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Product delete view implementation"""

    http_method_names = "get", "post"
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("homepage")


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """Category create view implementation"""

    http_method_names = "get", "post"
    model = Category
    fields = "__all__"
    template_name = "category_form.html"
    success_url = reverse_lazy("homepage")
