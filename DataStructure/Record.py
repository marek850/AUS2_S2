from abc import ABC, abstractmethod
from DataStructure.IBlock import IBlock

class Record(IBlock, ABC):
    def __init__(self):
        self.__max_str_length = 155
    @property
    def max_str_length(self):
        return self.__max_str_length

    @max_str_length.setter
    def max_str_length(self, value):
        if not isinstance(value, int):
            raise ValueError("max_str_length must be an integer")
        if value <= 0:
            raise ValueError("max_str_length must be positive")
        self.__max_str_length = value
    
    def fill_string(self, string):
        pass
    
    def get_size(self):
        """
        Returns the size of the Record in bytes.
        """
        return len(self.to_byte_array())

    def __eq__(self, other):
       pass

    @classmethod
    def from_byte_array(cls, byte_array):
        pass

    def to_byte_array(self):
        pass
