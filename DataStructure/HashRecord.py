from DataStructure.Record import Record


class HashRecord(Record):
    def __init__(self):
        super().__init__()
        self.__key = 0
    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, value):
        self.__key = value