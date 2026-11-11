from colorama import Fore, Style
import os
print(Fore.CYAN + "=== Учебный центр. Подготовка данных ===" + Style.RESET_ALL)
fio = input("Введите фамилию: ")
while True:
    n_str = input("Введите номер варианта N от 1 до 30: ")
    N = int(n_str)
    if 1 <= N <= 30:
        break
    print("N должен быть от 1 до 30. Попробуйте ещё раз.")
A = N % 5
B = N % 4
T = 65 + A
P = 75 + B
print(Fore.GREEN + "Исполнитель:", fio)
print("Вариант N =", N)
print("A =", A, "B =", B, "T =", T, "P =", P)
print(Style.RESET_ALL)
students = [
    {"ID": 1, "Имя": "Анна", "Группа": "Альфа", "Тест1": 54, "Тест2": 62, "Тест3": 70, "Посещаемость": 70},
    {"ID": 2, "Имя": "Борис", "Группа": "Бета", "Тест1": 76, "Тест2": 80, "Тест3": 84, "Посещаемость": 82},
    {"ID": 3, "Имя": "Вера", "Группа": "Гамма", "Тест1": 88, "Тест2": 92, "Тест3": 86, "Посещаемость": 90},
    {"ID": 4, "Имя": "Глеб", "Группа": "Альфа", "Тест1": 60, "Тест2": "", "Тест3": 68, "Посещаемость": 76},
    {"ID": 5, "Имя": "Дарья", "Группа": "Бета", "Тест1": 70, "Тест2": 74, "Тест3": 78, "Посещаемость": 79},
    {"ID": 6, "Имя": "Егор", "Группа": "Гамма", "Тест1": 40, "Тест2": 55, "Тест3": 50, "Посещаемость": 68},
    {"ID": 7, "Имя": "Жанна", "Группа": "Альфа", "Тест1": 80, "Тест2": 84, "Тест3": 88, "Посещаемость": 92},
    {"ID": 8, "Имя": "Захар", "Группа": "Бета", "Тест1": 58, "Тест2": 64, "Тест3": 60, "Посещаемость": 74},
    {"ID": 9, "Имя": "Ирина", "Группа": "Гамма", "Тест1": 90, "Тест2": 94, "Тест3": 92, "Посещаемость": 95},
    {"ID": 10, "Имя": "Кирилл", "Группа": "Альфа", "Тест1": 66, "Тест2": 70, "Тест3": 72, "Посещаемость": 80},
    {"ID": 11, "Имя": "Лена", "Группа": "Бета", "Тест1": 72, "Тест2": "", "Тест3": 76, "Посещаемость": 77},
    {"ID": 12, "Имя": "Максим", "Группа": "Гамма", "Тест1": 48, "Тест2": 52, "Тест3": 56, "Посещаемость": 72},
]
for s in students:
    s["Тест1"] = s["Тест1"] + A
    if s["Тест2"] != "":
        s["Тест2"] = s["Тест2"] + A
    s["Тест3"] = s["Тест3"] + A
    s["Посещаемость"] = s["Посещаемость"] + B
print("Первый элемент:", students[0])
print("Последний элемент:", students[-1])
print("Группа у второй записи:", students[1]["Группа"])
print("Всего записей:", len(students))
groups = ["Альфа", "Бета", "Гамма"]
g = input("Введите название группы для проверки: ")
if g in groups:
    print("Группа есть в списке")
else:
    print("Такой группы нет")
names = ["Анна", "Борис", "Вера"]
print("Длина до:", len(names))
names.append("Тест")
print("После append:", names)
names.pop()
print("После pop:", names)
print("Длина после:", len(names))
total_sum = 0
count_all = 0
admitted_count = 0
for s in students:
    skip = s["Тест2"] == ""
    t1 = s["Тест1"]
    t2 = 0 if skip else s["Тест2"]
    t3 = s["Тест3"]
    suma = t1 + t2 + t3
    avg = suma / 3
    s["Сумма"] = suma
    s["Среднее"] = avg
    s["Пропуск"] = skip
    if avg >= 85:
        level = "высокий"
    elif avg >= T:
        level = "базовый"
    else:
        level = "требуется подготовка"
    s["Уровень"] = level
    reasons = []
    if avg < T:
        reasons.append("низкое среднее")
    if s["Посещаемость"] < P:
        reasons.append("низкая посещаемость")
    if skip:
        reasons.append("отсутствующий результат")
    s["Причины"] = reasons
    ok = avg >= T and s["Посещаемость"] >= P and not skip
    s["Допуск"] = ok
    if ok:
        admitted_count += 1
    total_sum += suma
    count_all += 3
common_avg = total_sum / count_all
print("Общая сумма:", total_sum)
print("Общее среднее:", round(common_avg, 2))
print("Допущено:", admitted_count)
os.makedirs("data", exist_ok=True)
with open("data/source.csv", "w", encoding="utf-8") as f:
    f.write("ID,Имя,Группа,Тест1,Тест2,Тест3,Посещаемость\n")
    for s in students:
        t2 = "" if s["Тест2"] == "" else str(s["Тест2"])
        line = str(s["ID"]) + "," + s["Имя"] + "," + s["Группа"] + "," + str(s["Тест1"]) + "," + t2 + "," + str(s["Тест3"]) + "," + str(s["Посещаемость"]) + "\n"
        f.write(line)
os.makedirs("results", exist_ok=True)
with open("results/python_report.txt", "w", encoding="utf-8") as f:
    f.write("Исполнитель: " + fio + "\n")
    f.write("Вариант: " + str(N) + "\n")
    f.write("A=" + str(A) + " B=" + str(B) + " T=" + str(T) + " P=" + str(P) + "\n\n")
    for s in students:
        f.write("ID " + str(s["ID"]) + " " + s["Имя"] + " среднее=" + str(round(s["Среднее"], 2)) + " уровень=" + s["Уровень"] + " допуск=" + str(s["Допуск"]))
        if s["Причины"]:
            f.write(" причины: " + ", ".join(s["Причины"]))
        f.write("\n")
    f.write("\nОбщая сумма: " + str(total_sum) + "\n")
    f.write("Общее среднее: " + str(round(common_avg, 2)) + "\n")
    f.write("Допущено: " + str(admitted_count) + "\n")
with open("data/source.csv", "r", encoding="utf-8") as f:
    lines = f.readlines()
print("Первые 3 строки source.csv:")
for i in range(3):
    print(lines[i].strip())
data_rows = 0
for line in lines[1:]:
    if line.strip():
        data_rows += 1
print("Строк данных:", data_rows)
with open("journal.txt", "a", encoding="utf-8") as j:
    j.write("Этап 1-3 завершён. source.csv и python_report.txt созданы.\n")
    j.write("Общая сумма " + str(total_sum) + " среднее " + str(round(common_avg, 2)) + " допущено " + str(admitted_count) + "\n")
print("Готово. Файлы записаны.")