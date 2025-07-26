from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
 template_name = 'pages/about.html'

 def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update({
        "title": "About us - Online Store",
        "subtitle": "About us",
        "description": "This is an about page for an online store. Here you can find information about our mission, vision, and values.",
        "author": "Developed by: Alexandra Hurtado",
    })
    return context


class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact Us - Online Store",
            "email": "ahurtadod@eafit.edu.co",
            "address": "EAFIT, Medellín, Colombia",
            "phone": "3024000000",
        })
        return context
    
class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best SmartTV for you", "price": 450},
        {"id": "2", "name": "iPhone", "description": "The last release of iPhone", "price": 500},
        {"id": "3", "name": "Chromecast", "description": "The most complete", "price": 100},
        {"id": "4", "name": "Glasses", "description": "Luxurious and modern Glasses", "price": 10},
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)
    
class ProductShowView(View):
    template_name = 'products/show.html'
    def get(self, request, id):
        try:
            product = Product.products[int(id) - 1]
        except (IndexError, ValueError):
            # Si el ID no es válido, redireccionar a la página de inicio
            return HttpResponseRedirect(reverse('home'))
        viewData = {}
        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)

from django import forms
from django.core.exceptions import ValidationError

class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('Price must be greater than zero.')
        return price

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {
            "title": "Create product",
            "form": form
        }
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            # Aquí podrías guardar el producto si tuvieras un modelo
            return render(request, 'products/product_created.html')  # Mostrar nueva plantilla
        else:
            viewData = {
                "title": "Create product",
                "form": form
            }
            return render(request, self.template_name, viewData)
