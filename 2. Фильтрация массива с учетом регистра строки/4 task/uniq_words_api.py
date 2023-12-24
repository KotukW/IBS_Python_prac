from fastapi import FastAPI, UploadFile, File
from typing import List

app = FastAPI()

def find_in_different_registers(words: list[str]):
    """
    Выполняет фильтрацию списка слов на основе дублей слов в зависимости от регистра.
    Если в списке найден дубль по регистру, все подобные слова исключаются.

    Аргументы:
    words (List[str]): Список слов для фильтрации.

    Возвращает:
    List[str]: Уникальный список слов в нижнем регистре после фильтрации на основе дублей.
    """
    words_dict = {}
    bad_words = []
    for word in words:
        if word not in words_dict:
            words_dict[word] = 1
        elif word.lower() not in bad_words:
            bad_words.append(word.lower())
    return list(set([key.lower() for key in words_dict if key.lower() not in bad_words]))

@app.post("/find_in_different_registers", response_model=List[str])
async def process_words(words: List[str]):
    """
    Передача полученных данных в функцию find_in_different_registers и возврат результата в консоль

    Аргументы:
    words (List[str]): Список слов для обработки.

    Возвращает:
    List[str]: Уникальный список слов в нижнем регистре после фильтрации на основе дублей.
    """
    result = find_in_different_registers(words)
    return result
