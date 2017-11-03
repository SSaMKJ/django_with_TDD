import re

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from lists.views import home_page
from lists.models import Item

# Create your tests here.

class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = '첫 번째 아이템'
        first_item.save()

        second_item = Item()
        second_item.text = '두 번째 아이템'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, '첫 번째 아이템')
        self.assertEqual(second_saved_item.text, '두 번째 아이템')


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

        response = home_page(request)

        # self.assertEqual(Item.objects.count(), 1)
        # new_item = Item.objects.first()
        # self.assertEqual('신규 작업 아이템', new_item.text)
        # self.assertIn('신규 작업 아이템', response.content.decode())


        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
        # observed_html = self.getContentDecode(response)
        # expected_html = render_to_string('home.html', {'new_item_text':'신규 작업 아이템'})
        # self.assertEqual(observed_html, expected_html)

    def test_home_page_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        request = HttpRequest()
        response = home_page(request)

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

    def getContentDecode(self, response):
        # CSRF tokens don't get render_to_string'd
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        observed_html = re.sub(csrf_regex, '', response.content.decode())
        return observed_html

class ListViewTest(TestCase):


    def test_home_page_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        request = HttpRequest()
        # response = home_page(request)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

        # self.assertContains('itemey 1', response)
        # self.assertContains('itemey 2', response)

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')