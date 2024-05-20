# OrderedSet.py

class OrderedSet:
    def __init__(self, iterable=None):
        self.data = {}
        if iterable is not None:
            for item in iterable:
                self.add(item)

    def add(self, value):
        self.data[value] = True

    def remove(self, value):
        del self.data[value]

    def pop(self):
        # 첫 번째 요소를 찾아 반환하고 삭제
        if not self.data:
            raise IndexError("pop from an empty set")
        # 딕셔너리의 첫 번째 키를 가져옴
        first_key = next(iter(self.data))
        del self.data[first_key]
        return first_key

    def __iter__(self):
        return iter(self.data)

    def __contains__(self, value):
        return value in self.data

    def __len__(self):
        return len(self.data)

