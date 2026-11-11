import pandas as pd
import os
N = 11
A = N % 5
B = N % 4
T = 65 + A
P = 75 + B
print("N=", N, "A=", A, "B=", B, "T=", T, "P=", P)
df = pd.read_csv("data/source.csv")
print(df.head())
print(df.tail())
print("shape:", df.shape)
print("columns:", df.columns.tolist())
print(df.dtypes)
df.info()
print(df.describe())
df["Пропуск_Тест2"] = df["Тест2"].isna()
print("Пропуски до:")
print(df.isna().sum())
print("Ожидалось 2 пропуска в Тест2")
df_drop = df.dropna()
print("После dropna осталось строк:", len(df_drop))
print("Удалились бы ID:", set(df["ID"]) - set(df_drop["ID"]))
df["Тест2"] = df["Тест2"].fillna(0)
print("Пропуски после fillna:")
print(df.isna().sum())
df["Сумма"] = df["Тест1"] + df["Тест2"] + df["Тест3"]
df["Среднее"] = df["Сумма"] / 3
levels = []
admits = []
for i, row in df.iterrows():
    avg = row["Среднее"]
    if avg >= 85:
        levels.append("высокий")
    elif avg >= T:
        levels.append("базовый")
    else:
        levels.append("требуется подготовка")
    ok = avg >= T and row["Посещаемость"] >= P and not row["Пропуск_Тест2"]
    admits.append(ok)
df["Уровень"] = levels
df["Допуск"] = admits
df["Среднее_округл"] = df["Среднее"].round(2)
s = pd.Series(df["Среднее"].values, index=df["ID"])
print("Среднее ID 4:", s[4])
df2 = df.set_index("ID")
print("loc[4]:", df2.loc[4]["Имя"])
print("iloc[3]:", df2.iloc[3]["Имя"])
print("loc по метке ID, iloc по позиции")
os.makedirs("results", exist_ok=True)
df.to_csv("results/cleaned.csv", index=False, encoding="utf-8")
df_check = pd.read_csv("results/cleaned.csv")
print("Строк после загрузки:", len(df_check))
print("Пропусков:", df_check.isna().sum().sum())
print("Пропуск_Тест2 True:", df_check["Пропуск_Тест2"].sum())
total_sum = df["Сумма"].sum()
total_avg = df["Среднее"].mean()
adm_count = df["Допуск"].sum()
print("Сумма Pandas:", total_sum)
print("Среднее Pandas:", total_avg)
print("Допущено:", adm_count)
admitted = df[df["Допуск"] == True].sort_values(["Среднее", "ID"], ascending=[False, True])
admitted[["ID", "Имя", "Группа", "Среднее", "Посещаемость"]].to_csv("results/admitted.csv", index=False, encoding="utf-8")
df["низкое_среднее"] = df["Среднее"] < T
df["низкая_посещ"] = df["Посещаемость"] < P
df["был_пропуск"] = df["Пропуск_Тест2"]
attention = df[(df["Среднее"] < T) | (df["Посещаемость"] < P) | (df["Пропуск_Тест2"] == True)]
attention.to_csv("results/attention.csv", index=False, encoding="utf-8")
strong = df[(df["Среднее"] >= T) & (df["Посещаемость"] >= P)]
strong.to_csv("results/strong_attendance.csv", index=False, encoding="utf-8")
group_sel = df[df["Группа"] == "Гамма"].sort_values(["Среднее", "ID"], ascending=[False, True])
group_sel.to_csv("results/group_selection.csv", index=False, encoding="utf-8")
g = df.groupby("Группа").agg(
    mean_avg=("Среднее", "mean"),
    min_avg=("Среднее", "min"),
    max_avg=("Среднее", "max"),
    count=("ID", "count"),
    mean_att=("Посещаемость", "mean"),
    admitted=("Допуск", "sum")
).reset_index()
g = g.sort_values(["mean_avg", "Группа"], ascending=[False, True])
g.to_csv("results/summary.csv", index=False, encoding="utf-8")
print(g)
print("admitted ID:", admitted["ID"].tolist())
print("attention ID:", attention["ID"].tolist())
print("Pandas готово")