import pandas as pd 

def avg_jobtitle_age(employees_csv):
    """
    Вычисляет средний возраст для каждой должности из предоставленного DataFrame сотрудников.

    Аргументы:
    employees_csv (pandas.DataFrame): DataFrame, содержащий информацию о сотрудниках.

    Возвращает:
    dict: Словарь, в котором ключи - должности, а значения - средний возраст сотрудников на каждой из должностей.
    """

    avg_age = {}
    avg_age = employees_csv.groupby('Должность')['Возраст'].mean().to_dict()
    return avg_age

employees = pd.read_csv("1. Работа с pandas и csv\\1 task\\employees.csv")
print(avg_jobtitle_age(employees))