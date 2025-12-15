import allure
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    def __init__(self, driver, url):
        self.driver = driver
        self.driver.maximize_window()
        self.driver.get(url)
        self.close_communication_if_exists()

    @allure.step("Проверка наличия и закрытие всплывающего окна,"
                 " если оно появляется")
    def close_communication_if_exists(self, timeout=25):
        """
        Ожидает появления либо кнопки закрытия коммуникации,
        либо поля поиска (признак, что окна нет)
        """
        # Ждем появления любого из двух элементов
        element = WebDriverWait(self.driver, timeout).until(
            EC.any_of(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[aria-label="Закрыть коммуникацию"]')),
                # Поле поиска (индикатор нормальной страницы)
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[name="kp_query"]'))
            )
        )
        # Проверяем, что именно нашли
        if element.get_attribute("aria-label") == "Закрыть коммуникацию":
            element.click()

    @allure.step("Ожидание появления элементов на странице со значением value")
    def _wait_for_elements(self, by, value, multiple=False, timeout=20):
        if multiple:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located((by, value)))
        else:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value)))

    @allure.step("Получение текста со всех элементов "
                 "страницы соотв. css_selector")
    def _get_element_texts(self, by, css_selector):
        elements = self._wait_for_elements(by, css_selector, multiple=True)
        return [element.text for element in elements]

    @allure.step("Поиск контента по фразе: {phrase}")
    def search_items_by_phrase(self, phrase):
        with allure.step("Поиск поля ввода названия фильма и ввод названия"):
            self._wait_for_elements(
                By.CSS_SELECTOR, "input[name=kp_query]").send_keys(phrase)
        with allure.step("Нахождение и выбор кнопки Все результаты"):
            self._wait_for_elements(By.CSS_SELECTOR, "#all").click()

        with allure.step("Нахождение и нажатие кнопки Поиск"):
            self.driver.find_element(
                By.CSS_SELECTOR, "button[aria-label='Найти']").click()

    @allure.step("Получаем количество результатов поиска")
    def get_search_results_count(self):
        with allure.step("Ожидает появления элемента с классом "
                         ".search_results_topText и извлекает из него текст"):
            results_text = self._wait_for_elements(
                By.CSS_SELECTOR, ".search_results_topText").text
        with allure.step("Поиск числа в results_text с помощью "
                         "регулярного выражения"):
            match = re.search(r'результаты:\s*(\d+)', results_text)
        with allure.step("Обработка результата поиска"):
            if match:
                return int(match.group(1))
            else:
                return 0

    @allure.step("Получаем названия фильмов")
    def find_films_titles(self):
        return self._get_element_texts(By.XPATH, "//p[@class='name']/a")

    @allure.step("Проверка заголовка страницы")
    def check_page_title(self, expected_title):
        WebDriverWait(self.driver, timeout=20).until(
            lambda driver: driver.title != "")
        return self.driver.title == expected_title

    @allure.step("Клик на первый найденный фильм")
    def click_on_first_film(self):
        """Кликает на первый фильм в результатах поиска"""
        film_links = WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((
                By.XPATH, "//p[@class='name']/a"))
        )
        if film_links:
            film_links[0].click()
        return self
