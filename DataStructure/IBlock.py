from abc import ABC, abstractmethod

class IBlock(ABC):
    
    @abstractmethod
    def get_size(self):
        pass
    @abstractmethod
    def from_byte_array(self):
        pass
    @abstractmethod
    def to_byte_array(self):
        pass    
    def decimal_to_binary(self, n, length=8):
        """
        Converts a decimal number to a binary representation with a fixed byte length.
        """
        return n.to_bytes(length, byteorder='big')  # Converts to `length` bytes

    def string_to_binary(self, string):
        """
        Converts a string to UTF-8 encoded bytes.
        """
        return string.encode('utf-8')
