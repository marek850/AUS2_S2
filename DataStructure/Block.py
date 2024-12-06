import sys
from DataStructure.IBlock import IBlock
from DataStructure.Record import Record

class Block(IBlock):
    def __init__(self, size, record = None):
        self.__valid_count = 0  # počet platných záznamov
        self.__record_type = record # Track the type of the initial record
        self.__records = []  # záznamy v bloku
        self.__size = size  # veľkosť bloku
        self.__next_block = None  # integer, adresa nasledovného bloku
        self.__previous_block = None  # adresa predchádzajúceho bloku
        while self.is_block_full() == False:
            self.__records.append(type(self.__record_type)())  # Fill with empty instances
        
        
    def __str__(self):
        records_str = "\n".join([str(record) for record in self.__records])
        return (
            f"Blok:\n"
            f"Záznamy:\n{records_str}\n"
            f"Nasledovník: {self.__next_block}\n"
            f"Predchodca: {self.__previous_block}\n"
        )
        
    def get_valid_records(self):
        return self.__records[:self.__valid_count]
    @property
    def valid_count(self):
        return self.__valid_count

    @property
    def record_type(self):
        return self.__record_type

    @property
    def records(self):
        return self.__records
    
    @property
    def next_block(self):
        return self.__next_block
    @valid_count.setter
    def valid_count(self, value):
        self.__valid_count = value
    @record_type.setter
    def record_type(self, value):
        self.__record_type = value
    @records.setter
    def records(self, value):
        self.__records = value
    @next_block.setter
    def next_block(self, value):
        self.__next_block = value
    @property
    def previous_block(self):
        return self.__previous_block

    @previous_block.setter
    def previous_block(self, value):
        self.__previous_block = value

    @property
    def size(self):
        return self.__size
    
    def add_record(self, record):
        if  self.is_full() == False:
            if not self.records:
                self.records.append(record)
            else:
                self.__records[self.__valid_count] = record
            self.__valid_count += 1
        else:
            return False
        
    def remove_record(self, record):
        for i in range(self.__valid_count):
            if self.__records[i] == record:
                self.__records.pop(i)
                self.__records.append(type(record)())
                self.__valid_count -= 1
        
    def is_block_full(self):
        return self.__size - self.get_current_size() < self.__record_type.get_size()
    
    def is_full(self):
        return self.__valid_count == len(self.records)

    def is_empty(self):
        return self.__valid_count == 0
    
    def to_byte_array(self, padding = True):
        byte_array = bytearray()
        byte_array += self.__valid_count.to_bytes(4, 'little')
        if self.__next_block is not None:
            byte_array += self.__next_block.to_bytes(4, 'little')
        else:
            byte_array.extend((2**10 - 1).to_bytes(4, 'little'))
        if self.__previous_block is not None:
            byte_array.extend(self.__previous_block.to_bytes(4, 'little'))
        else:
            byte_array.extend((2**10 - 1).to_bytes(4, 'little'))
        for record in self.__records:
            byte_array += record.to_byte_array()
        if len(byte_array) < self.__size and padding:
            byte_array += (10).to_bytes(self.__size - len(byte_array), 'little')

        return byte_array

    @staticmethod
    def from_byte_array(byte_array, record_class, size):
        cursor = 0
        valid_count = int.from_bytes(byte_array[cursor:cursor + 4], 'little')
        cursor += 4
        next_block_address = int.from_bytes(byte_array[cursor:cursor + 4], 'little')
        cursor += 4
        next_block = None if next_block_address == (2**10 - 1) else next_block_address
        previous_block_address = int.from_bytes(byte_array[cursor:cursor + 4], 'little')
        cursor += 4
        previous_block = None if previous_block_address == (2**10 - 1) else previous_block_address
        record_size = record_class().get_size()
        records = []
        while size - cursor >= record_size:
            record = record_class().from_byte_array(byte_array[cursor:])
            records.append(record)
            cursor += record_size
            
        block = Block(len(byte_array), record_class())    
        
        block.records = records
        block.valid_count = valid_count
        block.record_type = record_class
        block.next_block = next_block
        block.previous_block = previous_block
        return block
        
    def get_record(self, record):
        for i in range(self.valid_count):
            if self.__records[i] == record:
                return self.records[i]
            
    def get_current_size(self):
        return len(self.to_byte_array(padding=False))
    
    def get_size(self):
        return self.__size

