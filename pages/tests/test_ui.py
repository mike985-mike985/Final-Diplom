import pytest
import allure
from config import TITLE, VALID_UI_FILMS, FILM_PAGE, \
    FILM_PAGE_TITLE, FILM_PAGE_IDS, INVALID_MOVIE_ID


@allure.feature("Smoke")
@allure.story("UI")
@allure.title("Проверка заголовка главной страницы")
@pytest.mark.smoke
def test_check_main_page_title(main_page):
    """Smoke тест проверки заголовка главной страницы"""
    with allure.step("Заголовок главной страницы"):
        assert main_page.check_page_title(TITLE)


@allure.feature("Поиск")
@allure.story("UI")
@allure.title("Поиск фильмов по названию")
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.parametrize("film_title",
                         VALID_UI_FILMS)
def test_search_film_by_title(main_page, film_title):
    """Тест поиска фильма по названию на главной странице"""
    with allure.step(f"Поиск фильмов по названию"
                     f" {film_title}"):
        main_page.search_items_by_phrase(film_title)

    with allure.step("Проверяет, что количество результатов больше 0"):
        assert main_page.get_search_results_count() > 0, \
            'Не удалось получить список фильмов'

    with allure.step("Получение списка найденных фильмов"):
        assert film_title in main_page.find_films_titles(), \
            "Фильм не найден в результатах поиска"

    with allure.step("Проверяет, что количество найденных фльмов больше 0"):
        film_titles = main_page.find_films_titles()
        assert len(film_titles) > 0, "Не удалось получить список фильмов"


@allure.feature("Поиск")
@allure.story("UI")
@allure.title("Пустой поиск")
@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.parametrize("film_title",
                         ["блабалабалалалал"])
def test_empty_search(main_page, film_title):
    """Тест поиска фильма по названию на главной странице"""
    with allure.step(f"Поиск фильмов по названию"
                     f" {film_title}"):
        main_page.search_items_by_phrase(film_title)

    with allure.step("Проверяет, что количество найденных фльмов 0"):
        assert main_page.get_search_results_count() == 0, \
            "Удалось получить список фильмов"


@allure.feature("Поиск")
@allure.story("UI")
@allure.title("Поиск и переход на фильм")
def test_click_first_film(main_page):
    with allure.step("Поиск фильма"):
        main_page.search_items_by_phrase(FILM_PAGE)

    with allure.step("Клик на первый результат"):
        main_page.click_on_first_film()

    with allure.step("Заголовок главной страницы"):
        assert main_page.check_page_title(FILM_PAGE_TITLE)


@allure.feature("Страница фильма")
@allure.story("UI")
@allure.title("Клик на обложку фильма с указанием ID")
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.parametrize("film_id", FILM_PAGE_IDS)
def test_click_on_film_poster_with_id(film_page, film_id):
    """Тест клика на обложку фильма с указанием ID"""
    with allure.step(f"Переход на страницу фильма с ID {film_id}"):
        film_page.go_to_film_page_by_id(film_id)

    with allure.step("Проверка, что мы на правильной странице"):
        assert film_page.is_on_film_page(film_id), \
            f"Не удалось перейти на страницу фильма с ID {film_id}"

    with allure.step("Клик на обложку фильма"):
        film_page.click_on_film_poster_by_xpath(film_id)

    with allure.step("Проверка, что произошел переход "
                     "на страницу с постерами"):
        assert film_page.is_on_film_page(film_id), \
            "Не произошел переход на страницу с постерами"


@allure.feature("Страница фильма")
@allure.story("UI")
@allure.title("Переход на несуществующий фильм")
@pytest.mark.ui
@pytest.mark.negative
def test_nonexistent_film_page(film_page):
    """Тест перехода на страницу несуществующего фильма"""
    with allure.step("Переход на страницу несуществующего фильма"):
        film_page.go_to_film_page_by_id(INVALID_MOVIE_ID)

    with allure.step("Проверка, что отображается 404 ошибка"):
        assert film_page.has_404_error(), "Сообщение о 404 ошибке не найдено"
