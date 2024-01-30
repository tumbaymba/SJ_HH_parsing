import requests
import os
import json

class Employer:

    def employee_of_date(self):
        values = {'text': 'газ', 'area': 1, 'only_with_vacancies': True}

        req = requests.get('https://api.hh.ru/employers', values)
        data = req.json()

        employees_file = 'employers.json'
        with open(employees_file, 'w') as f:
            json.dump(data, f, ensure_ascii=False)
        return data