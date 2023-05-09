def readMatrix(filename) -> list:
    """
    Функция считывает из файла матрицу весов
    :param filename: название файла из которого считывают
    :return: возврщает двумерный список (матрицу весов)
    """
    file = open(filename, "r")  # открываем файл на чтение
    matrix = []
    for row in file:  # пока есть строчки в файле
        line = row.split()  # делим считаную строку
        # выполняем привидение типа для каждого элемента строки
        for index, item in enumerate(line):
            try:
                item = int(item)
            except ValueError:
                item = float(item)
            line[index] = item
        # преобразованую строчку добавляем в матрицу
        matrix.append(line)
    return matrix


def dataReader():
    """
    Функция считывает из стандартного потока ввода правила генерации
    :return: возвразает кортеж из кол-ва узлов, мин-веса, макс-веса, флага симметричности
    """
    count = int(input("Введите количество узлов, для генерации: "))
    max = int(input("Введите максимальное значение веса: "))
    min = int(input("Введите минимальное значение веса: "))
    symmetry = "nothing"
    while symmetry not in ["yes", "not"]:
        symmetry = input("Нужна ли симметричная матрица(yes or not): ")
    symmetry = True if symmetry == "yes" else False
    return count, min, max, symmetry
