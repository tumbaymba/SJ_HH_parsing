import os
from typing import List, Dict
from src.api import FILE_PATH
from src.config_json_file import JSONFileHandler
from src.hh_pars import HHParser
from src.sj_pars import SuperJobParser
from src.vacancy import Vacancy
from src.filter_salary import SalaryRangeFilter


def hh_processor(count: int, word_ro_search: str, salary_filter: SalaryRangeFilter,
                 salary_min_max: List[int]) -> List[Vacancy]:
    """
    Получаем список вакансий по API и возвращаем список согластно требованиям соискателя
    """
    hh_parser = HHParser()
    hh_vacancies = hh_parser.parse_vacancies(word_ro_search, count)

    hh_vacancy_obj_list = [
        Vacancy(
            platform='HH.ru',
            vacancy_id=vacancy['id'],
            title=vacancy['name'],
            url=vacancy['alternate_url'],
            salary_from=(vacancy['salary']['from'] if vacancy['salary'] else None),
            salary_to=(vacancy['salary']['to'] if vacancy['salary'] else None),
            currency=(vacancy['salary']['currency'] if vacancy['salary'] else None),
            description=vacancy['snippet']['requirement'] if vacancy['snippet']['requirement']
            else vacancy['snippet']['responsibility'])
        for vacancy in hh_vacancies]

    if salary_min_max.count(None) == 2:
        return hh_vacancy_obj_list
    else:
        return salary_filter.filter_vacancies(hh_vacancy_obj_list, salary_min_max)


def sj_process(count: int, word_ro_search: str, salary_filter: SalaryRangeFilter, salary_min_max: List[int | None]
               ) -> List[Vacancy]:
    """
    Обработка вакансии с ресурса SuperJob.
    Возвращает список отфильтрованных вакансий.
    """
    sj_parser = SuperJobParser()
    sj_vacancies = sj_parser.parse_vacancies(word_ro_search, count)

    sj_vacancy_obj_list = [
        Vacancy(
            platform='SuperJob.ru',
            vacancy_id=vacancy['id'],
            title=vacancy['profession'],
            url=vacancy['link'],
            salary_from=vacancy['payment_from'],
            salary_to=vacancy['payment_to'],
            currency=vacancy['currency'],
            description=vacancy['vacancyRichText'])
        for vacancy in sj_vacancies]

    if salary_min_max.count(None) == 2:
        return sj_vacancy_obj_list
    else:
        return salary_filter.filter_vacancies(sj_vacancy_obj_list, salary_min_max)


def print_vacancies(platforms_vacancies: Dict[str, List[Vacancy]]):
    """
    Выводит список вакансий для каждой платформы.
    """

    for platform, vacancies in platforms_vacancies.items():

        print('\n', '-' * 10, platform, '-' * 10)
        print('-' * 10, len(vacancies), '-' * 10)
        if not vacancies:
            print("Нет вакансий, соответствующих указанным критериям.", end='\n\n')
            continue

        for vacancy in vacancies:
            print(vacancy)


def main(selected_platforms: Dict[str, str], count: int, word_ro_search: str, salary_min_max: List[int]
         ) -> Dict[str, List[Vacancy]]:
    """
    Главная функция для выполнения задачи.
    """
    salary_filter = SalaryRangeFilter()

    hh_vacancies_filtered = []
    sj_vacancies_filtered = []

    if '1' in selected_platforms:
        hh_vacancies_filtered = hh_processor(
            count, word_ro_search, salary_filter,
            salary_min_max)

    if '2' in selected_platforms:
        sj_vacancies_filtered = sj_process(count, word_ro_search, salary_filter, salary_min_max)

    return {'HH.ru': hh_vacancies_filtered, 'SuperJob.ru': sj_vacancies_filtered}


def user_interface():
    """
    Пользовательский интерфейс для работы с программой.
    """
    print('Программа для поиска вакансий')

    json_file_handler = JSONFileHandler()
    file_to_read = 'n'
    if os.path.exists(FILE_PATH):
        file_to_read = input('Прочесть сохраненный ранее файл (y/n): ')

    selected_platforms = {}
    while True:
        platform_selector = ''
        while platform_selector != '3':
            platform_selector = input(
                'Выберете ресурс для поиска вакансий: \n'
                '1. HH.ru \n'
                '2. SuperJob.ru \n'
                '3. Нажмите после выбора \n')

            if platform_selector in selected_platforms.keys():
                print('Этот ресурс уже выбран.')
                continue

            if platform_selector == '1':
                selected_platforms['1'] = 'HH.ru'
            elif platform_selector == '2':
                selected_platforms['2'] = 'SuperJob.ru'

        if not selected_platforms:
            print('Не одна платформа не выбрана.')
            to_exit = input('Желаете выйти из программы? (y/n): ')
            if to_exit == 'y':
                exit()
        else:
            break

    word_to_search = input('Введите ключевое слово для поиска: ')

    min_salary, max_salary = None, None

    is_filtered = input('Желаете указать диапазон зарплат? (y/n): ')

    if is_filtered == 'y':
        try:
            min_salary = int(
                input('Введите минимальный уровень зарплаты (для следующего шага нажмите Enter): '))
        except ValueError:
            min_salary = None

        try:
            max_salary = int(input('Введите максимальный уровень зарплаты (для следующего шага нажмите Enter): '))
        except ValueError:
            max_salary = None

    try:
        count = int(input(
            'Какое количество вакансий желаете увидеть ? '
            '(количество должно быть кратно 10)? '
            '(по умолчанию: 50): '))
    except ValueError:
        count = 50

    salary_min_max = [min_salary, max_salary]

    if file_to_read.lower() != 'y':
        all_vacancies = main(selected_platforms, count, word_to_search, salary_min_max)
    else:
        all_vacancies = (json_file_handler.load_vacancies(selected_platforms, count, word_to_search, salary_min_max))

    print_vacancies(all_vacancies)

    if file_to_read.lower() != 'y':
        save_vacancies = input('Желаете сохранить в файл формата json? (y/n): ')

        if save_vacancies == 'y':
            vacancies_to_save = {}
            for platform, vacancies in all_vacancies.items():
                vacancies_to_dict = [
                    vacancy.to_dict() for vacancy in vacancies
                ]
                vacancies_to_save[platform] = vacancies_to_dict
            json_file_handler.save_all_vacancies(vacancies_to_save)


if __name__ == '__main__':
    user_interface()
