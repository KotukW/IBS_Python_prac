import pandas as pd 
"""
Напишите функцию, которая принимает на вход CSV файл с данными о сотрудниках компании.
В файле должны быть следующие колонки: "Имя", "Возраст", "Должность".
Функция должна вернуть словарь, в котором ключами являются уникальные должности, а
значениями — средний возраст сотрудников на каждой должности.
"""

def avg_jobtitle_age(employees_csv):
    avg_age = {}
    avg_age = employees_csv.groupby('Должность')['Возраст'].mean().to_dict()
    return avg_age

employees = pd.read_csv("1 task\employees.csv")
print(avg_jobtitle_age(employees))