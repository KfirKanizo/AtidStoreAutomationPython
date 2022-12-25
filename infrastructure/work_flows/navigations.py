from seleniumbase import BaseCase
from infrastructure.page_objects import home_page


class navigations(BaseCase):
    def navigate_to_store_page(self):
        self.click(home_page.store_btn)