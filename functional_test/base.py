import sys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from selenium.webdriver.common.keys import Keys


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://'+arg.split('=')[1]
                return
            super().setUpClass()
            cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.initBrowser()

    def initBrowser(self):
        self.browser = webdriver.Chrome('drivers/chromedriver')
        self.browser.implicitly_wait(1)  # seconds

    def tearDown(self):
        self.browser.quit()
        # pass


    def check_for_row_in_list_table(self, saved_item):
        rows = self.getTableRows()
        self.assertIn(saved_item, [row.text for row in rows], '신규 작업이 테이블에 표시되지 않는다.')

    def getTableRows(self):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        return rows

    def sendInputText(self, inputText):
        inputbox = self.find_input_box()
        inputbox.send_keys(inputText)
        inputbox.send_keys(Keys.ENTER)

    def find_input_box(self):
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), '작업 아이템 입력')
        return inputbox



# if __name__ == '__main__':
#     unittest.main(warnings='ignore')

