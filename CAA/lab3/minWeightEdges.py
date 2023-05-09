from readFuncs import readMatrix
import math


def minWeightEdges(matrix):
    """
    Функция находит полусумму двух минимальных ребер
    :param matrix: матрица весов
    :return: возвращает полусумму двух минимальных ребер
    """
    # инициализируем значения как бесконечность
    first, second = math.inf, math.inf
    # проходимся по все матрице
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            # если вес легче первого минимального, то это значение становится первым минимальным,
            # а изначальное уходит второму
            if matrix[i][j] < first:
                second = first
                first = matrix[i][j]
            elif first < matrix[i][j] < second: # если найденное меньше только второгу, то перезаписываем второе
                second = matrix[i][j]
    # возвращаем полусумму
    return (first + second) / 2


def main():
    print(minWeightEdges(readMatrix("matrix.txt")))


if __name__ == "__main__":
    main()
