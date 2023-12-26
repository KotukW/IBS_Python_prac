import random
import string
import json
import csv
import yaml
from abc import ABC, abstractmethod
from io import StringIO

class BaseWriter(ABC):
    """
    Абстрактный класс с методом write для генерации файла
    """

    @abstractmethod
    def write(self, data: list[list[int, str, float]]) -> StringIO:
        """
        Записывает данные в строковый объект файла StringIO
        :param data: полученные данные
        :return: Объект StringIO с данными из data
        """
        pass

class JSONWriter(BaseWriter):
    """
    Потомок BaseWriter с переопределением метода write для генерации файла в json формате
    """

    def write(self, data: list[list[int, str, float]]) -> StringIO:
        json_data = json.dumps(data)
        string_io = StringIO(json_data)
        return string_io

class CSVWriter(BaseWriter):
    """
    Потомок BaseWriter с переопределением метода write для генерации файла в csv формате
    """

    def write(self, data: list[list[int, str, float]]) -> StringIO:
        string_io = StringIO()
        csv_writer = csv.writer(string_io)
        csv_writer.writerows(data)
        string_io.seek(0)
        return string_io

class YAMLWriter(BaseWriter):
    """
    Потомок BaseWriter с переопределением метода write для генерации файла в yaml формате
    """

    def write(self, data: list[list[int, str, float]]) -> StringIO:
        yaml_data = yaml.dump(data)
        string_io = StringIO(yaml_data)
        return string_io

class DataGenerator:
    def __init__(self, data: list[list[int, str, float]] = None):
        self.data: list[list[int, str, float]] = data

    def generate(self) -> None:
        """
        Генерирует матрицу данных размера 4x4
        """
        data = []
        for _ in range(4):
            row = [
                random.randint(1, 10),
                random.choice(string.ascii_uppercase),
                round(random.uniform(1.0, 10.0), 2)
            ]
            data.append(row)
        self.data = data

    def to_file(self, path: str, writer: BaseWriter) -> None:
        """
        Метод для записи в файл данных полученных после генерации.
        Если данных нет, то вызывается кастомный Exception.
        :param path: Путь куда требуется сохранить файл
        :param writer: Одна из реализаций классов потомков от BaseWriter
        """
        if self.data is None:
            raise ValueError("Данные не были сгенерированы")

        with open(path, 'w') as file:
            string_io = writer.write(self.data)
            file.write(string_io.getvalue())

generator = DataGenerator()
generator.generate()


json_writer = JSONWriter()
csv_writer = CSVWriter()
yaml_writer = YAMLWriter()

try:
    generator.to_file('7. Генерация файлов в форматах CSV, JSON и YAML\data.json', json_writer)
    generator.to_file('7. Генерация файлов в форматах CSV, JSON и YAML\data.csv', csv_writer)
    generator.to_file('7. Генерация файлов в форматах CSV, JSON и YAML\data.yaml', yaml_writer)
except ValueError as e:
    print(e)