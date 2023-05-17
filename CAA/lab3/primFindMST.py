import math
from readFuncs import readMatrix


def primFindMST(matrix, remainVertex):
    """
    Функция строит минимальное остовное дерево для оставшихся вершин, по алгоритму Прима.
    :param matrix: 2мерный список матрица весов
    :param remainVertex: список оставшихся вершин
    :return: возвращает вес минимального остовного дерева
    """
    # инициализируем матрицу весов остовного дерева
    mst = [[0 for _ in range(len(matrix))] for _ in range(len(matrix))]
    for i in range(len(matrix)):
        mst[i][i] = math.inf
    size = len(remainVertex)
    if size <= 1:
        # если одна вершина то МОД равен 0
        return mst, 0
    # задаем список посещенных вершин
    visited = [remainVertex[0]]
    weight = []
    # пока не посетили все вершины
    while len(visited) != size:
        # ищем минимальное ребро ведущее в ещё не включенную вершину
        min_w = math.inf
        i, j = 0, 0
        for elem in visited:
            for newVertex in [vertex for vertex in remainVertex if vertex not in visited]:
                if min_w > matrix[elem][newVertex]:
                    # найдено более выгодное ребро, сохраняем его
                    min_w = matrix[elem][newVertex]
                    i = elem
                    j = newVertex
        # добавляем ребро если мы ещё не посещали концевую вершину
        weight.append(min_w)
        visited.append(j)
        mst[i][j] = min_w
        # затираем ребро в исходной матрице, чтоб снова его не взять
        matrix[i][j] = math.inf
    return mst, sum(weight)


def main():
    print(primFindMST(readMatrix("matrix.txt"), [0, 1, 2, 4, 5]))


if __name__ == "__main__":
    main()
