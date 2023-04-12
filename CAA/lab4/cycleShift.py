DEBUG = True


def prefixFunction(pattern: str) -> list:
    """
    Функция принимает на вход строку и высчитывает для каждой подстроки [1…i]
    значение префикс-функции. При этом на каждом шаге используется информация
    о длине максимального префикса на предыдущем шаге, что ускоряет подсчёт.
    :param pattern: стока для который вычисляют префикс функцию
    :return: массив из элементов, обозначающих длину максимального префикса строки, совпадающего с её суффиксом
    """
    global DEBUG
    size = len(pattern)
    result = [0] * size

    j, i = 0, 1
    while i < size:
        if pattern[i] == pattern[j]:  # символы совпали
            result[i] = j + 1  # увеличиваем текущую длину
            if DEBUG:
                print(f"Символы ({pattern[i]}) совпали на индексах j={j} i={i}")
                print(f"Текущий префикс/суфикс: {pattern[:j + 1]}")
                print(f"Записываем значение result[{i}]={j + 1}")
                print(result, end="\n\n")
            j += 1  # увеличиваем индексы
            i += 1
        else:
            if j == 0:
                if DEBUG:
                    print(f"Суфикс/префикс на текущей итерации не найден ({pattern[j]} != {pattern[i]}):")
                    print(f"Записываем значение result[{i}]=0")
                    print("Идем к следующему символу")
                    print("\n")
                result[i] = 0  # сопадений нет
                i += 1  # к следующему символу
            else:
                if DEBUG:
                    print(f"Рассматриваем предыдущую длину: {result[j - 1]}")
                    print("\n")
                j = result[j - 1]  # возвращаемя с предыдущей длине
    if DEBUG:
        print("Массив префикс функции")
        print(result, end="\n\n")
    return result


def algorithmKMP(pattern: str, text: str) -> int:
    """
    Посредством посимвольного сравнения двух строк определятся совпадение подстроки pattern
    со строкой text. Если все символы совпали – вхождение найдено
    и в результат возвращается.
    Если первые символы не совпали, то первый символ pattern
    сравнивается со вторым text и так далее до попадания. Если
    символ pattern не совпадает с символом text, то следующее сравнение происходит
    с символом подстроки P под индексом префикс-функции предыдущего символа.
    Эти действия будут повторяться до тех пор, пока не будет
    достигнут последний символ строки text.
    :param pattern: подстрока, вхождение которой ищут
    :param text: строка в которой ищут вхождение
    :return: список индексов вхождений
    """
    global DEBUG
    patternSize, textSize = len(pattern), len(text)
    prefArray = prefixFunction(pattern)
    i = 0
    j = 0
    if DEBUG:
        print("ИНИЦИАЛИЗАЦИЯ АЛГОРИТМА КМП:")
        print(f"pattern={pattern}, text={text}, i={i}, j={j}\n")
    while j < textSize:
        if pattern[i] == text[j]:  # символы совпали
            if DEBUG:
                print(f"Символы ({pattern[i]}) совпали на индексах i={i} j={j}")
                print(f"Текущий вхождение имеет вид: {pattern[:i + 1]}\n")
            i += 1  # идем дальше
            j += 1
            if i == patternSize:  # нашли вхождение
                if DEBUG:
                    print("Нашли вхождение")
                    print(f"На индексе: {j - i}")
                    print(f"Выходим из функции\n")
                return j - i  # прекращаем поиск выводя индекс
        else:
            if i == 0:
                if DEBUG:
                    print(f"Символ ({text[j]}) не является началом вхождения подстроки, идем к следующему символу строки\n")
                j += 1  # идем к следующему
            else:
                if DEBUG:
                    print(f"Нашли различные символы ({pattern[i]} != {text[j]}) и i({i})>0 из-за чего")
                    print(f"Рассматриваем предыдущую длину: {prefArray[i - 1]}\n")
                i = prefArray[i - 1]  # востанавливаем индекс паттерна
    if DEBUG:
        print("text - не является циклической престановкой,")
        print("возвращаем -1")
    return -1


def main():
    # считываем данные
    text = input()
    pattern = input()
    # если разная длина выводим сразу ответ
    if len(text) != len(pattern):
        print(-1)
        return
    # иначе запускаем алгоритм КМП для склеиного текста
    print(algorithmKMP(pattern, text * 2))


if __name__ == "__main__":
    main()
