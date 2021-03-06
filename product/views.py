from django.shortcuts import render,HttpResponse,redirect,reverse,get_object_or_404
from .forms import ProductForm, SearchForm
from .models import Product, Category
from reviews.forms import ReviewForm
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

# Create your views here.
def index(request):
    product = Product.objects.all()
    return render(request,'product/index.template.html',{
        'product': product,
    })

def all_product(request):
    product = Product.objects.all()
    if request.GET:

        queries = ~Q(pk__in=[])

        # if a name is typed, add it to the query
        if 'name' in request.GET and request.GET['name']:
            name = request.GET['name']
            queries = queries & Q(name__icontains=name)

        # if a category is choose, add it to the query
        if 'category' in request.GET and request.GET['category']:
            print("adding category")
            category = request.GET['category']
            queries = queries & Q(category__in=category)

        # update the existing book found
        product = product.filter(queries)

    category = Category.objects.all()
    search_form = SearchForm(request.GET)
    return render(request,'product/all_product.template.html',{
        'product': product,
        'catergory': category,
        'search_form': search_form
    })

@staff_member_required
def create_product(request):
    if request.method == 'POST':
        create_form = ProductForm(request.POST)

        if create_form.is_valid():
            create_form.save()
            return redirect(reverse(all_product))
        else:
            return render(request, 'product/create_product.template.html',{
                'form': create_form
            })

    else:
        create_form = ProductForm()
        return render(request, 'product/create_product.template.html',{
            'form': create_form
        })

@staff_member_required
def update_product(request,product_id):
    update_product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        form_for_product =ProductForm(request.POST,instance=update_product)
        if form_for_product.is_valid():
            form_for_product.save()
            return redirect(reverse(all_product))
        else:
            return render(request, 'product/update_product.template.html', {
                "form": form_for_product
                })
    else:
        form_for_product = ProductForm(instance=update_product)
        return render(request, 'product/update_product.template.html', {
            "form": form_for_product
        })

@staff_member_required
def delete_product(request,product_id):
    product_to_delete = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        product_to_delete.delete()
        return redirect(all_product)

    else:
        return render(request, 'product/product_delete.template.html',{
            "product": product_to_delete
        })

#view product in details
def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    review_form = ReviewForm()
    return render(request, 'product/one_product.template.html', {
        'product': product,
        'form': review_form
    })


