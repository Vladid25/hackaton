# visualization.py
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def visualize_data(data):
    # Візуалізація розподілу даних для колонок "Кількість" та "Сума"
    plt.figure(figsize=(10, 6))
    sns.histplot(data["Кількість"].dropna(), kde=True)
    plt.title('Distribution of Кількість')
    plt.savefig('app/static/images/distribution_quantity.png')
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.histplot(data["Сума"].dropna(), kde=True)
    plt.title('Distribution of Сума')
    plt.savefig('app/static/images/distribution_sum.png')
    plt.close()

    # Boxplot для колонок "Кількість" та "Сума"
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data[["Кількість", "Сума"]])
    plt.title('Boxplot for Кількість and Сума')
    plt.savefig('app/static/images/boxplot.png')
    plt.close()