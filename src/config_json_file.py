import json
from src.vacancy import Vacancy
from typing import List, Dict, Any
from src.api import FILE_PATH
from src.abstract_methods import FileHandler
from src.filter_salary import SalaryRangeFilter
from json import JSONDecodeError

class JSONFileHandler(FileHandler):
    """
    Класс, который обрабатывает файлы JSON, содержащие вакансии.
    """

    __file_path: str = FILE_PATH
    __data = []

    @classmethod
    def _read_file(cls, file_path: str) -> None:
        """
        Считывает файл JSON и загружает данные.

        """
        try:
            with open(file_path, 'r') as f:
                cls.__data = json.load(f)
        except FileNotFoundError:
            print(f'File {file_path} не найден, создан новый файл')
            cls._save_file(cls.__data, cls.__file_path)
        except JSONDecodeError:
            print(f'File {file_path} не является JSON файлом')

    @classmethod
    def _save_file(
            cls, data: List[Dict[str, Any]], file_path: str = FILE_PATH) -> None:
        """
        Сохраняет данные в JSON-файл.

        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавляет вакансию к данным JSON.

        """
        self._read_file(self.__file_path)
        self.__data.append(vacancy.to_dict())
        self._save_file(self.__data, self.__file_path)

    def _get_vacancy(self, vacancy_id: int) -> Dict[str, Any]:
        """
        Извлекает вакансию из данных JSON на основе ID вакансии.
        Возвращает данные о вакансии.
        """
        self._read_file(self.__file_path)
        return self.__data[vacancy_id]

    def _delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удаляет вакансию из данных JSON.
        """
        self._read_file(self.__file_path)
        try:
            self.__data.remove(vacancy.to_dict())
        except ValueError:
            print(f' Вакансия "{vacancy.title}" не найдена')
        self._save_file(self.__data, self.__file_path)

    def _load_vacancies(self, platforms, count, word_to_search, salary_min_max):
        """
        Загружает вакансии из данных JSON на основе заданных параметров.
        """
        self._read_file(self.__file_path)

        result = {}
        for platform, vacancies in self.__data.items():
            if platform not in platforms.values():
                continue

            vacancies_obj_list = [
                Vacancy(
                    platform=vacancy['platform'],
                    vacancy_id=vacancy['vacancy_id'],
                    title=vacancy['title'],
                    url=vacancy['url'],
                    salary_from=vacancy['salary_from'],
                    salary_to=vacancy['salary_to'],
                    currency=vacancy['currency'],
                    description=vacancy['description']
                ) for vacancy in vacancies
            ]
            salary_filter = SalaryRangeFilter()
            vacancies_filtered = salary_filter.filter_vacancies(
                vacancies_obj_list, salary_min_max
            )
            result[platform] = vacancies_filtered
        return result

    def load_vacancies(self, platforms, count, word_to_search, salary_min_max):

        return self._load_vacancies(platforms, count, word_to_search, salary_min_max)

    def save_all_vacancies(self, vacancies) -> None:
        """
        Сохраняет все вакансии в JSON-файл.

        """
        self._save_file(vacancies)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавляет вакансию к данным JSON.

        """
        self._add_vacancy(vacancy)

    def get_vacancy(self, vacancy_id: int) -> Dict[str, Any]:
        """
        Извлекает вакансию из данных JSON на основе ID.

        """
        return self._get_vacancy(vacancy_id)

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удаляет вакансию из данных JSON.

        """
        self._delete_vacancy(vacancy)
