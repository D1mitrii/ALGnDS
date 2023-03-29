import sys

DEBUG = True


def reader():
    """
    Функция считывает стартовую и конечную вершины. После чего считывает ребра из
    стандартного потока ввода, пока в него подают.
    Разбивает ввод и заносить в словарь ребер ребра.
    После чего происходит сортировка ребер, по их весу.
    :return: кортеж из 3х элементов: стартовая вершина, конечная вершина, словарь ребер графа
    """
    global DEBUG
    start, end = input().split()
    edges = dict()

    for line in sys.stdin:
        if line == '\n':
            break
        source, destination, weight = line.split()
        if source not in edges.keys():
            edges[source] = list()
        edges[source].append((destination, float(weight)))

    for key in edges.keys():
        edges[key].sort(key=lambda edge: edge[1])
    return start, end, edges


def greedyAlgorithm(startVertex, endVertex, edges):
    """
    Жадный поиск пути от стартовой вершины к конечной. Используется поиск в глубину.
    :param startVertex: стартовая вершина
    :param endVertex: конечная
    :param edges: словарь ребер
    :return: Возвращает путь от стартовой до конечной вершины.
    """
    result = ""  # В данной переменной после поиска в глубину будет храниться конечное решение.
    found = False  # Переменная 'флаг', необходима для приостановки поиска в глубину, когда решение было найдено.

    def modedDFS(path):
        """
        Модифицированный поиск в глубину.
        Смотрим текущую смежные ребра с текущей вершиной.
        Пока они есть удаляем из них минимальное и добавляем к текущему пути
        букву вершины куда ведет эторебро.
        :param path: путь на текущей интерации рекурсии
        :return: ничего не возвращает
        """
        nonlocal result, found, endVertex, edges
        global DEBUG
        if found:  # выход из рекурси если путь был найден
            return
        if path[-1] == endVertex:  # нашли путь от стартовой до конечной вершины
            result = path  # сохраняем его
            found = True  # поднимаем флаг, ибо нашли путь
            if DEBUG:
                print('\n')
                print("Путь был найден:")
                print(f"{result}")
            return
        if edges.get(path[-1]) is None and DEBUG:
            print('\n')
            print(f"Вершина |{path[-1]}| является листом графа")
        while edges.get(path[-1]) and edges[path[-1]] is not None:  # пока есть смежные ребра с текущей вершиной
            newEdge = edges[path[-1]].pop(0)  # берем минимальное из них
            if DEBUG and not found:
                print('\n')
                print(f"Берем ребро |{path[-1]}{newEdge[0]}| с весом |{newEdge[1]}|")
                print("Текущий путь:")
                print(path + newEdge[0])
            modedDFS(path + newEdge[0])  # запускаем поиск добавив к текущему пути вершину куда это ребро ведет.

    modedDFS(startVertex)  # вызываем поиск в глубину из стартовой вершины
    return result  # возвращаем найденный путь


def main():
    data = reader()  # Cчитываем данные
    print(greedyAlgorithm(*data))  # Передаем их алгоритму, после чего печатаем ответ.


if __name__ == "__main__":
    main()
