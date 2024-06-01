import matplotlib.pyplot as plt
import seaborn as sns

def visualize_data(data):
    # Візуалізація розподілу даних
    data.hist(bins=50, figsize=(20, 15))
    plt.savefig('app/static/images/histogram.png')
    plt.close()
    # Boxplot для кожної числової колонки
    data.select_dtypes(include=['float64', 'int64']).plot(kind='box', subplots=True, layout=(2, 3), figsize=(15, 10), title='Boxplot for Numerical Columns')
    plt.savefig('app/static/images/boxplot.png')
    plt.close()
    # Видалення нечислових даних для кореляційної матриці
    numeric_data = data.select_dtypes(include=['float64', 'int64'])
    # Кореляційна матриця
    plt.figure(figsize=(15, 10))
    sns.heatmap(numeric_data.corr(), annot=True, fmt='.2f', cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.savefig('app/static/images/correlation_matrix.png')
    plt.close()
    # Розподіл кожної змінної
    for column in numeric_data.columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(data[column].dropna(), kde=True)
        plt.title(f'Distribution of {column}')
        plt.savefig(f'app/static/images/distribution_{column}.png')
        plt.close()
