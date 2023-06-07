from readFuncs import readMatrix
import math


def minWeightEdges(matrix, remainVertex):
    """
    Функция находит сумму полусумм двух легчайших смежных ребер для каждой вершины в оставшихся вершинах
    :param matrix: 2мерный список матрица весов
    :param remainVertex: список оставшихся вершин
    :return: возвращает найденное значение
    """
    if len(remainVertex) <= 1:
        return 0
    if len(remainVertex) == 2:
        return (matrix[remainVertex[0]][remainVertex[1]] + matrix[remainVertex[1]][remainVertex[0]]) / 2
    first, second = math.inf, math.inf
    # инициализируем значения как бесконечность
    for i in remainVertex:
        for j in remainVertex:
            if i == j:
                continue
            # если вес легче первого минимального, то это значение становится первым минимальным,
            # а изначальное уходит второму
            if matrix[i][j] <= first:
                second, first = first, matrix[i][j]
            elif first < matrix[i][j] < second:  # если найденное меньше только второгу, то перезаписываем второе
                second = matrix[i][j]
    return (first + second) / 2


def main():
    print(minWeightEdges(readMatrix("matrix.txt"), [0, 1, 2, 3, 4, 5]))


if __name__ == "__main__":
    main()