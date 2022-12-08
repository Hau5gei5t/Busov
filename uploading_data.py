import pandas as pd

def upload_chunks():
    pd.set_option("expand_frame_repr", False)
    df = pd.read_csv("vacancies_by_year.csv")
    df["years"] = df["published_at"].apply(lambda s: int(s[:4]))
    years = df["years"].unique()
    for year in years:
        data = df[df["years"] == year]
        data.iloc[:, :6].to_csv(rf"csv_files\year_{year}.csv", index=False)
    print(df.head(10))
    print(years)

upload_chunks()