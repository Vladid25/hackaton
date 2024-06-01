import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

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
