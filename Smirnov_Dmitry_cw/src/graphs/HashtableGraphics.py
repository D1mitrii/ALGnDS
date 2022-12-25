import random
import time
import gc
import matplotlib.pyplot as plt

from Smirnov_Dmitry_cw.src.module.Hashtable import Hashtable

PROBENAME = "double"


class HashtableGraphics:
    @staticmethod
    def best_case():
        times_insert = list()
        times_get = list()
        times_remove = list()

        MAX = 1_000_000
        dataset = list(range(1, MAX))

        table = Hashtable(PROBENAME)
        gc.disable()
        start = time.time_ns()
        for i in dataset:
            table[i] = i
            times_insert.append(time.time_ns() - start)
        gc.enable()
        gc.disable()
        start = time.time_ns()
        for i in dataset:
            a = table[i]
            times_get.append(time.time_ns() - start)
        gc.enable()
        gc.disable()
        start = time.time_ns()
        for i in range(1000000-1, 0, -1):
            table.remove(i)
            times_remove.append(time.time_ns() - start)
        gc.enable()
        fig, ax = plt.subplots()

        ax.scatter(list(range(1, MAX)), times_insert, color=['red'], s=0.5, label="Operation: insert")
        ax.scatter(list(range(1, MAX)), times_get, color=['green'], s=0.5, label="Operation: find")
        ax.scatter(list(range(1, MAX)), times_remove, color=['blue'],  s=0.5, label="Operation: remove")
        plt.legend(loc="best")
        plt.title(f"Hashtable({PROBENAME}) best all operations")
        ax.set_xlabel("Elements count")
        ax.set_ylabel("Time, ns")
        plt.show()

    @staticmethod
    def worst_case():
        times_insert = list()
        times_get = list()
        times_remove = list()

        table = Hashtable(PROBENAME)

        gc.disable()
        start = time.time()
        for i in range(1, 10000):
            table[i] = i
            times_insert.append(time.time() - start)
        gc.enable()
        gc.disable()
        start = time.time()
        for i in range(1, 10000):
            a = table[i]
            times_get.append(time.time() - start)
        gc.enable()
        gc.disable()
        start = time.time()
        for i in range(1, 10000):
            table.remove(i)
            times_remove.append(time.time() - start)
        gc.enable()

        fig, ax = plt.subplots()

        ax.scatter([i for i in range(1, 10000)], times_insert, color=['red'], s=0.5, label="Operation: insert")
        ax.scatter([i for i in range(1, 10000)], times_get, color=['green'], s=0.5, label="Operation: find")
        ax.scatter([i for i in range(1, 10000)], times_remove, color=['blue'],  s=0.5, label="Operation: remove")
        plt.legend(loc="best")
        plt.title(f"Hashtable worst all operations")
        ax.set_xlabel("Elements count")
        ax.set_ylabel("Time, sec")
        plt.show()

    @staticmethod
    def average_case():
        times_insert = list()
        times_get = list()
        times_remove = list()
        MAX = 1_000_000
        table = Hashtable(PROBENAME)

        gc.disable()
        start = time.time_ns()
        for i in range(1, MAX):
            table[i] = i
            times_insert.append(time.time_ns() - start)
        gc.enable()

        gc.disable()
        start = time.time_ns()
        for i in range(1, MAX):
            a = table[i]
            times_get.append(time.time_ns() - start)
        gc.enable()

        gc.disable()
        start = time.time_ns()
        for i in range(1, MAX):
            table.remove(i)
            times_remove.append(time.time_ns() - start)
        gc.enable()

        fig, ax = plt.subplots()

        ax.scatter(list(range(1, MAX)), times_insert, color=['red'], s=0.5, label="Operation: insert")
        ax.scatter(list(range(1, MAX)), times_get, color=['green'], s=0.5, label="Operation: find")
        ax.scatter(list(range(1, MAX)), times_remove, color=['blue'],  s=0.5, label="Operation: remove")
        plt.legend(loc="best")
        plt.title(f"Hashtable({PROBENAME}) average all operations")
        ax.set_xlabel("Elements count")
        ax.set_ylabel("Time, ns")
        plt.show()


HashtableGraphics.best_case()
#HashtableGraphics.worst_case()
#HashtableGraphics.average_case()