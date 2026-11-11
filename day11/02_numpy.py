import numpy as np
import os
M = np.array([
    [55, 63, 71],   
    [77, 81, 85],   
    [89, 93, 87],   
    [61, 0, 69],  
    [71, 75, 79],   
    [41, 56, 51],   
    [81, 85, 89],  
    [59, 65, 61],  
    [91, 95, 93],   
    [67, 71, 73], 
    [73, 0, 77],  
    [49, 53, 57],   
], dtype=float)
print("type:", type(M))
print("dtype:", M.dtype)
print("ndim:", M.ndim)
print("shape:", M.shape)
print("size:", M.size)
print("Первая строка ID1:", M[0])
print("Последняя строка ID12:", M[-1])
print("Второй столбец Тест2:", M[:, 1])
print("Блок 4 строки 2 столбца:", M[:4, :2])
sums_row = np.sum(M, axis=1)
means_row = np.mean(M, axis=1)
means_col = np.mean(M, axis=0)
total = np.sum(M)
avg_all = np.mean(M)
print("Суммы по участникам:", sums_row)
print("Средние по участникам:", means_row)
print("Средние по тестам:", means_col)
print("Общая сумма:", total)
print("Общее среднее:", avg_all)
print("Мин:", np.min(M), "Макс:", np.max(M))
att = np.array([73, 85, 93, 79, 82, 71, 95, 77, 98, 83, 80, 75], dtype=float)
T = 66
P = 78
mask_avg = means_row >= T
mask_att = att < P
print("Средние не ниже T, ID:", np.where(mask_avg)[0] + 1)
print("Посещаемость ниже P, ID:", np.where(mask_att)[0] + 1)
arr = np.arange(1, 37)
print("arange 1-36 shape:", arr.reshape(12, 3).shape)
print("35 элементов нельзя сделать 12x3 потому что 12*3=36")
zeros = np.zeros((12, 3))
ones = np.ones((12, 3))
print("Нули + единицы:\n", zeros + ones)
os.makedirs("results", exist_ok=True)
with open("results/numpy_report.txt", "w", encoding="utf-8") as f:
    f.write("Общая сумма NumPy: " + str(total) + "\n")
    f.write("Общее среднее NumPy: " + str(avg_all) + "\n")
    f.write("Суммы по строкам: " + str(sums_row.tolist()) + "\n")
    f.write("Средние по строкам: " + str(means_row.tolist()) + "\n")
M2 = M.copy()
print("До изменения сумма:", np.sum(M2))
M2[0, 2] = M2[0, 2] + 6
print("После +6 к Тест3 ID1 сумма:", np.sum(M2))
print("Среднее первой строки было", means_row[0], "стало", np.mean(M2[0]))
print("Средние по тестам изменились, суммы других строк нет")
print("NumPy готово")