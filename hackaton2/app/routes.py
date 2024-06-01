from flask import render_template, current_app as app
import pandas as pd
from .utils.analysis import analyze_data
from .utils.visualization import visualize_data
from .utils.outliers import detect_outliers
from .utils.feature_importance import feature_importance

@app.route('/')
def index():
    data = pd.read_excel('hackaton/hackaton2/app/static/uploads/dataset.xlsx')
    # Видалення рядків за умовою в колонці 'Дата'
    data.drop(data[data['Дата'] == 'Лопатка силікон з принтом 29,5*5*1см'].index, inplace=True)
    sample_data = data.head(5).to_html(classes='table table-striped', index=False)

    missing_values, data_description = analyze_data(data)

    analysis = f"Missing Values:<br>{pd.DataFrame(missing_values).to_html(classes='table table-striped')}<br><br>Data Description:<br>{pd.DataFrame(data_description).to_html(classes='table table-striped')}"
    outliers = detect_outliers(data)
    outliers_text = f"Outliers detected:<br>{pd.DataFrame(outliers).to_html(classes='table table-striped')}"
    visualize_data(data)

    #feature_importance_values = feature_importance(data)
    #feature_importance_text = f"Feature Importance:<br>{pd.DataFrame(feature_importance_values).to_html(classes='table table-striped')}"
    return render_template('reserv.html', sample_data=sample_data, analysis=analysis, outliers_text=outliers_text)
