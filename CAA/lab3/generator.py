import numpy as np
import math
from readFuncs import dataReader


def generateMatrix() -> list:
    """
    Функция запрашивает из стандартного потока ввода, правила генерации, после чего генерирует 2мерный список
    :return: возвращает 2мерный список (матрицу весов)
    """
    n, min, max, symmetry = dataReader()  # получаем правили генерации
    rng = np.random.default_rng()  # создаем объект генератора

    if symmetry:  # если нужна симметричная матрица весов
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                num = rng.integers(low=min, high=max)
                matrix[i][j] = num
                matrix[j][i] = num
    else:  # если полностью случайная
        matrix = rng.integers(low=min, high=max, size=(n, n)).tolist()
    # расстанавливаем бесконечности по главной диагонали
    for i in range(n):
        matrix[i][i] = math.inf
    return matrix


def saveMatrix(filename, matrix):
    """
    Функция сохраняет матрицу весов в файл.
    :param filename: название файла, в который сохраняют
    :param matrix: матрица весов
    :return: функция ничего не возвращает
    """
    file = open(filename, "w")  # открываем на запист файл
    for row in matrix:
        string = " ".join([str(elem) for elem in row])  # преобразуем строку матрицы в строку
        file.write(f"{string}\n")  # записываем строчку в файл
    file.close()  # закрываем файл


def main():
    filename = input("Введите название файла: ")
    saveMatrix(filename, generateMatrix())


if __name__ == "__main__":
    main()
