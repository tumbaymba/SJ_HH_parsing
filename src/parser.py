from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests


class Parser(ABC):
    """
    Абстрактный базовый класс для парсера.
    """

    #__slots__ = ('keyword', 'url', 'headers', 'per_page', 'parameters')

    @abstractmethod
    def parse_vacancies(self, keyword: str, count: int) -> List[Dict[str, Any]]:
        """
        Анализирует вакансии на основе заданного ключевого слова и количества.

        """
        pass


class ParserMixin:
    """
    Выполняет HTTP-запрос GET и возвращает ответ в виде JSON.
    """

    @staticmethod
    def make_request(url: str, parameters: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:

        return requests.get(url, params=parameters, headers=headers).json()


