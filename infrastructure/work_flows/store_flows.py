from seleniumbase import BaseCase
from infrastructure.page_objects import store_page


class store_flows(BaseCase):
    def get_filter_min_price(self):
        filter_bar = self.get_text("//span[@class='from']")
        return filter_bar

    def get_filter_max_price(self):
        filter_bar = self.get_text("//span[@class='to']")
        return filter_bar

    def get_total_items_count(self):
        full_row = self.get_text("//p[@class='woocommerce-result-count']")
        values = full_row.split()
        return values[3]

    def get_items_count_by_category(self, category):
        list_of_categories = self.find_elements("//ul[@class='product-categories']//span[@class='count']")
        relevant_count = ''
        if category == "Accessories" or category == 1:
            relevant_count = list_of_categories[0].text
        elif category == "Men" or category == 2:
            relevant_count = list_of_categories[1].text
        elif category == "Women" or category == 3:
            relevant_count = list_of_categories[2].text
        relevant_count_number =  ''.join(filter(lambda i: i.isdigit(), relevant_count))
        relevant_count_number = int(relevant_count_number)
        return relevant_count_number

    def get_item_with_highest_price_in_page(self):
        current_highest_price = 0
        products_price = self.find_elements(store_page.all_products_price)
        for price in products_price:
            current_price = price.text
            current_price = current_price.split('.')
            current_price = current_price[0]
            current_price = int(current_price)
            if current_price > current_highest_price:
                current_highest_price = current_price
        return current_highest_price


    def get_item_with_highest_price(self):
        current_highest_price = 0
        pages = self.find_elements(store_page.pages_amount)
        pages_amount = len(pages) + 1
        for i in range(pages_amount):
            try:
                if self.is_element_clickable(store_page.next_page_btn):
                    page_highest_price = store_flows.get_item_with_highest_price_in_page(self)
                    if page_highest_price > current_highest_price:
                        current_highest_price = page_highest_price
                    self.click(store_page.next_page_btn)
                else:
                    page_highest_price = store_flows.get_item_with_highest_price_in_page(self)
                    if page_highest_price > current_highest_price:
                        current_highest_price = page_highest_price
                    return current_highest_price
            except Exception(e):
                print(e)