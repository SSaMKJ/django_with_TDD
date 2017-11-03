from django.shortcuts import render
from lists.models import Item

# Create your views here.


def home_page(request):
    text = request.POST.get('item_text', '')
    print(len(text), text)
    if len(text) > 0 :
        textItem = Item()
        textItem.text = text
        textItem.save()

    return render(request, 'home.html',{
        'new_item_text':text
    })