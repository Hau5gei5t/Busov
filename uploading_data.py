import pathlib
import time
import sqlite3

import pandas as pd
from concurrent.futures import ProcessPoolExecutor
import requests
import xmltodict
import math
import json
from pandas import json_normalize

pd.set_option("expand_frame_repr", False)


def upload_chunks(file_name):
    """
    Принимает на вход общую выгрузку, а возвращает столько csv файлов сколько разных годов содержалось в выгрузке
    """
    pd.set_option("expand_frame_repr", False)
    df = pd.read_csv(file_name)
    df["years"] = df["published_at"].apply(lambda s: int(s[:4]))
    years = df["years"].unique()
    for year in years:
        data = df[df["years"] == year]
        data.iloc[:, :6].to_csv(rf"csv_files\year_{year}.csv", index=False)


def prepare_data(file_name, prof, area_name):
    """
    Обрабатывает данные в чанке для дальнейшей работы
    Args:
        file_name: Имя csv файла, в котором все профессии за 1 год
        prof: Профессия для составления статистики

    Returns:
        list[int]: Возвращает список, в котором год,
        зарплата по вакансиям за 1 год,
        кол-во по необходимой вакансии за 1 год,
        зарплата по необходимой вакансии за 1 год,
        кол-во вакансий за 1 год

    """
    pd.set_option("expand_frame_repr", False)
    df = pd.read_csv(file_name)
    df.dropna()
    a = df["published_at"].apply(lambda s: int(s[:4])).unique()
    salary_by_year = int(df[["salary_from", "salary_to"]].mean(axis=1).mean())
    vac_counts_by_year = df[(df["name"].str.contains(prof)) & (df["area_name"] == area_name)]
    vac_salary_by_year = int(vac_counts_by_year[["salary_from", "salary_to"]].mean(axis=1).mean())
    return [a[0], salary_by_year, len(vac_counts_by_year), vac_salary_by_year, len(df)]


def main(folder, prof, area_name):
    """
    Обрабатывает чанки и выгружает обработанные данные
    Args:
        folder: Название папки с чанками
        prof: Профессия для составления статистики

    Returns:
        dict, dict, dict, dict: возвращает словари: Динамика уровня зарплат по годам,
        Динамика количества вакансий по годам,
        Динамика уровня зарплат по годам для выбранной профессии,
        Динамика количества вакансий по годам для выбранной профессии
    """
    if __name__ == "uploading_data":
        csv_path = pathlib.Path(folder)
        file_list = [f_name for f_name in csv_path.glob("*.csv")]
        salary_by_years = {}
        vac_counts_by_years = {}
        vac_salary_by_years = {}
        vacs_by_years = {}
        with ProcessPoolExecutor(max_workers=2) as executor:
            for x in range(len(file_list)):
                i = executor.submit(prepare_data, file_list[x], prof, area_name).result()
                salary_by_years[i[0]] = i[1]
                vac_counts_by_years[i[0]] = i[2]
                vac_salary_by_years[i[0]] = i[3]
                vacs_by_years[i[0]] = i[4]
        return salary_by_years, vacs_by_years, vac_salary_by_years, vac_counts_by_years


def get_years_currency(file_name):
    """
    Получает на вход файл, выбирает валюты, которые встречаются больше 5000 раз, находит самую раннюю и позднюю вакансию
    в этом диапазоне с интервалом в 1 месяц получает курсы валют с сайта ЦБ РФ, сохраняет полученный результат в формате
    .csv
    Args:
        file_name: название файла
    """
    result = pd.DataFrame()
    pd.set_option("expand_frame_repr", False)
    df = pd.read_csv(file_name)
    freq = df['salary_currency'].value_counts().to_dict()
    freq = {key: value for key, value in freq.items() if value >= 5000}
    print(freq)
    df = df[df["salary_currency"].isin(list(freq.keys()))]
    date_range = [df["published_at"].min().split("-")[:2], df["published_at"].max().split("-")[:2]]
    print(date_range)
    row = {}
    for year in range(int(date_range[0][0]), int(date_range[1][0]) + 1):
        for month in range(int(date_range[0][1]), 13):
            print(year, month)
            try:
                response = requests.get(
                    rf"http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/{str(month).zfill(2)}/{year}")
            except Exception:
                continue
            response = xmltodict.parse(response.text)
            for i in response['ValCurs']['Valute']:
                if i['CharCode'] in list(freq.keys()):
                    row["Date"] = f"{year}-{str(month).zfill(2)}"
                    row[i['CharCode']] = round(float(i["Value"].replace(",", ".")) / int(i["Nominal"]), 7)
            result = pd.concat([result, pd.DataFrame([row])])
            if year == int(date_range[1][0]) and month == int(date_range[1][1]):
                break
            if month == 12:
                break
    cnx = sqlite3.connect("currency.db")
    result.to_sql("currency", con=cnx, index=False)


def currency_conversion(file_name):
    """
    Обрабатывает данные из колонок ‘salary_from’, ‘salary_to’, ‘salary_currency’, и объединяет в одну колонку salary
    Args:
        file_name: имя файла
    """
    df = pd.read_csv(file_name)
    df["salary"] = df.apply(lambda row: get_mean(row), axis=1)
    df["salary"] = df.apply(lambda row: exchange_salary(row), axis=1)
    df.drop(labels=["salary_from", "salary_to", "salary_currency"], axis=1, inplace=True)
    df = df[["name", "salary", "area_name", "published_at"]]
    cnx = sqlite3.connect("new_vacs.db")
    df.to_sql("vacs", con=cnx, index=False)


def get_mean(row):
    """
    Возращает число в зависимости от заполненности полей ‘salary_from’, ‘salary_to’
    Args:
        row: Строка в df

    Returns:
        среднее между числами или ничего, если поля были пустыми
    """
    args = []
    if not math.isnan(row["salary_from"]):
        args.append(row["salary_from"])
    if not math.isnan(row["salary_to"]):
        args.append(row["salary_to"])
    if len(args) != 0:
        return sum(args) / len(args)
    return


def exchange_salary(row):
    """
    Сверяет дату появления вакансии с датой в файле содержащем курсы валют по датам,
    находит необходимую валюту и умнажает на коэффициент
    Args:
        row: Строка в df

    Returns:
        значение в рублях
    """
    res = []
    exchange = sqlite3.connect("currency.db")
    cur = exchange.cursor()
    # exchange = pd.read_csv("currency.csv")
    cur.execute("SELECT name FROM PRAGMA_TABLE_INFO('currency');")
    for i in cur.fetchall():
        res.append(i[0])
    if row["salary_currency"] in res:
        cur.execute(f"SELECT {row['salary_currency']} FROM currency WHERE Date = ?", (row["published_at"][:7],))
        res = row["salary"] * float(cur.fetchone()[0])
        return round(res, 2)
    return row["salary"]


def get_page(page, hours):
    """
    Отправляет запрос и получает выгрузку с сайта hh.ru по сто вакансий за страницу
    Args:
        page: Страница, для выгрузки
        hours: Вакансии после полудня

    Returns:
        текстовый json
    """

    params = {
        "specialization": 1,
        "found": 1,
        "per_page": 100,
        "page": page,
        "date_from": f"2022-12-14T{str(hours).zfill(2)}:00:00+0300",
        "date_to": f"2022-12-14T{str(hours + 1).zfill(2)}:59:00+0300"
    }
    try:
        req = requests.get('https://api.hh.ru/vacancies', params)
        data = req.content.decode()
        req.close()
    except:
        print("Запрос прошёл неудачно... пробую ещё")
        return get_page(page, hours)
    print("Запрос прошёл успешно")
    return data


def set_vacancies():
    """
    Собирает данные с сайта HH.ru и сохраняет в csv файл
    """
    df = pd.DataFrame()
    for i in range(23):
        for page in range(0, 22):
            js_obj = json.loads(get_page(page, i))
            df = pd.concat((df, json_normalize(js_obj["items"])))
            if (js_obj['pages'] - page) <= 1:
                break
            time.sleep(2)
    df = df[["name", "salary.from", "salary.to", "salary.currency", "area.name", "published_at"]]
    df.columns = ["name", "salary_from", "salary_to", "salary_currency", "area_name", "published_at"]
    df.to_csv("vacs_from_hh.csv", index=False)


currency_conversion("vacancies_dif_currencies.csv")
