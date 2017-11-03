from django.shortcuts import render, redirect
from lists.models import Item

# Create your views here.


def home_page(request):

    if request.method == 'POST':
        text = request.POST.get('item_text', '')
        textItem = Item()
        textItem.text = text
        textItem.save()
        return redirect('/')


    return render(request, 'home.html', {'items' : Item.objects.all()})