import re

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from lists.views import home_page, view_list, new_list
from lists.models import Item, List


# Create your tests here.

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expect_html = render_to_string('home.html')
        observed_html = self.getContentDecode(response)
        self.assertEqual(observed_html, expect_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '신규 작업 아이템'

        response = new_list(request)

        # self.assertEqual(Item.objects.count(), 1)
        # new_item = Item.objects.first()
        # self.assertEqual('신규 작업 아이템', new_item.text)
        # self.assertIn('신규 작업 아이템', response.content.decode())
        _list = List.objects.first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/%d/'%(_list.id))
        # observed_html = self.getContentDecode(response)
        # expected_html = render_to_string('home.html', {'new_item_text':'신규 작업 아이템'})
        # self.assertEqual(observed_html, expected_html)

    def test_home_page_displays_all_list_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list = list_)
        Item.objects.create(text='itemey 2', list = list_)

        request = HttpRequest()
        response = view_list(request, list_.id)

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

    def getContentDecode(self, response):
        return ToolsForTest().getContentDecode(response)


class ToolsForTest():
    def getContentDecode(self, response):
        # CSRF tokens don't get render_to_string'd
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        observed_html = re.sub(csrf_regex, '', response.content.decode())
        return observed_html

class ListViewTest(TestCase):
    def test_home_page_displays_all_list_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list = list_)
        Item.objects.create(text='itemey 2', list = list_)

        request = HttpRequest()
        # response = home_page(request)

        response = self.client.get('/lists/%d/'%(list_.id))

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

        # self.assertContains('itemey 1', response)
        # self.assertContains('itemey 2', response)

    def test_uses_list_template(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)
        response = self.client.get('/lists/%d/'%(list_.id))
        self.assertTemplateUsed(response, 'list.html')

    def test_display_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list = correct_list)
        Item.objects.create(text='itemey 2', list = correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='다른 아이템 1', list = other_list)
        Item.objects.create(text='다른 아이템 2', list = other_list)

        response = self.client.get('/lists/%d/'%(correct_list.id))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, '다른 아이템 1')
        self.assertNotContains(response, '다른 아이템 2')

    def test_saving_a_POST_request(self):
        self.client.post('/lists/new'
                         , data={'item_text': '신규 작업 아이템'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '신규 작업 아이템')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new'
                                    , data={'item_text': '신규 작업 아이템'})
        new_list = List.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/%d/'%(new_list.id))

