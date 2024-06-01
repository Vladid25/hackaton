from flask import render_template, current_app as app
import pandas as pd
from .utils.analysis import analyze_data, analyze_unique_values, analyze_dtypes, analyze_missing_values

@app.route('/')
def index():
    # Завантаження даних з файлу Excel
    data = pd.read_excel('app/static/uploads/HakatonData.xlsx')
    
    # Вибірка перших 5 рядків даних
    sample_data = data.head(5).to_html(classes='table table-striped', index=False)

    # Аналітика даних
    missing_values, data_description = analyze_data(data)
    unique_values = analyze_unique_values(data)
    dtypes = analyze_dtypes(data)
    missing_values_count = analyze_missing_values(data)

    # Форматування результатів аналітики
    analysis = f"""
    Missing Values:<br>{missing_values.to_frame().to_html(classes='table table-striped')}<br><br>
    Data Description:<br>{data_description.to_html(classes='table table-striped')}<br><br>
    Unique Values:<br>{unique_values.to_frame().to_html(classes='table table-striped')}<br><br>
    Data Types:<br>{dtypes.to_frame().to_html(classes='table table-striped')}<br><br>
    Missing Values Count:<br>{missing_values_count.to_frame().to_html(classes='table table-striped')}
    """

    return render_template('index.html', sample_data=sample_data, analysis=analysis)
