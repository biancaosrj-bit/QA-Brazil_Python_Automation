
import pytest
from selenium import webdriver

import data
import helpers
from pages import UrbanRoutesPage


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.set_capability(
            "goog:loggingPrefs",
            {"performance": "ALL"}
        )

        cls.driver = webdriver.Chrome(options=options)

        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            cls.driver.get(data.URBAN_ROUTES_URL)
            cls.page = UrbanRoutesPage(cls.driver)
        else:
            raise Exception("URL do Urban Routes indisponível")

    def prepare_order(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutesPage(self.driver)
        self.page.set_route(
            data.ADDRESS_FROM,
            data.ADDRESS_TO
        )
        self.page.select_comfort_plan()

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutesPage(self.driver)

        self.page.set_route(
            data.ADDRESS_FROM,
            data.ADDRESS_TO
        )

        assert self.page.get_from_address() == data.ADDRESS_FROM
        assert self.page.get_to_address() == data.ADDRESS_TO

    def test_select_plan(self):
        self.prepare_order()
        assert self.page.is_comfort_plan_selected()

    def test_fill_phone_number(self):
        self.prepare_order()

        self.page.enter_phone_number(data.PHONE_NUMBER)

        assert self.page.is_phone_verified()

    def test_fill_card(self):
        self.prepare_order()
        self.page.enter_phone_number(data.PHONE_NUMBER)
        self.page.enter_payment_method(
            data.CARD_NUMBER,
            data.CARD_CODE
        )
        assert self.page.is_card_linked()

    def test_comment_for_driver(self):
        self.prepare_order()

        self.page.set_message_for_driver(
            data.MESSAGE_FOR_DRIVER
        )

        assert (
            self.page.get_message_for_driver()
            == data.MESSAGE_FOR_DRIVER
        )

    def test_order_blanket_and_handkerchiefs(self):
        self.prepare_order()

        self.page.click_blanket_and_handkerchiefs_slider()

        assert self.page.is_blanket_and_handkerchiefs_selected()

    def test_order_2_ice_creams(self):
        self.prepare_order()

        self.page.order_ice_cream(2)

        assert self.page.get_ice_cream_count() == 2

    def test_car_search_model_appears(self):
        self.prepare_order()

        self.page.enter_phone_number(data.PHONE_NUMBER)

        self.page.set_message_for_driver(
            data.MESSAGE_FOR_DRIVER
        )

        self.page.click_order_button()

        assert self.page.is_car_search_modal_visible()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
