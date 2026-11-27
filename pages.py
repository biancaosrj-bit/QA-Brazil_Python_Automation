
import helpers
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class UrbanRoutesPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # ENDEREÇOS

    def set_route(self, from_address, to_address):
        from_input = self.wait.until(
            EC.element_to_be_clickable((By.ID, "from"))
        )
        from_input.clear()
        from_input.send_keys(from_address, Keys.DOWN, Keys.ENTER)

        time.sleep(1)

        to_input = self.wait.until(
            EC.element_to_be_clickable((By.ID, "to"))
        )
        to_input.clear()
        to_input.send_keys(to_address, Keys.DOWN, Keys.ENTER)

        time.sleep(1)

        button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Chamar um táxi')]")
            )
        )
        button.click()

    def get_from_address(self):
        return self.driver.find_element(
            By.ID, "from"
        ).get_attribute("value")

    def get_to_address(self):
        return self.driver.find_element(
            By.ID, "to"
        ).get_attribute("value")

    # PLANO COMFORT

    def select_comfort_plan(self):
        active = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".tcard.active")
            )
        )

        if "Comfort" not in active.text:
            comfort = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class,'tcard')]//*[normalize-space()='Comfort']")
                )
            )
            comfort.click()

    def is_comfort_plan_selected(self):
        active = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".tcard.active")
            )
        )
        return "Comfort" in active.text

    # TELEFONE

    def enter_phone_number(self, phone_number):
        try:
            button = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, "np-button")
                )
            )
            button.click()
        except TimeoutException:
            pass

        phone = self.wait.until(
            EC.element_to_be_clickable((By.ID, "phone"))
        )
        phone.clear()
        phone.send_keys(phone_number)

        next_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Próximo']")
            )
        )
        next_button.click()

        code = helpers.retrieve_phone_code(self.driver)

        code_input = self.wait.until(
            EC.element_to_be_clickable((By.ID, "code"))
        )
        code_input.send_keys(code)
        code_input.send_keys(Keys.TAB)

        print("CÓDIGO RECUPERADO:", code)
        print("CAMPO SMS:", code_input.get_attribute("value"))

        confirm = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Confirm') or contains(., 'Confirmar')]")
            )
        )
        confirm.click()
        time.sleep(2)

        print("SMS AINDA VISÍVEL:", self.driver.find_element(By.ID, "code").is_displayed())
        print("TEXTO DA JANELA:", self.driver.find_element(
            By.XPATH, "//*[contains(., 'Confirmar')]"
        ).text)

        self.wait.until(
            EC.invisibility_of_element_located((By.ID, "code"))
        )

    def is_phone_verified(self):
        phone = self.wait.until(
            EC.presence_of_element_located((By.ID, "phone"))
        )
        return phone.get_attribute("value") != ""

    # CARTÃO

    def enter_payment_method(self, card_number, card_code):
        payment_button = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "pp-button"))
        )
        payment_button.click()

        add_card = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[normalize-space()='Adicionar cartão']")
            )
        )
        add_card.click()

        number_input = self.wait.until(
            EC.element_to_be_clickable((By.ID, "number"))
        )
        number_input.send_keys(card_number)

        code_input = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input.card-input#code")
            )
        )
        code_input.send_keys(card_code)
        code_input.send_keys(Keys.TAB)

        add_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Adicionar']")
            )
        )

        print("NÚMERO:", number_input.get_attribute("value"))
        print("CVV:", code_input.get_attribute("value"))
        print("BOTÃO ADICIONAR:", add_button.is_enabled())

        add_button.click()
        time.sleep(2)

        print(
            "PAGAMENTO APÓS ADICIONAR:",
            self.driver.find_element(By.TAG_NAME, "body").text[:1000]
        )

    def is_card_linked(self):
        payment_button = self.wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "pp-button")
            )
        )
        return "Cartão" in payment_button.text

    # COMENTÁRIO PARA O MOTORISTA

    def set_message_for_driver(self, message):
        comment = self.wait.until(
            EC.element_to_be_clickable((By.ID, "comment"))
        )
        comment.clear()
        comment.send_keys(message)

    def get_message_for_driver(self):
        return self.driver.find_element(
            By.ID, "comment"
        ).get_attribute("value")

    # MANTA E LENÇOS

    def click_blanket_and_handkerchiefs_slider(self):
        slider = self.wait.until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "slider")
            )
        )
        slider.click()

    def is_blanket_and_handkerchiefs_selected(self):
        checkbox = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='checkbox']")
            )
        )
        return checkbox.get_property("checked")

    # SORVETES

    # SORVETES

    def order_ice_cream(self, count):
        chocolate = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='r-counter-label' and text()='Chocolate']")
            )
        )

        container = chocolate.find_element(
            By.XPATH, "./ancestor::div[@class='r-counter-container']"
        )

        plus_button = container.find_element(
            By.CLASS_NAME, "counter-plus"
        )

        for _ in range(count):
            self.wait.until(
                lambda driver: "disabled" not in plus_button.get_attribute("class")
            )
            plus_button.click()

    def get_ice_cream_count(self):
        chocolate = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='r-counter-label' and text()='Chocolate']")
            )
        )

        container = chocolate.find_element(
            By.XPATH, "./ancestor::div[@class='r-counter-container']"
        )

        count = container.find_element(
            By.CLASS_NAME, "counter-value"
        )

        return int(count.text)

    # PEDIDO FINAL

    # PEDIDO FINAL

    # PEDIDO FINAL

    def click_order_button(self):
        order_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "smart-button")
            )
        )
        order_button.click()

    def is_car_search_modal_visible(self):
        try:
            modal = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//*[contains(text(), 'Buscar carro')]"
                    )
                )
            )
            return modal.is_displayed()

        except TimeoutException:
            return False