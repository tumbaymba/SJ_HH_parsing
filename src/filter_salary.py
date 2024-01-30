
from typing import List
from src.vacancy import Vacancy


class SalaryRangeFilter:

    def filter_vacancies(self, vacancies: List[Vacancy], salary_range: List[int]) -> List[Vacancy]:
        """
        Фильтрует вакансии на основе диапазона зарплат.

        """
        min_salary, max_salary = salary_range
        filtered_vacancies = []

        for vacancy in vacancies:
            if vacancy.avg_salary == 0:
                continue
            if min_salary is not None and vacancy.avg_salary <= min_salary:
                continue
            if max_salary is not None and vacancy.avg_salary >= max_salary:
                continue
            filtered_vacancies.append(vacancy)
        return filtered_vacancies
