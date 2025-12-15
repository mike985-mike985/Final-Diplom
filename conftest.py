import pytest
from pages.main_page import MainPage
from pages.film_page import FilmPage
from selenium import webdriver
from config import MAIN_URL


@pytest.fixture
def driver():
    """Фикстура для создания драйвера"""
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture
def main_page(driver):
    """Фикстура для создания главной страницы"""
    return MainPage(driver, MAIN_URL)


@pytest.fixture
def film_page(driver):
    """Фикстура для создания страницы фильма"""
    return FilmPage(driver)
