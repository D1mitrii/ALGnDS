import math
from copy import deepcopy
from readFuncs import readMatrix
from primFindMST import primFindMST
from minWeightEdges import minWeightEdges


class methodBB:

    def __init__(self, matrix, startVertex, DEBUG=False):
        # инициализация полей класса
        self.__matrix = matrix
        self.__startVertex = startVertex
        self.__recordPath = []
        self.__recordWeight = math.inf
        self.__DEBUG = DEBUG

    def __findMinCostEdge(self, vertex, remainVertices):
        """
        Метод находит минимальное ребро из последней вершины пути к оставшимся вершинам.
        :param vertex: последняя вершина пути
        :param remainVertices: вершины ещё не добавленные в путь
        :return: вес минимального ребра из
        """
        if len(remainVertices) == 0:
            return 0
        # инициализируем ребро как бесконечность
        minEdge = math.inf
        # проходимся по всем ребрам из вершины к оставшимся, если нашли меньше, то меняяем
        for elem in remainVertices:
            if self.__matrix[vertex][elem] < minEdge:
                minEdge = self.__matrix[vertex][elem]
        return minEdge

    def __solve(self, currentPath, currentWeight):
        """
        Рекурсивный метод перебирающий все возможные решение, используется МВиГ
        :param currentPath: текущий путь
        :param currentWeight: вес текущего пути
        :return: ничего не возвращает
        """
        if self.__DEBUG:
            print(f"Рассматривается путь: {'-'.join(self.__strVertexArray(currentPath))}, его вес {currentWeight}")
        # нашли путь по все вершинам
        if len(currentPath) == len(self.__matrix):
            # проверям, что он лучше рекорда
            if currentWeight + self.__matrix[currentPath[-1]][self.__startVertex] < self.__recordWeight:
                # если лучше обновляем рекорд
                if self.__DEBUG:
                    print(
                        f"OLD оптимальное решиение: cost:{self.__recordWeight}\npath:{'-'.join(self.__strVertexArray(self.__recordPath))}")
                self.__recordWeight = currentWeight + self.__matrix[currentPath[-1]][self.__startVertex]
                self.__recordPath = currentPath + [self.__startVertex]
                if self.__DEBUG:
                    print(
                        f"NEW оптимальное решиение: cost:{self.__recordWeight}\npath:{'-'.join(self.__strVertexArray(self.__recordPath))}")
            else:
                # если хуже то возращаемся
                if self.__DEBUG:
                    print(
                        f"Нашли цепочку c ценой({currentWeight + self.__matrix[currentPath[-1]][self.__startVertex]}) > рекорда({self.__recordWeight}):"
                        f"\n{'-'.join(self.__strVertexArray(currentPath + [self.__startVertex]))} - она не оптимальная!")
                return
        # достаем последнюю вершину пути
        lastVertex = currentPath[-1]
        # создаем список ещё не просмотренных вершин
        notViewed = [i for i in range(len(self.__matrix)) if i not in currentPath]
        # отсечение ветвей хуже текущего рекорда
        minWeightEstimation = minWeightEdges(deepcopy(self.__matrix), [lastVertex] + notViewed.copy())
        MSTEstimation = primFindMST(deepcopy(self.__matrix), notViewed.copy())[1] + self.__findMinCostEdge(currentPath[-1], notViewed)
        if self.__DEBUG:
            print("Оценки оставшегося пути:")
            print(f"\tПо полусумме двух легчайших ребер: {minWeightEstimation}")
            print(f"\tПо весу МОД: {MSTEstimation}")
        if currentWeight + max(minWeightEstimation, MSTEstimation) > self.__recordWeight:
            if self.__DEBUG:
                print(f"Рекорд ({self.__recordWeight}) отсек путь с весом + оценкой"
                      f"({currentWeight + max(minWeightEstimation, MSTEstimation)}):")
                print(f"Отсеченный путь {'-'.join(self.__strVertexArray(currentPath))}")
            return
        if self.__DEBUG:
            print(f"Ещё не рассмотренные вершины: {self.__strVertexArray(notViewed)}")
        for vertex in notViewed:
            # поочередно добавляем вершины в путь, если в них он есть из последней вершины текущего пути
            if self.__matrix[lastVertex][vertex] != math.inf:
                # добавляем вершину
                currentPath.append(vertex)
                if self.__DEBUG:
                    print(
                        f"Добавляем к пути вершину ({vertex + 1}) путь: {'-'.join(self.__strVertexArray(currentPath))}")
                self.__solve(currentPath, currentWeight + self.__matrix[lastVertex][vertex])
                if self.__DEBUG:
                    print(f"Удаляем последнию вершину из пути: {'-'.join(self.__strVertexArray(currentPath))}")
                currentPath.pop()
            else:
                return

    @staticmethod
    def __strVertexArray(array):
        """
        Выполянет преобразование элементов массива в массив из строк
        :param array: массив для преобразования
        :return: массив, где каждый элемент строка
        """
        return [str(vertex + 1) for vertex in array]

    def __call__(self):
        """
        Функция находит нижнюю границу, после чего запускает МВиГ
        :return:возвращает полученный путь и его вес
        """
        # запускаем МВиГ
        self.__solve([self.__startVertex], 0)
        return self.__recordPath, self.__recordWeight


def main():
    filename = input("Введите название файла матрицы: ")
    startVerext = int(input("Введите стартовую вершину (нумерация начинается с 1): ")) - 1
    matrix = readMatrix(filename)
    MBBsolver = methodBB(matrix, startVerext, True)
    path, weight = MBBsolver()
    print("Цепочка:")
    print("-".join([str(elem + 1) for elem in path]))
    print("Стоимость её прохождения:")
    print(weight)


if __name__ == '__main__':
    main()
