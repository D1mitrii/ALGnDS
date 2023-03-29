import sys
from binaryHeap import Heap

DEBUG = False


def heuristic(currentVertex, endVertex):
    """
    Эврестическая функция - близость символов,
    обозначающих вершины графа, в таблице ASCII.
    Считается следующим образом: разница кодов конечной вершины с текущей по модолю.
    :param currentVertex: текущая вершина
    :param endVertex: конечная вершина
    :return: возвращает значение эврестической функции
    """
    return abs(ord(endVertex) - ord(currentVertex))


def aStarAlgorithm(startVertex, endVertex, graph):
    """
    Функция реализует алгоритм A*. Создает словарь расстояний, и словарь корней.
    Создает очередь с приоритетом на куче.
    Пока куча не пустая, достаем вершину с минимальной ценной из очереди. Если это конечная прекращаем поиск,
    если эта вершина лист пропускаем рассмотрение этой вершины,
    иначе рассматриваем ребра смежные с этой вершиной, берем вершину куда ведет это ребро, считаем вес пути в данную вершину
    если такую вершину не рассматривали или вес получился более оптимальный  обновляем словари и добавляем в очередь эту вершину.
    :param startVertex: начальная вершина
    :param endVertex: конечная вершина
    :param graph: словарь ребер графа
    :return: словарь корней (ключ - куда пришли, значение - откуда)
    """
    global DEBUG
    distances = dict({startVertex: 0})
    roots = dict({startVertex: None})
    queue = Heap([(0, startVertex)])
    while queue.size() != 0:
        if DEBUG:
            print("Очередь на текущей итеариции имеет вид:")
            print(queue)
        current = queue.extract_min()[1]
        if current == endVertex:
            if DEBUG:
                print('Дошли до конечной вершины!')
            break
        if current not in graph:
            if DEBUG:
                print(f"Вершина |{current}| является листом графа")
            continue
        for nextVertex, weight in graph[current]:
            temp_dist = distances[current] + weight
            if nextVertex not in distances or temp_dist < distances[nextVertex]:
                roots[nextVertex] = current
                distances[nextVertex] = temp_dist
                queue.insert((temp_dist + heuristic(nextVertex, endVertex), nextVertex))
                if DEBUG:
                    print(f"Обновляется решение!")
                    print("\tСловарь посещенных вершин:")
                    print("\t", roots)
                    print("\tСловарь цен пути в вершины:")
                    print("\t", distances)
                    print("\tОчередь имеет вид:")
                    print(queue)
    return roots


def recoverPath(map, endVertex):
    """
    Функция востанавливает путь пройденный А*. Начинает востанавливать с конечной вершины по старт.
    :param map: словарь путей
    :param endVertex: конечная вершина
    :return: возвращает путь от стартовой вершины до конечной
    """
    path = ''
    current = endVertex
    while current:  # пока существует вершина из которой пришли
        path += current  # к пути добавляем текущую
        current = map[current]  # берем вершину откуда пришли в текущую
    return path[::-1]  # переворачиваем путь


def reader():
    """
    Функция считывает стартовую и конечную вершины. После чего считывает ребра из
    стандартного потока ввода, пока в него подают.
    Разбивает ввод и заносить в словарь ребер ребра.
    :return: кортеж из 3х элементов: стартовая вершина, конечная вершина, словарь ребер графа
    """
    start, end = input().split()
    edges = dict()

    for line in sys.stdin:
        if line == '\n':
            break
        source, destination, weight = line.split()
        if source not in edges.keys():
            edges[source] = list()
        edges[source].append((destination, float(weight)))
    return start, end, edges


if __name__ == "__main__":
    data = reader()  # считываем данные
    """
    Предаем данные в алгоритм A*,
    после чего востанавливаем путь проёденный алгоритмом,
    печатаем результат
    """
    print(recoverPath(aStarAlgorithm(*data), data[1]))
