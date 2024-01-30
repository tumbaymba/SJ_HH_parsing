from src.parser import Parser, ParserMixin


class HHParser(Parser, ParserMixin):

    def __init__(self):
        super().__init__()
        self.per_page: int = 10
        self.url: str = 'https://api.hh.ru/vacancies'
        self.headers: dict = {'HHParser-User-Agent': 'Vacant/1.0 (pavlushindv@gmail.com)'}
        self.parameters: dict = {'page': 1, 'per_page': self.per_page, 'text': '', 'search_field': 'name'}

    def parse_vacancies(self, keyword: str, count: int) -> list[dict]:
        """
        Анализирует вакансии с сайта HH.ru на основе заданного ключевого
        слова и количества.

        """
        self.parameters.update({'text': keyword if keyword else ''})
        result = []
        pages = count // self.per_page + 1 \
            if count % self.per_page else count // self.per_page

        for page in range(0, pages):
            self.parameters.update({'page': page})

            response = self.make_request(
                self.url, self.parameters, self.headers
            )
            result.extend(response['items'])
        return result
