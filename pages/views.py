from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.views import View
from django.contrib import messages
from .models import Product

# Create your views here. 
class HomePageView(TemplateView):
    template_name = "pages/home.html"

class AboutPageView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Andres Suarez Rios",
        })
        return context 

'''    
class Product:
    products = [
    {"id":"1", "name":"TV", "description":"Best TV", "price": 500},
    {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 999},
    {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 50},
    {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 20}
]'''
    
class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.objects.all()

        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        # ✅ Fetch product directly from the database
        product = get_object_or_404(Product, pk=id)  

        viewData = {
            "title": f"{product.name} - Online Store",
            "subtitle": f"{product.name} - Product Information",
            "product": product
        }
        return render(request, self.template_name, viewData)

    
class ContactPageView(TemplateView):
    template_name = "pages/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact Us - Online Store",
            "subtitle": "Contact Information",
        })
        return context

class ProductForm(forms.ModelForm):
    #name = forms.CharField(required=True)
    #price = forms.IntegerField(required=True)

    class Meta:
        model = Product
        fields = ['name', 'price']

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.") 
        return price

class ProductCreateView(View):
    template_name = 'products/create.html'
    
    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        
        return render(request, self.template_name, viewData)
    
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            '''new_product = {
                "id": str(len(Product.products) + 1), 
                "name": form.cleaned_data["name"],
                "description": "New Product",
                "price": form.cleaned_data["price"]
            }
            Product.products.append(new_product)'''
            messages.success(request, "Product created!")

            return redirect('success')
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)
        
class ProductSuccessView(TemplateView):
    template_name = "products/success.html"

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products' # This will allow you to loop through 'products' in your template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of products'
        return context 