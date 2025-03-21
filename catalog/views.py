from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.views.generic import View
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


from catalog.forms import CatalogForm, CatalogAdminForm
from catalog.models import Product


def home(request):
    return render(request, "home.html")


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        message = request.POST.get("message")
        return HttpResponse("Данные отправлены.")
    return render(request, "contacts.html")


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = CatalogForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:products_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.product += 1
        self.object.save()
        return self.object

class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = CatalogForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user.has_perm('catalog.can_unpublish_product'):
            return CatalogForm
        if user.has_perm('catalog.can_delete_product'):
            return CatalogAdminForm
        raise PermissionDenied

    def get_success_url(self):
        return reverse("catalog:product_detail", args=[self.kwargs.get("pk")])

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:products_list")

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)

class UnpublishProductView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        if not request.user.has_perm('catalog.can_unpublish_product'):
            return PermissionDenied

        product.unpublish = product.is_active
        product.is_active = False
        product.save()
        return redirect('catalog:product_detail', product_id=product.id)
