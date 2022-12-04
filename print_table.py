import csv, re
import datetime

from prettytable import PrettyTable


class DataSet:
    """
    Класс для подготовки данных для дальнейшего использования.
    Attributes:
        file_name (str): Название файла
    """
    def __init__(self, file_name):
        """Инициализирует объект DataSet

        Args:
            file_name (str): Название файла
        """
        self.file_name = file_name
        self.vacancies_objects = DataSet.parse_row(file_name)

    @staticmethod
    def сsv_reader(file_name):
        """
        Обрабатывает csv файл, пропуская незаполенные строки

        Args:
            file_name (str): Название файла

        Returns:
            list, list: Список названий заголовков, Список вакансий
        """
        file_csv = open(file_name, encoding="utf_8_sig")
        reader_csv = csv.reader(file_csv)
        list_data = [x for x in reader_csv]
        DataSet.check_file(list_data)
        columns = list_data[0]
        result = [x for x in list_data[1:] if len(x) == len(columns) and x.count('') == 0]
        return columns, result

    @staticmethod
    def check_file(list_data):
        """
        Проверяет файл на пустоту или отсутствие данных и если это подтведилось - выходит из программы

        Args:
            list_data (list): Все строки в файле
        """
        if len(list_data) == 0:
            print("Пустой файл")
            exit()
        if len(list_data) == 1:
            print("Нет данных")
            exit()

    @staticmethod
    def parse_row(file_name):
        """
        Парсит каждый пункт професси от лишних пробелов, html тегов и преобразует строку навыков в список
        Args:
            file_name (str): Название файла

        Returns:
            list: Возвращает список объектов Vacancy
        >>> len(DataSet.parse_row("test_vacancies.csv")[0].key_skills)
        2
        """
        name, rows = DataSet.сsv_reader(file_name)
        result = []
        for row in rows:
            new_row = dict(zip(name, row))
            for x in new_row:
                if x == "name":
                    new_row[x] = " ".join(new_row[x].split())
                if x == "description":
                    new_row[x] = " ".join((re.sub(r'\<[^>]*\>', '', new_row[x])).split())
                elif x == "key_skills":
                    new_row[x] = new_row[x].split("\n")
                DataSet.translate_row(new_row, x)

            result.append(Vacancy(new_row))
        return result

    @staticmethod
    def translate_row(new_row, word):
        """
        Переводит пункты salary_gross, premium, experience_id на русский язык
        Args:
            new_row (dict): Словарь профессии
            word (str): Пункт в профессии
        """
        if word == "salary_gross" or word == "premium":
            new_row[word] = new_row[word].replace("False", "Нет")
            new_row[word] = new_row[word].replace("True", "Да")
        if word == "experience_id":
            new_row[word] = ru_exp[new_row[word]]


class InputConnect:
    """
    Класс для получения, обработки и печати данных необходимых пользователю
    Attributes:
        file_name (str): Название файла
        filter_dict (list[str]): Параметр фильтрации
        sort_parameter (str): Параметр сортировки
        is_reverse_sort (str): Обратный порядок сортировки
        from_to (str | list[str]): Диапазон вывода
        show_title (str | list[str]): Требуемые столбцы
    """
    def __init__(self):
        """
        Инициализирует класс InputConnect
        """
        self.file_name, self.filter_dict, \
        self.sort_parameter, self.is_reverse_sort, \
        self.from_to, self.show_title = InputConnect.get_params()

    @staticmethod
    def get_params():
        """
        Получает на вход данные введенные пользователем, обрабатывает и возвращает их
        Returns:
            str, str, str, str, list[str], list[str] : Название файла, Параметр фильтрации, Параметр сортировки,
            Обратный порядок сортировки, Диапазон вывода, Требуемые столбцы
        """
        file_name = input("Введите название файла: ")
        filter_dict = input("Введите параметр фильтрации: ")
        sort_parameter = input("Введите параметр сортировки: ")
        is_reverse_sort = input("Обратный порядок сортировки (Да / Нет): ")
        from_to = input("Введите диапазон вывода: ").split()
        show_title = input("Введите требуемые столбцы: ").split(", ")
        filter_dict, is_reverse_sort = InputConnect.check_user_input(filter_dict, is_reverse_sort, sort_parameter)
        return file_name, filter_dict, sort_parameter, is_reverse_sort, from_to, show_title

    @staticmethod
    def check_user_input(filter_dict, is_reverse_sort, sort_parameter):
        """
        Проверяет коррекнтость данных, введенных пользователем. Если некорректно - выводит ошибку
        и завершает работу программы
        Args:
            filter_dict (str | list[str]): Параметр фильтрации
            is_reverse_sort (str): Обратный порядок сортировки
            sort_parameter (str): Параметр сортировки

        Returns:
            str, bool: Параметр фильтрации, Обратный порядок сортировки
        """
        if (filter_dict != "") and (not ":" in filter_dict):
            print("Формат ввода некорректен")
            exit()
        elif filter_dict != "" and not filter_dict.split(": ")[0] in exa:
            print("Параметр поиска некорректен")
            exit()
        else:
            filter_dict = filter_dict.split(": ")
        if sort_parameter not in exa:
            print("Параметр сортировки некорректен")
            exit()
        if is_reverse_sort not in reverse_parameter:
            print("Порядок сортировки задан некорректно")
            exit()
        else:
            is_reverse_sort = reverse_parameter[is_reverse_sort]
        return filter_dict, is_reverse_sort

    def print_vacancy(self, data):
        """
        Подготавливает и печатает таблицу профессий в консоль
        Args:
            data (list[Vacancy]): Список объектов Vacancy
        """
        self.tab = PrettyTable()
        self.tab._max_width = {x: 20 for x in (["№"] + list(ru_words.values()))}
        self.tab.field_names = ["№"] + list(ru_words.values())
        self.tab.align = "l"
        self.tab.hrules = True
        data = InputConnect.filter_table(self, data)
        for x in range(len(data)):
            InputConnect.formatter(data[x])
            new_data = list(data[x])
            new_data.insert(0, x + 1)
            self.tab.add_row(new_data)
        InputConnect.print_from_to(self)

    def print_from_to(self):
        """
        Печатает таблицу в определённом диапазоне и с определенными пунктами профессии,
        если параметров нет - печается все

        """
        if len(self.show_title) != 1:
            self.show_title = ["№"] + self.show_title
        else:
            if self.show_title[0] == "":
                self.show_title = self.tab.field_names
        if len(self.from_to) == 2:
            print(self.tab.get_string(start=int(self.from_to[0]) - 1, end=int(self.from_to[1]) - 1,
                                      fields=list(self.show_title)))
            exit()
        if len(self.from_to) == 1 and self.from_to[0] != 0:
            print(self.tab.get_string(start=int(self.from_to[0]) - 1, fields=self.show_title))
            exit()
        print(self.tab.get_string(fields=self.show_title))

    def filter_table(self, data):
        """
        Фильтрует список объектов Vacancy, по данным, введенным пользователем.
        Если Ничего не было найдено, то выводит это в консоль и завершает работу программы
        Args:
            data (list[Vacancy]): Список объектов Vacancy

        Returns:
            list: Отсортированный и фильтрованный список объектов Vacancy
        """
        if len(self.filter_dict) != 1:
            new_data = list(filter(lambda x: filter_types[self.filter_dict[0]](x, self.filter_dict[1]), data))
        else:
            new_data = data
        if len(new_data) == 0:
            print("Ничего не найдено")
            exit()
        return InputConnect.sort_table(self, new_data)

    def sort_table(self, data):
        """
        Сортирует список объектов Vacancy, по данным, введенным пользователем.
        Если пользователь ничего не вводил в параметр сортировки, то сортировка не будет применена
        Args:
            data(list[Vacancy]): Фильтрованный список объектов Vacancy

        Returns:
            list: Отсортированный и фильтрованный список объектов Vacancy
        """
        if self.sort_parameter != "":
            new_data = sorter_types[self.sort_parameter](data, self.is_reverse_sort)
        else:
            new_data = data
        return new_data

    @staticmethod
    def check_skills(row, words):
        """
        Проверяет наличие навыков, которые ввел пользователь
        Args:
            row (Vacancy): объект Vacancy
            words (str | list[str]): навык(и), введенные пользователем

        Returns:
            bool: Наличие всех запрашиваемых навыков в профессии
        """
        current_count = 0
        words = words.split(", ")
        check_count = len(words)
        row = row.key_skills
        for x in words:
            if x in row:
                current_count += 1
        return current_count == check_count

    @staticmethod
    def formatter(vac):
        """
        Форматирует данные в полях объекта Vacancy для печати в таблице
        Args:
            vac (Vacancy): Объект Vacancy
        """
        vac.salary = "{0:,} - {1:,} ({2}) ({3})".format(int(float(vac.salary.salary_from)),
                                                        int(float(vac.salary.salary_to)),
                                                        ru_currency[vac.salary.salary_currency],
                                                        salary_gross_dic[vac.salary.salary_gross]).replace(",",
                                                                                                           " ")
        vac.published_at = datetime.datetime.strptime(vac.published_at, "%Y-%m-%dT%H:%M:%S%z").strftime("%d.%m.%Y")
        vac.key_skills = "\n".join(vac.key_skills)
        try:
            vac.key_skills = vac.key_skills[0:100] + " ..." if vac.key_skills[101] == " " and vac.key_skills[100] == " " \
                else vac.key_skills[0:100] + "..."
        except:
            pass
        vac.description = vac.description[0:100] + " ..." if vac.description[101] == " " and vac.description[100] == " " \
            else vac.description[0:100] + "..."


class Vacancy:
    """
    Класс для предоставления вакансии
    Attributes:
        name (str): Назваеие профессии
        description (str): Описание профессии
        key_skills (list): Навыки, указанные в профессии
        experience_id (str): Опыт работы
        premium (str): Премиум-вакансия
        employer_name (str): Название компании
        salary (object(Salary)): Класс Salary
        area_name (str): Расположение
        published_at (str): Дата публикации
    """
    def __init__(self, row):
        """
        Инициализирует объект Vacancy
        Args:
            row (dict): Словарь в котором содержиться строка вакансии, разделённая на различные пункты
        """
        self.name = row["name"]
        self.description = row["description"]
        self.key_skills = row["key_skills"]
        self.experience_id = row["experience_id"]
        self.premium = row["premium"]
        self.employer_name = row["employer_name"]
        self.salary = Salary(row["salary_from"], row["salary_to"], row["salary_gross"], row["salary_currency"])
        self.area_name = row["area_name"]
        self.published_at = row["published_at"]

    def __iter__(self):
        """
        Получение итератора для перебора объекта
        """
        for each in self.__dict__.values():
            yield each


class Salary:
    """
    Класс для предоставления зарплаты
    Attributes:
        salary_from (int): Нижняя граница вилки оклада
        salary_to (int): Верхняя граница вилки оклада
        salary_currency (str): Валюта оклада
        salary_gross (str): Признак того что оклад указан до вычета налогов
    """
    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        """
        Инициализирует объект Salary
        Args:
            salary_from (int): Нижняя граница вилки оклада
            salary_to (int): Верхняя граница вилки оклада
            salary_gross (str): Признак того что оклад указан до вычета налогов
            salary_currency (str): Валюта оклада
        """
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency


ru_words = {"name": "Название",
            "description": "Описание",
            "key_skills": "Навыки",
            "experience_id": "Опыт работы",
            "premium": "Премиум-вакансия",
            "employer_name": "Компания",
            "salary": "Оклад",
            "area_name": "Название региона",
            "published_at": "Дата публикации вакансии"}
exa = ['Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия', 'Компания', 'Оклад', 'Название региона',
       'Дата публикации вакансии', '', "Идентификатор валюты оклада"]
ru_exp = {"noExperience": "Нет опыта",
          "between1And3": "От 1 года до 3 лет",
          "between3And6": "От 3 до 6 лет",
          "moreThan6": "Более 6 лет"}
ru_currency = {"AZN": "Манаты",
               "BYR": "Белорусские рубли",
               "EUR": "Евро",
               "GEL": "Грузинский лари",
               "KGS": "Киргизский сом",
               "KZT": "Тенге",
               "RUR": "Рубли",
               "UAH": "Гривны",
               "USD": "Доллары",
               "UZS": "Узбекский сум"}
salary_gross_dic = {"Нет": "С вычетом налогов",
                    "Да": "Без вычета налогов"}
currency_to_rub = {"AZN": 35.68,
                   "BYR": 23.91,
                   "EUR": 59.90,
                   "GEL": 21.74,
                   "KGS": 0.76,
                   "KZT": 0.13,
                   "RUR": 1,
                   "UAH": 1.64,
                   "USD": 60.66,
                   "UZS": 0.0055}
reverse_parameter = {"Нет": False,
                     "Да": True,
                     "": False}
filter_types = {"Название": lambda row, words: row.name == words,
                "Описание": lambda row, words: row.description == words,
                "Навыки": lambda row, words: InputConnect.check_skills(row, words),
                "Опыт работы": lambda row, words: words == row.experience_id,
                "Премиум-вакансия": lambda row, words: words in row.premium,
                "Компания": lambda row, words: row.employer_name == words,
                "Идентификатор валюты оклада": lambda row, words: ru_currency[row.salary.salary_currency] == words,
                "Оклад": lambda row, words: int(float(row.salary.salary_from)) <= int(words) <= int(
                    float(row.salary.salary_to)),
                "Название региона": lambda row, words: words in row.area_name,
                "Дата публикации вакансии": lambda row, words: datetime.datetime
                                                                   .strptime(row.published_at, "%Y-%m-%dT%H:%M:%S%z")
                                                                   .strftime("%d.%m.%Y") == words,
                "": lambda row, words: row}
sorter_types = {"Название": lambda row, revers: sorted(row, key=lambda d: d.name, reverse=revers),
                "Описание": lambda row, revers: sorted(row, key=lambda d: d.description, reverse=revers),
                "Навыки": lambda row, revers: sorted(row, key=lambda d: len(d.key_skills),
                                                     reverse=revers),
                "Опыт работы": lambda row, revers: sorted(row, key=lambda d: sort_exp[d.experience_id],
                                                          reverse=revers),
                "Премиум-вакансия": lambda row, revers: sorted(row, key=lambda d: d.premium, reverse=revers),
                "Компания": lambda row, revers: sorted(row, key=lambda d: d.employer_name, reverse=revers),
                "Идентификатор валюты оклада": lambda row, revers: sorted(row,
                                                                          key=lambda d: ru_currency[d.salary_currency],
                                                                          reverse=revers),
                "Оклад": lambda row, revers: sorted(row, key=lambda d:
                (int(float(d.salary.salary_from)) + int(float(d.salary.salary_to))) / 2 * currency_to_rub[
                    d.salary.salary_currency],
                                                    reverse=revers),
                "Название региона": lambda row, revers: sorted(row, key=lambda d: d.area_name, reverse=revers),
                "Дата публикации вакансии": lambda row, revers: sorted(row, key=lambda d: datetime.datetime.
                                                                       strptime(d.published_at, "%Y-%m-%dT%H:%M:%S%z")
                                                                       .strftime("%Y.%m.%d.%H.%M.%S"), reverse=revers),
                "": lambda row, words: row}
sort_exp = {"Нет опыта": 0,
            "От 1 года до 3 лет": 1,
            "От 3 до 6 лет": 2,
            "Более 6 лет": 3}

