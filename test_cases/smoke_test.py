from seleniumbase import BaseCase
from infrastructure.configurations import config
from infrastructure.page_objects import home_page, store_page, product_page
from infrastructure.work_flows.navigations import navigations as nv
from infrastructure.work_flows.store_flows import store_flows as stf


class smoke_test(BaseCase):
    def setUp(self):
        super().setUp()
        print("\n************** STARTING TEST **************\n")
        self.maximize_window()
        self.open(config.base_url)

    def tearDown(self):
        print("\n************** CLOSING TEST **************\n")
        self.save_screenshot("end_test", "/infrastructure/img_repo")
        super().tearDown()


    def test_search_for_product(self):
        nv.navigate_to_store_page(self)
        #search for product
        self.send_keys(store_page.search_input, "ATID Black Shoes")
        self.click(store_page.search_btn)
        #assert product name found
        product_name = self.get_text(product_page.product_name)
        self.assertEqual(product_name, "ATID Black Shoes")


    def test_filter_by_price(self):
        nv.navigate_to_store_page(self)
        #assert filter values before change filter
        self.assert_equal(stf.get_filter_min_price(self), "30 ₪")
        self.assert_equal(stf.get_filter_max_price(self), "250 ₪")
        #move change filter
        self.press_up_arrow(store_page.price_filter_min, times=7)
        self.focus(store_page.slider)
        self.press_down_arrow(store_page.price_filter_max, times=5)
        #assert filter values after change filter
        self.assert_equal(stf.get_filter_min_price(self), "100 ₪")
        self.assert_equal(stf.get_filter_max_price(self), "200 ₪")
        #press on submit filter button
        self.click(store_page.price_filter_btn)
        #assert filter has be saved
        self.assert_equal(stf.get_filter_min_price(self), "100 ₪")
        self.assert_equal(stf.get_filter_max_price(self), "200 ₪")


    def test_count_store_equals_to_count_by_category(self):
        nv.navigate_to_store_page(self)
        total_items_count = stf.get_total_items_count(self)
        accesories_items_count = stf.get_items_count_by_category(self, "Accessories")
        men_items_count = stf.get_items_count_by_category(self, 2)
        woman_items_count = stf.get_items_count_by_category(self, "Women")
        total_categories_count = accesories_items_count + men_items_count + woman_items_count
        #SHOULD BE FAILED ACCORDING TO BUG IN THE WEBSITE
        self.assert_equal(int(total_items_count), total_categories_count)


    def test_product_with_highest_price(self):
        nv.navigate_to_store_page(self)
        highest_price_value = stf.get_item_with_highest_price(self)
        self.assert_equal(250, highest_price_value)