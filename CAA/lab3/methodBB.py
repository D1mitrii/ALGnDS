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
                        f"СТАРОЕ оптимальное решиение: cost:{self.__recordWeight}\npath:{'-'.join(self.__strVertexArray(self.__recordPath))}")
                self.__recordWeight = currentWeight + self.__matrix[currentPath[-1]][self.__startVertex]
                self.__recordPath = currentPath + [self.__startVertex]
                if self.__DEBUG:
                    print(
                        f"НОВОЕ оптимальное решиение: cost:{self.__recordWeight}\npath:{'-'.join(self.__strVertexArray(self.__recordPath))}")
            else:
                # если хуже то возращаемся
                if self.__DEBUG:
                    print(
                        f"Нашли цепочку c ценой({currentWeight + self.__matrix[currentPath[-1]][self.__startVertex]}):"
                        f"\n{'-'.join(self.__strVertexArray(currentPath + [self.__startVertex]))} - она не оптимальная!")
                return
        # отсечение ветвей хуже нижней оценки
        if currentWeight > self.__estimation:
            if self.__DEBUG:
                print(f"Нижняя оценка ({self.__estimation}) отсекла путь с весом ({currentWeight}):")
                print(f"Отсеченный путь {'-'.join(self.__strVertexArray(currentPath))}")
            return
        # достаем последнюю вершину пути
        lastVertex = currentPath[-1]
        # создаем список ещё не просмотренных вершин
        notViewed = [i for i in range(len(self.__matrix)) if i not in currentPath]
        if self.__DEBUG:
            print(f"Ещё не рассмотренные вершины: {[str(vertex + 1) for vertex in notViewed]}")
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
        try:
            # пытаем получить нижнюю границу
            self.__estimation = primFindMST(deepcopy(self.__matrix), self.__startVertex)[1] + minWeightEdges(
                deepcopy(self.__matrix))
        except RuntimeError as e:
            print(e)
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
