
from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # 그녀는 입력 사자가 가운데 배치된 것을 본다
        inputbox = self.find_input_box()
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            delta=10
        )

        self.sendInputText('testing')
        # 그녀는 입력 사자가 가운데 배치된 것을 본다
        inputbox = self.find_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
