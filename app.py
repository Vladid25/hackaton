import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Використання бекенду Agg для уникнення попереджень GUI
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore
from flask import Flask, render_template

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
def analyze_data(data):
    # Перевірка на пропущені значення
    missing_values = data.isnull().sum()
    # Статистичний опис даних
    data_description = data.describe()
    return missing_values, data_description
def visualize_data(data):
    # Візуалізація розподілу даних
    data.hist(bins=50, figsize=(20, 15))
    plt.savefig('static/images/histogram.png')
    plt.close()
    # Boxplot для кожної числової колонки
    data.select_dtypes(include=['float64', 'int64']).plot(kind='box', subplots=True, layout=(2, 3), figsize=(15, 10), title='Boxplot for Numerical Columns')
    plt.savefig('static/images/boxplot.png')
    plt.close()
    # Видалення нечислових даних для кореляційної матриці
    numeric_data = data.select_dtypes(include=['float64', 'int64'])
    # Кореляційна матриця
    plt.figure(figsize=(15, 10))
    sns.heatmap(numeric_data.corr(), annot=True, fmt='.2f', cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.savefig('static/images/correlation_matrix.png')
    plt.close()
    # Розподіл кожної змінної
    for column in numeric_data.columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(data[column].dropna(), kde=True)
        plt.title(f'Distribution of {column}')
        plt.savefig(f'static/images/distribution_{column}.png')
        plt.close()

def detect_outliers(data):
    # Обчислення Z-score для кожної числової колонки
    z_scores = data.select_dtypes(include=['float64', 'int64']).apply(zscore)

    # Виявлення викидів (значення Z-score > 3 або < -3)
    outliers = z_scores[(z_scores > 3) | (z_scores < -3)].dropna(how='all')
    return outliers

def feature_importance(data):
    # Припускаємо, що остання колонка є цільовою змінною
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    # Перетворення цільової змінної на числові значення, якщо вона категоріальна
    if y.dtype == 'object':
        y = LabelEncoder().fit_transform(y)

    # Видалення колонок з датами
    X = X.select_dtypes(exclude=['datetime'])

    # Кодування категоріальних змінних
    label_encoders = {}
    for column in X.select_dtypes(include=['object']).columns:
        label_encoders[column] = LabelEncoder()
        X[column] = label_encoders[column].fit_transform(X[column])

    # Розділення даних на тренувальний і тестовий набори
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Навчання моделі RandomForest
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Отримання важливості фіч
    importances = model.feature_importances_
    feature_importance = pd.Series(importances, index=X.columns).sort_values(ascending=False)

    return feature_importance


@app.route('/')
def index():
    data = pd.read_excel('static/uploads/Online Sales Data.xlsx')

    # Вибірка перших 5 рядків даних
    sample_data = data.head(5).to_html(classes='table table-striped', index=False)

    # Аналітика даних
    missing_values, data_description = analyze_data(data)

    # Форматування результатів аналітики
    analysis = f"Missing Values:<br>{missing_values.to_frame().to_html(classes='table table-striped')}<br><br>Data Description:<br>{data_description.to_html(classes='table table-striped')}"

    # Виявлення викидів
    outliers = detect_outliers(data)
    outliers_text = f"Outliers detected:<br>{outliers.to_html(classes='table table-striped')}"

    # Візуалізація даних
    visualize_data(data)

    # Визначення впливовості факторів
    feature_importance_values = feature_importance(data)
    feature_importance_text = f"Feature Importance:<br>{feature_importance_values.to_frame().to_html(classes='table table-striped')}"

    return render_template('index.html', sample_data=sample_data, analysis=analysis, outliers_text=outliers_text, feature_importance_text=feature_importance_text)

if __name__ == '__main__':
    app.run(debug=True)
