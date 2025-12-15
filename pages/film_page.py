import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FilmPage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)

    @allure.step("Переход на страницу фильма по ID: {film_id}")
    def go_to_film_page_by_id(self, film_id):
        film_url = f"https://www.kinopoisk.ru/film/{film_id}/"
        self.driver.get(film_url)
        WebDriverWait(self.driver, 20).until(
            EC.url_contains(f"/film/{film_id}")
        )
        return self

    @allure.step("Клик на обложку фильма через XPath с ID")
    def click_on_film_poster_by_xpath(self, film_id):
        poster_locator = f'//a[contains(@href, "/film/{film_id}/posters/")]'
        poster = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, poster_locator))
        )
        poster.click()
        WebDriverWait(self.driver, 20).until(
            EC.url_contains("/posters")
        )
        return self

    @allure.step("Проверка, что мы на странице фильма с ID: {film_id}")
    def is_on_film_page(self, film_id):
        current_url = self.driver.current_url
        expected_pattern = f"/film/{film_id}"
        return expected_pattern in current_url

    @allure.step("Проверка наличия 404 ошибки")
    def has_404_error(self):
        """
        Проверяет, есть ли на странице сообщение '404. Страница не найдена'
        """
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH, "//*[contains(text(), '404')]"))
        )
        return "404. Страница не найдена" in self.driver.page_source
