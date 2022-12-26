import random
import time
import gc
import matplotlib.pyplot as plt

from Smirnov_Dmitry_cw.src.module.RBTree import RBTree


class RBTreeGraphics:
    @staticmethod
    def best_case():
        times_insert = list()
        times_get = list()
        times_remove = list()

        MAX = 1000000
        #dataset = list(range(1, MAX))
        dataset = [500000, ] * MAX
        for i in range(499999):
            current = dataset[i]
            dataset[i * 2 + 1] = current // 2
            dataset[i * 2 + 2] = current + current // 2
        tree = RBTree()
        gc.disable()
        start = time.time_ns()
        for i in dataset:
            tree[i] = i
            times_insert.append(time.time_ns() - start)
        gc.enable()
        gc.disable()
        start = time.time_ns()
        for i in dataset:
            a = tree[i]
            times_get.append(time.time_ns() - start)
        gc.enable()
        gc.disable()
        dataset.reverse()
        for_remove = set(dataset)
        start = time.time_ns()
        for i in for_remove:
            tree.remove(i)
            times_remove.append(time.time_ns() - start)
        gc.enable()
        fig, ax = plt.subplots()
        ax.scatter(list(range(1, len(times_insert)+1)), times_insert, color=['red'], s=0.5, label="Operation: insert")
        ax.scatter(list(range(1, len(times_get)+1)), times_get, color=['green'], s=0.5, label="Operation: find")
        ax.scatter(list(range(1, len(times_remove)+1)), times_remove, color=['blue'], s=0.5, label="Operation: remove")
        plt.legend(loc="best")
        plt.title(f"RB-Tree best case all operations")
        ax.set_xlabel("Elements count")
        ax.set_ylabel("Time, ns")
        plt.show()

    @staticmethod
    def worst_case():
        times_insert = list()
        times_get = list()
        times_remove = list()

        MAX = 1_000_000
        dataset = list(range(1, MAX))
        tree = RBTree()
        gc.disable()
        start = time.time_ns()
        for i in dataset:
            tree[i] = i
            times_insert.append(time.time_ns() - start)
        gc.enable()
        random.shuffle(dataset)
        gc.disable()
        start = time.time_ns()
        for i in dataset:
            a = tree[i]
            times_get.append(time.time_ns() - start)
        gc.enable()
        gc.disable()
        start = time.time_ns()
        for i in dataset:
            tree.remove(i)
            times_remove.append(time.time_ns() - start)
        gc.enable()
        fig, ax = plt.subplots()

        ax.scatter(list(range(1, MAX)), times_insert, color=['red'], s=0.5, label="Operation: insert")
        ax.scatter(list(range(1, MAX)), times_get, color=['green'], s=0.5, label="Operation: find")
        ax.scatter(list(range(1, MAX)), times_remove, color=['blue'], s=0.5, label="Operation: remove")
        plt.legend(loc="best")
        plt.title(f"RB-Tree worst case all operations")
        ax.set_xlabel("Elements count")
        ax.set_ylabel("Time, ns")
        plt.show()

    @staticmethod
    def average_case():
        times_insert = list()
        times_get = list()
        times_remove = list()
        MAX = 1_000_000
        dataset = list(random.randint(1, MAX) for _ in range(1, MAX))
        random.shuffle(dataset)
        tree = RBTree()

        gc.disable()
        start = time.time_ns()
        for i in dataset:
            tree[i] = i
            times_insert.append(time.time_ns() - start)
        gc.enable()

        gc.disable()
        start = time.time_ns()
        for i in dataset:
            a = tree[i]
            times_get.append(time.time_ns() - start)
        gc.enable()

        gc.disable()
        start = time.time_ns()
        for i in dataset:
            tree.remove(i)
            times_remove.append(time.time_ns() - start)
        gc.enable()
        tree.print()

        fig, ax = plt.subplots()

        ax.scatter(list(range(1, MAX)), times_insert, color=['red'], s=0.5, label="Operation: insert")
        ax.scatter(list(range(1, MAX)), times_get, color=['green'], s=0.5, label="Operation: find")
        ax.scatter(list(range(1, MAX)), times_remove, color=['blue'], s=0.5, label="Operation: remove")
        plt.legend(loc="best")
        plt.title(f"RB-Tree average case all operations")
        ax.set_xlabel("Elements count")
        ax.set_ylabel("Time, ns")
        plt.show()


#RBTreeGraphics.best_case()
RBTreeGraphics.worst_case()
#RBTreeGraphics.average_case()
#data_array = list(500000, 250000, 750000, 125000, 375000, 625000, 875000)
