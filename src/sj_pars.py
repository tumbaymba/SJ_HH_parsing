# from src.constants import SUPER_JOB_API_SECRET
from src.parser import Parser, ParserMixin


class SuperJobParser(Parser, ParserMixin):
    """
    Parser implementation for the SuperJob website.
    """

    def __init__(self):
        super().__init__()
        self.per_page: int = 20
        self.url: str = "https://api.superjob.ru/2.0/vacancies/"
        self.headers: dict = {
            'X-Api-App-Id': 'v3.r.136850847.e39865903958048a12b45a35681fa6697b3ce8dd.538c47ffb34a07f5d50b1c565986aa9720d117a4'}
        self.parameters: dict = {'page': 1, 'count': self.per_page, 'keywords[0][srws]': 1, 'keywords[0][skwc]': 'or',
                                 'keywords[0][keys]': ''}

    def parse_vacancies(self, keyword: str, count: int) -> list[dict]:
        """
        Анализирует вакансии с сайта SuperJob на основе заданного ключевого
        слова и количества.

        """

        self.parameters.update({'keywords[0][keys]': keyword if keyword else ''})
        result = []
        pages = count // self.per_page + 1 \
            if count % self.per_page else count // self.per_page

        for page in range(0, pages):
            self.parameters.update({'page': page})

            response = self.make_request(self.url, self.parameters, self.headers)
            result.extend(response['objects'])
        return result
