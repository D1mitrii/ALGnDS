from copy import deepcopy

DEBUG = False

boardSize = 0
minColor = 0
minBoard = []
minSquares = []
operationCounter = 0


def printBoard(board):
    """
    Функция отвечает за вывод дву мерного массива, соответствуещего столешницу.
    :param board:
    :return: Ничего
    """
    for row in board:
        print(*row)


def placeSquare(board, xStart, yStart, width, color, squares):
    """
    Функция отвевает за установку квадрата на столещницу.
    Функция добавляет квадрат в частичное решение.
    :param board: двумерный массив
    :param xStart: Абсцисса левого верхнего угла квадрата для вставки
    :param yStart: Ордината левого верхнего угла квадрата для вставки
    :param width: Сторона вставляемого квадрата
    :param color: Цвет квадрата
    :param squares: Массив частичных решений, содержащий квадраты решения
    :return: Ничего
    """
    global operationCounter, DEBUG
    operationCounter += 1
    for x in range(xStart, xStart + width):
        for y in range(yStart, yStart + width):
            board[y][x] = color
    if DEBUG:
        print(f"Квадрат со стороной {width} ставят, координаты его левого угла ({xStart}:{yStart})")
        printBoard(board)
    squares.append([xStart, yStart, width])


def sliceSquare(board, xStart, yStart, width, squares):
    """
    Функция отвечает за срез нижней стороны и правой в 1 клетку.
    Функция также уменьшает сторону последнего квадрата в частичном решении на единицу.
    :param board: двумерный массив.
    :param xStart: Абсцисса левого верхнего угла квадрата для среза.
    :param yStart: Ордината левого верхнего угла квадрата для среза.
    :param width: Сторона квадрата для среза.
    :param squares: Массив частичных решений, содержащий квадраты решения.
    :return: Ничего
    """
    global DEBUG
    for y in range(yStart, yStart + width):
        board[y][xStart + width - 1] = 0
    for x in range(xStart, xStart + width - 1):
        board[yStart + width - 1][x] = 0
    if DEBUG:
        print(f"Квадрат со стороной {width} уменьшают, координаты его левого угла ({xStart}:{yStart})")
        printBoard(board)
    squares[-1][2] -= 1
    if squares[-1][2] == 0:
        squares.pop()


def backTracking(board, xStart, yStart, color, squares):
    """
    Функция бэктрэкинга. Находим максимальный размер квадрата который можем вставить и вставляем его.
    Затем в цикле постепенно перебираем от найденого размера до квадрата в одну клетку и ищем новую координату для вставки.
    Если такая есть, то для полученной координаты запускается эта же функция,
    таким образом развивается это частичное решение. Если вставить нельзя,
    то проверяем количество цветов в раскраске частичного решения если оно меньше минимальной раскраски,
    то сохраняем решение и заменяем минимальную раскраску. В конце цикла уменьшаем первый квадрат,
    который мы вставили.
    :param board: Двумерный массив.
    :param xStart: Абсцисса ещё не занятой области на столешницу.
    :param yStart: Ордината ещё не занятой области на столешницу.
    :param color: Текущий цвет
    :param squares: Массив частичных решений.
    :return: Ничего
    """
    global minColor, minBoard, minSquares
    # Поиск максимального размера квадрата для вставки
    maxSide = min(boardSize - yStart, boardSize - xStart)
    for x in range(xStart + 1, xStart + maxSide):
        if board[yStart][x]:
            maxSide = x - xStart
            break
    # Устанавливаем квадрат с найденным размером
    placeSquare(board, xStart, yStart, maxSide, color, squares)
    # Постепенно пребираем квадраты с меньшей стороной
    for n in range(maxSide, 0, -1):
        # Поиск новой координаты для вставки, ищем ещё не занятое место
        flagFound = False
        for y in range(yStart, boardSize):
            if flagFound:
                y -= 1
                break
            for x in range(boardSize // 2, boardSize):
                if board[y][x] == 0:
                    flagFound = True
                    break
        # Если нашли снова запускаем бэктрэкинг, но уже с новой координатой и увеличеным на единицу цветом
        if flagFound:
            if color + 1 != minColor:
                backTracking(board, x, y, color + 1, squares)
        else:
            # Найдено решение, если оно имеет раскраску меньше текущей минимальной,
            # то сохраняем решение в глобальные переменные
            if color < minColor:
                minColor = color
                minBoard = deepcopy(board)
                minSquares = deepcopy(squares)
        # Уменьшаем вставленный квадрат, чтобы проверить остальные варианты расстановки
        sliceSquare(board, xStart, yStart, n, squares)


if __name__ == "__main__":
    # Точка входа в программу.

    boardSize = int(input())  # Считывает входные данные.
    # Находит маштаб, если можно маштабировать задачу.
    factor = 1
    for i in range(2, boardSize + 1):
        if boardSize % i == 0:
            factor = boardSize // i
            boardSize = i
            break
    # Заводим первоначальный размер
    minColor = boardSize * boardSize + 1
    # Создаем двумерный массив столещницы в заданом маштабе
    board = [[0 for _ in range(boardSize)] for _ in range(boardSize)]
    # Находим сторону максимального квадрата
    bigSquare = (boardSize + 1) // 2
    # Находим сторону двух смежных квадратов
    remainingSquare = boardSize // 2
    # Создаем массив квадратов частичного решения
    squares = []
    placeSquare(board, 0, 0, bigSquare, 1, squares)  # Устанавливаем максимальный квадрат
    # Устанавливаем два квадрата смежных с максимальным
    placeSquare(board, bigSquare, 0, remainingSquare, 2, squares)
    placeSquare(board, 0, bigSquare, remainingSquare, 3, squares)
    # Запускаем рекурсивный бэктрэкинг
    backTracking(board, remainingSquare + (boardSize % 2), remainingSquare, 4, squares)
    # Вывод дополнительной информации
    if DEBUG:
        print(f"Количество операций: {operationCounter}")
        print("Столещница с минимальным количество квадратов:")
        printBoard(minBoard)
        print("Основной ответ на поставленную задачу:")
    # Вывод результата работы программы
    print(minColor)
    for square in minSquares:
        print(square[0] * factor + 1, square[1] * factor + 1, square[2] * factor)
