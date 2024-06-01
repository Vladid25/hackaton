from flask import render_template, current_app as app
import pandas as pd
from .utils.analysis import analyze_data
from .utils.visualization import visualize_data
from .utils.outliers import detect_outliers
from .utils.feature_importance import feature_importance

@app.route('/')
def index():
    data = pd.read_excel('hackaton/hackaton2/app/static/uploads/Online Sales Data.xlsx')

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
