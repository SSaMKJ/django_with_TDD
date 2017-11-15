from django.shortcuts import render, redirect
from lists.models import Item, List


# Create your views here.


def home_page(request):

    return render(request, 'home.html')


def view_list(request, list_id):
    # 정규식으로 넘어오는 path variable 이 자동으로 list_id에 매핑되는구나... 좋네.
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'items': items, 'list':list_})


def new_list(request):
    item_text = request.POST.get('item_text', '')
    list_ = List.objects.create()
    Item.objects.create(text=item_text, list=list_)
    return redirect('/lists/%d/'%(list_.id))


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST.get('item_text', ''), list=list_)
    return redirect('/lists/%d/' % (list_.id))