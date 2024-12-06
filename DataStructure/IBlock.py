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
