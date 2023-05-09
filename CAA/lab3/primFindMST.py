import math
from readFuncs import readMatrix


def primFindMST(matrix, startVertex=0):
    """
    Функция строит минимально остовное дерево из стартовой вершины, по алгоритму Прима
    :param matrix: матрица весов
    :param startVertex: стартовая вершина
    :return: возврщает матрицу весов остовного дерева, и вес остовного дерева
    """
    size = len(matrix)
    # инициализируем матрицу весов остовного дерева
    mst = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        mst[i][i] = math.inf
    # задаем список посещенных вершин
    visited = [startVertex]
    weight = []
    # пока не посетили все вершины
    while len(visited) != size:
        # ищем минимальное ребро ведущее в ещё не включенную вершину
        min_w = math.inf
        i, j = 0, 0
        for elem in visited:
            if min_w > min(matrix[elem]):
                # найдено более выгодное ребро, сохраняем его
                min_w = min(matrix[elem])
                i = elem
                j = matrix[elem].index(min_w)
            elif min(matrix[elem]) == math.inf:
                # если минимального нет, то граф не дерево
                raise RuntimeError("The tree is not unit")
        # добавляем ребро если мы ещё не посещали концевую вершину
        if j not in visited:
            weight.append(min_w)
            visited.append(j)
            mst[i][j] = min_w
        # затираем ребро в исходной матрице, чтоб снова его не взять
        matrix[i][j] = math.inf
    return mst, sum(weight)


def main():
    print(sum(primFindMST(readMatrix("matrix.txt"), 1)[1]))


if __name__ == "__main__":
    main()
