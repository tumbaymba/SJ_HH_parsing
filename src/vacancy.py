class Vacancy:
    """
    Класс, представляющий вакансию на работу.
    """
    __slots__ = ['_platform', '_vacancy_id', '_title', '_url', '_salary_from', '_salary_to', '_currency',
                 '_description', '_avg_salary']

    def __init__(self, platform: str, vacancy_id: int, title: str, url: str, salary_from: int, salary_to: int,
                 currency: str, description: str):
        self._platform: str = platform
        self._vacancy_id: int = int(vacancy_id)
        self._title: str = title
        self._url: str = url
        self._salary_from: int = salary_from
        self._salary_to: int = salary_to
        self._currency: str = currency
        self._description: str = (description[:200] if len(description) > 200 else description) \
            if description is not None else "Отсутствует описание"
        self._avg_salary: int = 0

        if isinstance(salary_from, int):
            if isinstance(salary_to, int):
                self._avg_salary = max(salary_from, salary_to)
            else:
                self._avg_salary = salary_from
        elif isinstance(salary_to, int):
            self._avg_salary = salary_to

    @property
    def title(self) -> str:
        """
        Получает название вакансии.

        """
        return self._title

    @property
    def platform(self) -> str:

        return self._platform

    @property
    def vacancy_id(self) -> int:
        """
        Получает идентификатор вакансии.

        """
        return self._vacancy_id

    @property
    def url(self) -> str:
        """
        Получает URL вакансии
        """
        return self._url

    @property
    def salary_from(self) -> int:
        """
        Получает стартовую зарплату по вакансии.

        """
        return self._salary_from

    @property
    def salary_to(self) -> int:
        """
        Получает максимальную зарплату по вакансии.

        """
        return self._salary_to

    @property
    def description(self) -> str:
        """
        Получает описание вакансии.

        """
        return self._description

    @property
    def avg_salary(self) -> int:
        """
        Получает среднюю зарплату по вакансии.
        """
        return self._avg_salary

    def to_dict(self) -> dict:
        """
        Вакансия преобразуется в словарь.

        """
        return {'platform': self._platform, 'vacancy_id': self._vacancy_id, 'title': self._title,
            'url': self._url, 'salary_from': self._salary_from, 'salary_to': self._salary_to,
            'currency': self._currency, 'description': self._description, 'avg_salary': self._avg_salary}

    def __str__(self):
        """
        Возвращает строковое значение вакансии.

        """
        return (f'Platform: {self._platform}\n' f'ID: {self._vacancy_id}\n' f'Title: {self._title}\n'
            f'Salary: {self._salary_from} {self._currency} - ' f'{self._salary_to} {self._currency} \n'
            f'Description: {self._description}\n' f'Link: {self._url}\n')


    def __eq__(self, other):
        """
        Сравнивает две вакансии по размеру средней з/п.

        """
        if isinstance(other, self.__class__):
            return self._avg_salary == other._avg_salary
        return NotImplemented

    def __ne__(self, other):
        """
        Сравните две вакансии на предмет неравенства, на основе средней з/п.

        """
        if isinstance(other, self.__class__):
            return self._avg_salary != other._avg_salary
        return NotImplemented
