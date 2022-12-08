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
    print(df.head(10))
    print(years)
