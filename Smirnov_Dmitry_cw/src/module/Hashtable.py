from typing import NoReturn, Any, Callable


class Hashtable:
    def __init__(self, probe="linear"):
        self.__MAX_SIZE = 16384
        self.fill_factor = 0.75
        self.__item_count = 0
        self.__probe = probe
        self.__array = [None for _ in range(self.__MAX_SIZE)]

    def __linear_probing(self, index: int) -> int:
        return index

    def __quadratic_probing(self, index: int) -> int:
        return index * index

    def __double_probing(self, index: int, value: int) -> int:
        return index * self.__second_hash(value)

    def __choose_probing(self, index: int, value: int = 0) -> int:
        if self.__probe == "linear":
            return self.__linear_probing(index)
        elif self.__probe == "quadratic":
            return self.__quadratic_probing(index)
        elif self.__probe == "double":
            return self.__double_probing(index, value)

    def __setitem__(self, key, value) -> NoReturn:
        idx = 0
        hash_value = self.__first_hash(key)
        i = hash_value
        while True:
            if self.__array[i] is None or self.__array[i] == "del":
                self.__array[i] = (key, value)
                self.__item_count += 1
                if self.__item_count >= 0.75 * self.__MAX_SIZE:
                    self.__resize()
                break
            else:
                if self.__array[i][0] == key:
                    self.__array[i] = (key, value)
                    break
                idx += 1
                offset = self.__choose_probing(idx, hash_value)
                i = (hash_value + offset) % self.__MAX_SIZE

    def remove(self, key) -> NoReturn:
        if self.__item_count == 0:
            return
        hash_value = self.__first_hash(key)
        idx = 0
        i = hash_value
        while True:
            if self.__array[i] and self.__array[i][0] == key:
                self.__array[i] = "del"
                self.__item_count -= 1
                break
            idx += 1
            if idx >= self.__MAX_SIZE:
                break
            offset = self.__choose_probing(idx, hash_value)
            i = (hash_value + offset) % self.__MAX_SIZE

    def __getitem__(self, key) -> Any:
        if self.__item_count == 0:
            return
        hash_value = self.__first_hash(key)
        idx = 0
        i = hash_value
        while True:
            if self.__array[i] and self.__array[i] != "del" and self.__array[i][0] == key:
                return self.__array[i][1]
            idx += 1
            if idx >= self.__MAX_SIZE:
                raise KeyError("Key not found in hashtable (operation find)")
                break
            offset = self.__choose_probing(idx, hash_value)
            i = (hash_value + offset) % self.__MAX_SIZE

    def __first_hash(self, key: int) -> int:
        #return 0  # - worst case
        return key % self.__MAX_SIZE

    def __second_hash(self, value: int) -> int:
        #return 1  # - worst case
        return 107 - value % 107

    def __resize(self) -> NoReturn:
        self.__array += [None for _ in range(self.__MAX_SIZE)]
        self.__MAX_SIZE *= 2

    def __str__(self) -> list:
        return self.__array

    def __len__(self) -> int:
        return self.__item_count
