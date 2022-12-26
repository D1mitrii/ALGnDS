import gc
import random
import time

from matplotlib import pyplot as plt

from Smirnov_Dmitry_cw.src.module.Hashtable import Hashtable
from Smirnov_Dmitry_cw.src.module.RBTree import RBTree


class CompareGraphic:
    def __init__(self):
        pass

    @staticmethod
    def insert_case():
        rb_tree = list()
        hashtable = list()

        MAX = 1_000_000
        dataset = list(random.randint(1, MAX) for _ in range(1, MAX))
        random.shuffle(dataset)

        tree = RBTree()
        table = Hashtable("linear")

        gc.disable()
        start = time.time_ns()
        for i in dataset:
            tree[i] = i
            rb_tree.append(time.time_ns() - start)
        gc.enable()

        gc.disable()
        start = time.time_ns()
        for i in dataset:
            table[i] = i
            hashtable.append(time.time_ns() - start)
        gc.enable()

        fig, ax = plt.subplots()

        ax.scatter(list(range(1, MAX)), rb_tree, color=['red'], s=0.5, label="RBTree: insert")
        ax.scatter(list(range(1, MAX)), hashtable, color=['green'], s=0.5, label="Hashtable: insert")
        plt.legend(loc="best")
        plt.title(f"RB-Tree vs Hashtable(linear): operation - insert")
        ax.set_xlabel("Elements count")
        ax.set_ylabel("Time, ns")
        plt.show()

    @staticmethod
    def find_case():
        rb_tree = list()
        hashtable = list()

        MAX = 1_000_000
        dataset = list(random.randint(1, MAX) for _ in range(1, MAX))
        random.shuffle(dataset)

        tree = RBTree()
        table = Hashtable("linear")

        for i in dataset:
            tree[i] = i
            table[i] = i

        gc.disable()
        start = time.time_ns()
        for i in dataset:
            a = tree[i]
            rb_tree.append(time.time_ns() - start)
        gc.enable()

        gc.disable()
        start = time.time_ns()
        for i in dataset:
            a = table[i]
            hashtable.append(time.time_ns() - start)
        gc.enable()

        fig, ax = plt.subplots()

        ax.scatter(list(range(1, MAX)), rb_tree, color=['red'], s=0.5, label="RBTree: find")
        ax.scatter(list(range(1, MAX)), hashtable, color=['green'], s=0.5, label="Hashtable: find")
        plt.legend(loc="best")
        plt.title(f"RB-Tree vs Hashtable(linear): operation - find")
        ax.set_xlabel("Elements count")
        ax.set_ylabel("Time, ns")
        plt.show()

    @staticmethod
    def remove_case():
        rb_tree = list()
        hashtable = list()

        MAX = 1_000_000
        dataset = list(random.randint(1, MAX) for _ in range(1, MAX))
        random.shuffle(dataset)

        tree = RBTree()
        table = Hashtable("linear")

        for i in dataset:
            tree[i] = i
            table[i] = i
        random.shuffle(dataset)
        gc.disable()
        start = time.time_ns()
        for i in dataset:
            tree.remove(i)
            rb_tree.append(time.time_ns() - start)
        gc.enable()

        gc.disable()
        start = time.time_ns()
        for i in dataset:
            table.remove(i)
            hashtable.append(time.time_ns() - start)
        gc.enable()

        fig, ax = plt.subplots()

        ax.scatter(list(range(1, MAX)), rb_tree, color=['red'], s=0.5, label="RBTree: remove")
        ax.scatter(list(range(1, MAX)), hashtable, color=['green'], s=0.5, label="Hashtable: remove")
        plt.legend(loc="best")
        plt.title(f"RB-Tree vs Hashtable(linear): operation - remove")
        ax.set_xlabel("Elements count")
        ax.set_ylabel("Time, ns")
        plt.show()


# CompareGraphic.insert_case()
# CompareGraphic.find_case()
CompareGraphic.remove_case()
