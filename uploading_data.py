from multiprocessing import Pool
import pathlib
import pandas as pd


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


def prepare_data(file_name, prof):
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
    a = df["published_at"].apply(lambda s: int(s[:4])).unique()
    salary_by_year = int(df[["salary_from", "salary_to"]].mean(axis=1).mean())
    vac_counts_by_year = df[df["name"] == prof]
    vac_salary_by_year = int(vac_counts_by_year[["salary_from", "salary_to"]].mean(axis=1).mean())
    return [a[0], salary_by_year, len(vac_counts_by_year), vac_salary_by_year, len(df)]


def main(folder, prof):
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
        with Pool(None) as pool:
            for x in range(len(file_list)):
                i = pool.apply_async(prepare_data, (file_list[x],prof)).get()
                salary_by_years[i[0]] = i[1]
                vac_counts_by_years[i[0]] = i[2]
                vac_salary_by_years[i[0]] = i[3]
                vacs_by_years[i[0]] = i[4]
        return salary_by_years, vacs_by_years, vac_salary_by_years, vac_counts_by_years
