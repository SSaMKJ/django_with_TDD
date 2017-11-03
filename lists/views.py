from django.shortcuts import render, redirect
from lists.models import Item, List


# Create your views here.


def home_page(request):

    return render(request, 'home.html')


def view_list(request, list_id):
    print('list_id = '+list_id)
    print('list_id = '+list_id)
    print('list_id = '+list_id)
    print('list_id = '+list_id)
    print('list_id = '+list_id)
    print('list_id = '+list_id)
    print('list_id = '+list_id)
    print('list_id = '+list_id)
    print('list_id = '+list_id)
    list_ = List.objects.get(list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'items': items})


def new_list(request):
    text = request.POST.get('item_text', '')
    textItem = Item()
    textItem.text = text
    list_ = List.objects.create()
    textItem.list = list_
    textItem.save()
    return redirect('/lists/%d/'%list_.id)