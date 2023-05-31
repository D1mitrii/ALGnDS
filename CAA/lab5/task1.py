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
    """
    Func build trie by patterns
    :param patterns: array of patterns
    :return: root node of trie
    """
    global DEBUG
    if DEBUG:
        print("\n\nBUILDING A TRIE")
    root = Node()
    for i, pattern in enumerate(patterns):
        if DEBUG:
            print("Go from the ROOT")
            print(f"Now add pattern[{pattern}] to trie")
        node = root
        # for each pattern go sym
        for indx, sym in enumerate(pattern):
            # add node to trie if not already exist in trie
            if DEBUG:
                if sym in node.moves:
                    print(f"Go to node {node.moves[sym].preffix}")
                else:
                    print(f"Add new node {pattern[:indx + 1]} to node {pattern[:indx]}")
            node = node.moves.setdefault(sym, Node(pattern[:indx + 1]))
        node.setTerminal(i)
    return root


def setSuffixLinks(root):
    """
    Make from trie to automaton
    :param root: root of trie
    :return: return root of automaton
    """
    global DEBUG
    if DEBUG:
        print("\n\nInstall suffix links in the trie")
    queue = []
    # add suffixLink to root from root childrens
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


if __name__ == "__main__":
    text = input()
    patterns = [input() for _ in range(int(input()))]

    result = sorted(algorithmAho(text, patterns))
    print("\n".join([f"{ind + 1} {pattern + 1}" for ind, pattern in result]))
    if DEBUG:
        for ind, pattern in result:
            patternLen = len(patterns[pattern])
            text = text[:ind] + " " * patternLen + text[ind + patternLen:]
        print("Having cut out all the patterns from the text left:", text.replace(' ', ''), sep='\n')
