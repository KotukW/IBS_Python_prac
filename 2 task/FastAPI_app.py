from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
import numpy as np

app = FastAPI()

def average_age_by_position(file_path):
    """
    Вычисляет средний возраст для каждой должности из файла CSV.

    Args:
    - file_path (str): Путь к файлу CSV с данными о сотрудниках. Файл должен содержать столбцы 'Имя', 'Возраст' и 'Должность'.

    Returns:
    - dict: Словарь с данными, содержащий статус код и средний возраст по каждой должности.
      Если файл не содержит необходимых столбцов, возвращает статус код 400 и сообщение о невалидном файле.
    """

    data = pd.read_csv(file_path)
    if set(['Имя', 'Возраст', 'Должность']).issubset(set(data.columns)):
        average_age = data.groupby('Должность')['Возраст'].mean().to_dict()
        processed_data = {key: None if pd.isna(value) else value for key, value in average_age.items()}
        return {"status_code": 200, "data": processed_data}
    else:
        return {"status_code": 400, "data": "Невалидный файл"}

@app.post("/average_age_by_position")
def get_average_age_by_position(file: UploadFile = File(...)):
    """
    Обрабатывает запрос на вычисление среднего возраста сотрудников по должностям на основе загруженного файла.

    Args:
    - file (UploadFile, required): Загружаемый файл (CSV) с данными о сотрудниках.

    Returns:
    - dict: Словарь с данными, содержащий статус код и средний возраст по каждой должности.
      В случае возникновения ошибки возвращает статус код 400 и детали ошибки.
    """
    
    try:
        file_path = f"{file.filename}"
        result = average_age_by_position(file_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))