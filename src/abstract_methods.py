from abc import ABC, abstractmethod


class FileHandler(ABC):

    @abstractmethod
    def _add_vacancy(self, vacancy):
        """
        Добавляет вакансию в файл
        """
        pass

    @abstractmethod
    def _get_vacancy(self, vacancy_id):
        """
        Извлекает вакансию из файла на основе ее идентификатора и возвращает её
        """
        pass

    @abstractmethod
    def _load_vacancies(self, platforms, count, word_to_search, salary_min_max):
        """
        Загружает вакансии из файла по заданным критериям
        и возвращает список вакансий, соответствующих этим критериям.
        """
        pass

    @abstractmethod
    def _delete_vacancy(self, vacancy_id):
        """
        Удаляет вакансию из файла на основе ее ID.
        """
        pass
