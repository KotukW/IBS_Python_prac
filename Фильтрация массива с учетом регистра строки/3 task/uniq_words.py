"""
Реализуйте функцию соответствующую следующему описанию:
На вход подаётся массив слов зависимых от регистра, для которых необходимо произвести
фильтрацию на основании дублей слов, если в списке найден дубль по регистру, то все
подобные слова вне зависимости от регистра исключаются.
На выходе должны получить уникальный список слов в нижнем регистре.
"""

def find_in_different_registers(words: list[str]):
    words_dict = {}
    bad_words = []
    for word in words:
        if word not in words_dict:
            words_dict[word] = 1
        elif word.lower() not in bad_words:
            bad_words.append(word.lower())
    return list(set([key.lower() for key in words_dict if key.lower() not in bad_words]))

print(find_in_different_registers(['Мама', 'МАМА', 'Мама', 'папа', 'ПАПА', 'Мама', 'ДЯдя', 'брАт',
'Дядя', 'Дядя', 'Дядя']))