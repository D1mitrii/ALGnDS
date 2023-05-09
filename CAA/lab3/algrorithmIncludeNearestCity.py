import math
from readFuncs import readMatrix


class AlgorithmIncludeNearestCity:
    def __init__(self, matrix, startVertex, DEBUG=False):
        # инициализация полей класса
        self.__matrix = matrix
        self.__startVertex = startVertex
        self.__DEBUG = DEBUG
        self.__path = [self.__startVertex]

    def __nextCity(self):
        """
        Функция ищет минимальное ребро в ещё не добавленные город
        :return: ничего не возвразает
        """
        # создаем список ещё не пройденных городов
        notIncluded = [i for i in range(len(self.__matrix)) if i not in self.__path]
        # заводим начальные значения
        minWeight = math.inf
        indexFrom = 0
        indexTo = 0

        if self.__DEBUG:
            print(f"Путь имеет вид: {'-'.join(self.__strVertexArray(self.__path))}")
            print(f"Уже выбранные вершины: {self.__strVertexArray(self.__path)}")
            print(f"Ещё не добавленные вершины: {self.__strVertexArray(notIncluded)}")
        # рассматрицаем дуги из уже просмотренных вершин в ещё не просмотренные
        for vertex in self.__path:
            for nextVertex in notIncluded:
                if self.__DEBUG:
                    print(
                        f"Рассматриваем дугу: {vertex + 1}->{nextVertex + 1} с весом {self.__matrix[vertex][nextVertex]}")
                if self.__matrix[vertex][nextVertex] <= minWeight:
                    # если нашли ребро с меньшим весов, чем текущее
                    # то обнавляем значения
                    indexFrom = vertex
                    indexTo = nextVertex
                    minWeight = self.__matrix[vertex][nextVertex]
        if minWeight != math.inf:
            # добавляем к решение, если ребро в графе есть
            if self.__DEBUG:
                print("Нашли дугу с минимальным весом")
                print(f"FROM:{indexFrom + 1}  TO:{indexTo + 1} MINWEIGHT:{minWeight}")
                print("Добавляем её в путь\n")
            self.__path.insert(self.__path.index(indexFrom) + 1, indexTo)
        else:
            # если нет, то граф состоит из нескольких не связаных частей
            raise RuntimeError("Граф не целый")

    @staticmethod
    def __strVertexArray(array):
        """
        Выполянет преобразование элементов массива в массив из строк
        :param array: массив для преобразования
        :return: массив, где каждый элемент строка
        """
        return [str(vertex + 1) for vertex in array]

    def __findPathCost(self):
        """
        Функция находит стоимость пути
        :return: возвращает стоимость
        """
        cost = 0
        for i in range(1, len(self.__path)):
            # увеличивем переменную суммы на значения ребра в пути
            cost += self.__matrix[self.__path[i - 1]][self.__path[i]]
        return cost

    def __solve(self):
        """
        Функция отвечает за алгоритм АВБГ
        :return: ничего не возвращает
        """
        # пока не добавили все вершины
        while len(self.__path) < len(self.__matrix):
            # пытаемся добавить минимальное ребро
            try:
                self.__nextCity()
            except RuntimeError as e:
                print(e)
                break
        # нашли путь по всем вершниам, теперь проверяем, что можно зациклить
        if self.__matrix[self.__path[-1]][self.__startVertex] != math.inf:
            if self.__DEBUG:
                print(f"Образуем цикл добавлением дуги {self.__path[-1] + 1}->{self.__startVertex + 1}")
            self.__path.append(self.__startVertex)
        else:
            raise RuntimeError("Нельзя построить цепочку")

    def __call__(self):
        """
        Функция запускает АВБГ
        :return:возвращает полученный путь и его вес
        """
        # вызываем метод решения
        self.__solve()
        # возврщаем полученные значения
        return self.__path, self.__findPathCost()


def main():
    filename = input("Введите название файла матрицы: ")
    startVertex = int(input("Введите стартовую вершину (нумерация начинается с 1): ")) - 1
    matrix = readMatrix(filename)
    alg = AlgorithmIncludeNearestCity(matrix, startVertex, True)
    path, cost = alg()
    print("Цепочка:")
    print("-".join([str(elem + 1) for elem in path]))
    print("Стоимость её прохождения:")
    print(cost)


if __name__ == '__main__':
    main()
