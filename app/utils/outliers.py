# outliers.py
from scipy.stats import zscore

def detect_outliers(data):
    # Обчислення Z-score для колонок "Кількість" та "Сума"
    z_scores = data[["Кількість", "Сума"]].apply(zscore)
    # Виявлення викидів (значення Z-score > 3 або < -3)
    outliers = data[(z_scores > 3).any(axis=1) | (z_scores < -3).any(axis=1)]
    return outliers