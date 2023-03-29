class Heap:
    def __init__(self, arr=None):
        "Инициализация объектс класса"
        if arr is None:
            arr = []
        self.__heap = []
        for el in arr:
            self.insert(el)

    @staticmethod
    def getParent(index):
        "Получение индекса родителя текущей вершины"
        return (index - 1) // 2

    @staticmethod
    def getLeft(index):
        "Получение индекса левого ребенка"
        return 2 * index + 1

    @staticmethod
    def getRight(index):
        "Получение индекса правого ребенка"
        return 2 * index + 2

    def __siftUp(self, index):
        """
        Просеивает вверх узел
        :param index: индекс вершины которую хотят просеить вверх
        :return: ничего возвращает
        """
        if index < 0 or index >= len(self.__heap):
            return
        parent = self.getParent(index)
        while index and not self.__heap[parent] < self.__heap[index]:
            self.__heap[parent], self.__heap[index] = self.__heap[index], self.__heap[parent]
            index, parent = parent, self.getParent(index)

    def __siftDown(self, index):
        """
        Просеивает вниз узел
        :param index: индекс вершины которую хотят просеить вниз
        :return: ничего возвращает
        """
        if index < 0 or index >= len(self.__heap):
            return
        minIndex = index
        while True:
            left, right = self.getLeft(index), self.getRight(index)
            if right < len(self.__heap) and self.__heap[right] < self.__heap[minIndex]:
                minIndex = right
            if left < len(self.__heap) and self.__heap[left] < self.__heap[minIndex]:
                minIndex = left
            if minIndex == index:
                return
            else:
                self.__heap[index], self.__heap[minIndex] = self.__heap[minIndex], self.__heap[index]
                index = minIndex

    def extract_min(self):
        """
        Достает минимальеый ставит максимальный на его место и просеивает вниз.
        :return: возвращает минимальный элемент
        """
        if not self.__heap:
            return
        min_element = self.__heap[0]
        self.__heap[0] = self.__heap[-1]
        del self.__heap[-1]
        self.__siftDown(0)
        return min_element

    def insert(self, element):
        """
        Добавляет элемент ставит в конец и просеивает вверх его.
        :return: ничего возвращает
        """
        self.__heap.append(element)
        self.__siftUp(len(self.__heap) - 1)

    def size(self):
        """
        :return: возвращает размер кучи
        """
        return len(self.__heap)

    def __repr__(self):
        representation = ""
        for item in self.__heap:
            representation += '\t' + str(item) + "\n"
        return representation
