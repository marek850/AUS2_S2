from abc import ABC
import os
from DataStructure.Block import Block
class FileStructure(ABC):
    def __init__(self, block_size, record_type, file_name, load_file):
        self.__block_size = block_size  
        self.__record_type = record_type
        self.__file_path = file_name  
        self.__load_file = load_file
        self.__number_of_blocks = 0

        if not os.path.exists(self.__file_path):
            self._file = open(self.__file_path, "wb")
            self._file.close()
        self.__file = open(self.__file_path, "r+b")
    @property
    def load_file(self):
        return self.__load_file

    @load_file.setter
    def load_file(self, value):
        self.__load_file = value
    @property
    def file(self):
        return self.__file
    @property
    def record_type(self):
        return self.__record_type

    @property
    def block_size(self):
        return self.__block_size

    @property
    def file_path(self):
        return self.__file_path

    @property
    def number_of_blocks(self):
        return self.__number_of_blocks
    @file.setter
    def file(self, value):
        self.__file = value

    @record_type.setter
    def record_type(self, value):
        self.__record_type = value

    @block_size.setter
    def block_size(self, value):
        self.__block_size = value

    @file_path.setter
    def file_path(self, value):
        self.__file_path = value

    @number_of_blocks.setter
    def number_of_blocks(self, value):
        self.__number_of_blocks = value
    
    def get_block_offset(self, block_address):
        return block_address * self.__block_size

    def read_block(self, block_address):
        offset = self.get_block_offset(block_address)
        self.__file.seek(offset)
        block_data = self.__file.read(self.__block_size)
        if not block_data:
            return None
        return Block.from_byte_array(block_data,  type(self.__record_type), self.__block_size)

    def write_block(self, block_address, block):
        offset = self.get_block_offset(block_address)
        self.__file.seek(offset)
        self.__file.write(block.to_byte_array())

    def append_block(self, block):
        self.__file.seek(0, 2)  # Move to the end of the file
        self.__file.write(block.to_byte_array())

    def get_file_size(self):
        self.__file.seek(0, 2)  # Move to the end of the file
        return self.__file.tell()
    def get_all_blocks(self):
        blocks = []
        try:
            for block_address in range(self.__number_of_blocks):
                offset = self.get_block_offset(block_address)
                self.__file.seek(offset)
                block_data = self.__file.read(self.__block_size)
                if block_data:
                    block = Block.from_byte_array(block_data, type(self.__record_type), self.__block_size)
                    blocks.append(block)
        except Exception as e:
            print(f"An error occurred while reading blocks: {e}")
        return blocks