from django.test import LiveServerTestCase
from selenium import webdriver

from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.initBrowser()

    def initBrowser(self):
        self.browser = webdriver.Chrome('drivers/chromedriver')
        self.browser.implicitly_wait(1)  # seconds

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 에디스(Edith)는 멋진 작업 목록 온라인 앱이 나왔다는 소식을 듣고 해당 웹 사이트를 확인하러 같다.
        # self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)

        # 웹 페이지 타이틀과 헤더가 'To-Do'를 표시하고 있다.
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)


        # 그녀는 바로 작업을 추가하기로 한다.

        # "공작기털 사기"라고 텍스트 상자에 입력한다.
        # (에디스의 취미는 날치 잡이용 그물을 만드는 것이다.)
        # 엔터키를 치면 페이지가 갱신되고 작업 목록에
        # "1: 공작깃털 사기" 아이템이 추가된다.
        self.sendInputText('공작깃털 사기')

        edit_list_url = self.browser.current_url
        self.assertRegex(edit_list_url, '/lists/.+')

        self.check_for_row_in_list_table('1: 공작깃털 사기')

        # 추가 아이템을 입력할 수 있는 여분의 텍스트 상자가 존재한다.
        # 다시 "공작깃털을 이용해서 그물 만들기"라고 입력한다.(에디스는 매우 체계적인 사람이다.)
        self.sendInputText('공작깃털을 이용해서 그물 만들기')
        # 페이지는 다시 갱신되고, 두 개 아이템이 목록에 보인다.
        self.check_for_row_in_list_table('2: 공작깃털을 이용해서 그물 만들기')


        # 새로운 사용자인 프란시스가 사이트에 접속한다.

        self.browser.quit()
        self.initBrowser()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        print(page_text)
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertNotIn('그물 만들기', page_text)

        self.sendInputText('우유 사기')
        self.check_for_row_in_list_table('1: 우유 사기')

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edit_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertIn('우유 사기', page_text)
        # 에디스는 사이트가 입력한 목록을 저장하고 있는지 궁금하다.
        #  사이트는 그녀를 위한 특정 URL을 생성해준다.
        # 이때 URL에 대한 설명도 함께 제공된다.

        # 해당 URL에 접속하면 그녀가 만든 작업 목록이 그대로 있는 것을 확인할 수 있다.

        # 만족하고 잠자리에 든다.


    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # 그녀는 입력 사자가 가운데 배치된 것을 본다
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            delta=10
        )

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

