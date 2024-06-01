import pandas as pd

def analyze_data(data):
    # Перевірка на пропущені значення
    missing_values = data.isnull().sum()
    # Статистичний опис даних
    data_description = data.describe()
    return missing_values, data_description
