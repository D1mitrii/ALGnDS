import math

DEBUG = False


class Node:
    def __init__(self, preffix='root'):
        self.preffix = preffix
        self.moves = {}
        self.suffixLink = None
        self.terminalFlag = False
        self.patternsID = []

    def setTerminal(self, patternID):
        global DEBUG
        if patternID not in self.patternsID:
            self.patternsID += [patternID]
        if DEBUG:
            print(f"STATE[{self.preffix}] has become terminal")
        self.terminalFlag = True


def buildTrie(patterns):
    global DEBUG
    if DEBUG:
        print("\n\nBUILDING A TRIE")
    root = Node()
    for i, pattern in enumerate(patterns):
        if DEBUG:
            print("Go from the ROOT")
            print(f"Now add pattern[{pattern}] to trie")
        node = root
        for indx, sym in enumerate(pattern):
            if DEBUG:
                if sym in node.moves:
                    print(f"Go to node {node.moves[sym].preffix}")
                else:
                    print(f"Add new node {pattern[:indx + 1]} to node {pattern[:indx]}")
            node = node.moves.setdefault(sym, Node(pattern[:indx + 1]))
        node.setTerminal(i)
    return root


def setSuffixLinks(root):
    global DEBUG
    if DEBUG:
        print("\n\nInstall suffix links in the trie")
    queue = []
    for vertex in root.moves.values():
        if DEBUG:
            print(f"Add suffix link to ROOT from {vertex.preffix}")
        vertex.suffixLink = root
        queue.append(vertex)

    while queue:
        vertex = queue.pop(0)

        for char, childVertex in vertex.moves.items():

            queue.append(childVertex)
            linkedNode = vertex.suffixLink
            # Climbing the suffix link
            while linkedNode is not None and char not in linkedNode.moves:
                linkedNode = linkedNode.suffixLink

            # If find add suffixLink, else add suffixlink to root
            if linkedNode:
                childVertex.suffixLink = linkedNode.moves[char]
            else:
                childVertex.suffixLink = root
            if DEBUG:
                print(f"Add suffix link FROM:{childVertex.preffix} TO: {childVertex.suffixLink.preffix}")
            # Transferring all patterns from the suffix link
            childVertex.patternsID += childVertex.suffixLink.patternsID

    return root


def algorithmAho(text, patterns):
    """
    The function is performed by the Aho-Korasik algorithm
    :param text:
    :param patterns: array of pattern,
    :return:
    """
    global DEBUG
    root = setSuffixLinks(buildTrie(patterns))
    if DEBUG:
        treeDFS(root)
        findMaxEdges(root)
        print("\n\nAho-Corasick algorithm STARTED!")
    node = root
    res = []
    for i in range(len(text)):
        if DEBUG:
            print(f"CURRENT POSITION IN TEXT {i + 1} | CHAR IN TEXT: {text[i]}")
            print(f"CURRENT STATE: [{node.preffix}]")
        while node and text[i] not in node.moves:
            if DEBUG:
                print(f"From state[{node.preffix}] noway to state[{node.preffix}->{text[i]}]")
                print(f"Go to suffixLink state[{node.suffixLink.preffix if node.suffixLink else ''}]")
            node = node.suffixLink
        if not node:
            if DEBUG:
                print("Didn't find the path to sym returned to the ROOT")
            node = root
            continue
        node = node.moves[text[i]]
        for pattern in node.patternsID:
            if DEBUG:
                print(
                    f"State[{node.preffix}] find {patterns[pattern]} with id {pattern} at position {i - len(patterns[pattern]) + 1}")
            res.append((i - len(patterns[pattern]) + 1, pattern))
    return res


def findMaxEdges(root):
    """
    Func find all node witch have max edges
    :param root: root of trie
    :return: nothing
    """
    maxEdges = -math.inf
    nodes = []
    queue = [root]
    # using DFS find nodes
    while queue:
        currentNode = queue.pop(0)
        if len(currentNode.moves.values()) > maxEdges:
            # if max > current refresh list of nodes
            nodes.clear()
            nodes.append(currentNode)
            maxEdges = len(currentNode.moves.values())
        elif len(currentNode.moves.values()) == maxEdges:
            # find another node with max edges
            nodes.append(currentNode)
        for child in currentNode.moves.values():
            # add children in queue
            queue.append(child)
    print(f"The max number of edges ({maxEdges}) comes out of {[node.preffix for node in nodes]}")


def treeDFS(root):
    """
    Print automaton
    :param root: root node of Trie
    :return: nothing
    """
    print("\n\nTHE AUTOMATON")
    visited = []
    queue = [root]
    while queue:
        currentNode = queue.pop(0)
        if currentNode not in visited:
            addSpacing = "\t" * len(currentNode.preffix) if currentNode.preffix != "root" else ""
            print(
                f"{addSpacing}NODE[{currentNode.preffix}] - TERMINAL?[{currentNode.terminalFlag}] - SUFFIXLINK TO [{currentNode.suffixLink.preffix if currentNode.suffixLink else ''}]")
            visited += [currentNode]
            for child in currentNode.moves.values():
                queue = [child] + queue


def createSubsAndStarts(pattern, joker):
    """
    func spilt pattern by joker, and find for each sub start index in pattern
    :param pattern: pattern with jockers
    :param joker: wildcard
    :return: subs, array of tuples with
    """
    global DEBUG
    patterns = list(filter(None, pattern.split(joker)))
    if DEBUG:
        print(f"Split the pattern into substrings by the joker symbol [{joker}]")
        print(f"After splitting {patterns}")
    starts = []
    if pattern[0] != joker:
        starts.append(0)
    for i in range(1, len(pattern)):
        if pattern[i - 1] == joker and pattern[i] != joker:
            starts.append(i)
    if DEBUG:
        print(f"Array of tuples of subs and their start index in the pattern")
        print(list(zip(patterns, starts)))
    return patterns, list(zip(patterns, starts))


def solve(text, pattern, joker):
    """
    func make prework computation, after start aho-korasik alg
    :param text: source text
    :param pattern: pattern with masks
    :param joker: wildcard
    :return: return array of index occurrence pattern in text
    """
    global DEBUG
    patterns, tupleInfo = createSubsAndStarts(pattern, joker)
    occurrences = algorithmAho(text, patterns)
    arrayC = len(text) * [0]
    for occurrence in occurrences:
        j = occurrence[0] - tupleInfo[occurrence[1]][1]
        if j >= 0:
            if DEBUG:
                print(f"For pattern occurence {tupleInfo[occurrence[1]][0]} with startIndex {tupleInfo[occurrence[1]][1]} update arrayC[{j}]+=1")
            arrayC[j] += 1
    answer = []
    if DEBUG:
        print("Array C:")
        print(arrayC)
    for i in range(len(text) - len(pattern) + 1):
        if arrayC[i] == len(patterns):
            answer.append(i + 1)
    return answer


if __name__ == "__main__":
    text = input()
    pattern = input()
    joker = input()
    result = solve(text, pattern, joker)
    print(*result, sep='\n')
    if DEBUG:
        patternLen = len(pattern)
        for i in result:
            text = text[:i - 1] + " " * patternLen + text[i - 1 + patternLen:]
        print("Having cut out all the patterns from the text left:", text.replace(' ', ''), sep='\n')
